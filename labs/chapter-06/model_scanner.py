#!/usr/bin/env python3
"""
cAISP — Lab 6.3: Scanning Models for Malicious Code
====================================================

A multi-layer model scanner you can actually run and extend.

Layers, weakest to strongest:
  1. FORMAT       — is this a code-executing format at all?
  2. OPCODE       — does the pickle stream import/call dangerous things?
  3. STRUCTURE    — does the archive contain unexpected non-model files?
  4. INTEGRITY    — does the file match an expected hash?
  5. PROVENANCE   — is it signed by someone we trust?  (Lab 6.5)

The point of the lab is layer 5. Layers 1-4 catch malicious FILES.
Only layer 5 addresses malicious MODELS -- and even then only by making
"do I trust this publisher?" answerable.

USAGE
-----
    python labs/chapter-06/model_scanner.py --build      # make samples
    python labs/chapter-06/model_scanner.py --scan-all   # scan them
    python labs/chapter-06/model_scanner.py FILE         # scan one file
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import pathlib
import pickle
import pickletools
import sys
import zipfile


SAMPLES = pathlib.Path("labs/chapter-06/_samples")

# Formats that CANNOT execute code on load.
SAFE_FORMATS = {".safetensors", ".gguf", ".onnx", ".json", ".npz"}
# Formats that CAN.
RISKY_FORMATS = {".pkl", ".pickle", ".pt", ".pth", ".bin", ".ckpt", ".h5", ".joblib"}

DANGEROUS_MODULES = {
    "os", "posix", "nt", "subprocess", "sys", "builtins", "__builtin__",
    "socket", "shutil", "importlib", "runpy", "pty", "commands", "popen2",
    "requests", "urllib", "httplib", "ftplib", "telnetlib", "smtplib",
}
DANGEROUS_NAMES = {
    "system", "popen", "exec", "eval", "compile", "execfile", "open",
    "spawn", "spawnl", "spawnv", "fork", "call", "check_output", "run",
    "__import__", "getattr", "setattr", "loads", "load",
}


class Finding:
    def __init__(self, layer: str, severity: str, message: str):
        self.layer, self.severity, self.message = layer, severity, message

    def __str__(self) -> str:
        return f"[{self.severity:<8}] {self.layer:<10} {self.message}"


# =============================================================================
# LAYER 1 — Format
# =============================================================================

def check_format(path: pathlib.Path) -> list[Finding]:
    ext = path.suffix.lower()
    if ext in SAFE_FORMATS:
        return [Finding("format", "OK",
                        f"'{ext}' cannot execute code on load. Good choice.")]
    if ext in RISKY_FORMATS:
        return [Finding("format", "WARNING",
                        f"'{ext}' is a code-executing format. Prefer "
                        f".safetensors where possible.")]
    return [Finding("format", "INFO", f"Unrecognised extension '{ext}'.")]


# =============================================================================
# LAYER 2 — Opcode analysis (without executing)
# =============================================================================

def _analyse_pickle_stream(data: bytes, label: str) -> list[Finding]:
    findings: list[Finding] = []
    buf = io.StringIO()
    try:
        pickletools.dis(data, out=buf)
    except Exception as exc:
        return [Finding("opcode", "WARNING",
                        f"{label}: could not disassemble ({type(exc).__name__})")]

    listing = buf.getvalue()
    has_reduce = "REDUCE" in listing or "INST" in listing or "OBJ" in listing

    # Collect GLOBAL / STACK_GLOBAL operands
    imports: set[str] = set()
    lines = listing.splitlines()
    for i, line in enumerate(lines):
        if "GLOBAL" in line:
            # operands appear on this line or the preceding two
            window = " ".join(lines[max(0, i - 2): i + 1])
            for tok in window.replace("'", " ").replace('"', " ").split():
                if tok in DANGEROUS_MODULES or tok in DANGEROUS_NAMES:
                    imports.add(tok)

    if imports and has_reduce:
        findings.append(Finding(
            "opcode", "CRITICAL",
            f"{label}: dangerous import(s) {sorted(imports)} combined with a "
            f"call opcode. This file executes code on load. DO NOT LOAD."))
    elif imports:
        findings.append(Finding(
            "opcode", "WARNING",
            f"{label}: suspicious import(s) {sorted(imports)} present."))
    elif has_reduce:
        findings.append(Finding(
            "opcode", "INFO",
            f"{label}: object-construction opcodes present (normal for many "
            f"models, but it is the mechanism attackers use)."))
    else:
        findings.append(Finding("opcode", "OK",
                                f"{label}: no dangerous imports or calls."))
    return findings


def check_opcodes(path: pathlib.Path) -> list[Finding]:
    ext = path.suffix.lower()
    if ext not in RISKY_FORMATS:
        return [Finding("opcode", "OK", "Not a pickle-based format; skipped.")]

    # PyTorch .pt/.pth are usually ZIP archives containing a pickle
    if zipfile.is_zipfile(path):
        findings = []
        with zipfile.ZipFile(path) as z:
            pickles = [n for n in z.namelist()
                       if n.endswith((".pkl", "data.pkl"))]
            if not pickles:
                findings.append(Finding("opcode", "INFO",
                                        "ZIP archive with no pickle member."))
            for name in pickles:
                findings += _analyse_pickle_stream(z.read(name), name)
        return findings

    with open(path, "rb") as f:
        return _analyse_pickle_stream(f.read(), path.name)


# =============================================================================
# LAYER 3 — Structure
# =============================================================================

EXPECTED_IN_ARCHIVE = (".pkl", ".json", ".txt", ".bin", ".storage", "data/",
                       "version", "byteorder", ".safetensors", ".md")


def check_structure(path: pathlib.Path) -> list[Finding]:
    if not zipfile.is_zipfile(path):
        return [Finding("structure", "OK", "Not an archive; skipped.")]
    findings = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        findings.append(Finding("structure", "INFO",
                                f"Archive contains {len(names)} member(s)."))
        for n in names:
            low = n.lower()
            if low.endswith((".py", ".sh", ".exe", ".dll", ".so", ".bat")):
                findings.append(Finding(
                    "structure", "CRITICAL",
                    f"Executable/script file inside model archive: {n}"))
            elif not any(tok in low for tok in EXPECTED_IN_ARCHIVE):
                findings.append(Finding(
                    "structure", "WARNING", f"Unexpected member: {n}"))
    return findings


# =============================================================================
# LAYER 4 — Integrity
# =============================================================================

def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_integrity(path: pathlib.Path,
                    expected: dict[str, str]) -> list[Finding]:
    digest = sha256(path)
    want = expected.get(path.name)
    if want is None:
        return [Finding("integrity", "WARNING",
                        f"No expected hash recorded. sha256={digest[:16]}... "
                        f"Pin this in your manifest.")]
    if want == digest:
        return [Finding("integrity", "OK", "Hash matches the pinned value.")]
    return [Finding("integrity", "CRITICAL",
                    "HASH MISMATCH — the file is not what you pinned. "
                    "Possible substitution.")]


# =============================================================================
# LAYER 5 — Provenance
# =============================================================================

def check_provenance(path: pathlib.Path) -> list[Finding]:
    sig = path.with_suffix(path.suffix + ".sig")
    cert = path.with_suffix(path.suffix + ".pem")
    card = path.with_name(path.stem + ".modelcard.json")

    findings = []
    if sig.exists() or cert.exists():
        findings.append(Finding("provenance", "INFO",
                                "Signature material present — VERIFY it "
                                "(see Lab 6.5). Presence is not validity."))
    else:
        findings.append(Finding(
            "provenance", "CRITICAL",
            "NO SIGNATURE. You cannot establish who produced this file. "
            "This is the finding that matters most."))

    if card.exists():
        try:
            meta = json.loads(card.read_text())
            base = meta.get("base_model", "?")
            findings.append(Finding("provenance", "OK",
                                    f"Model card present (base: {base})."))
        except Exception:
            findings.append(Finding("provenance", "WARNING",
                                    "Model card present but unreadable."))
    else:
        findings.append(Finding("provenance", "WARNING",
                                "No model card. Training data, intended use "
                                "and limitations are undocumented."))
    return findings


# =============================================================================
# Sample builder
# =============================================================================

class Benign:
    def __init__(self):
        self.name = "clf-v1"
        self.weights = [0.1, 0.2, 0.3]


class Malicious:
    """Harmless marker payload; see Lab 4.3 for the full explanation."""
    def __reduce__(self):
        marker = pathlib.Path("/tmp/caisp_ch6_marker.txt")
        return (os.system, (f"python3 -c \"open(r'{marker}','w').write('x')\"",))


def build_samples() -> None:
    SAMPLES.mkdir(parents=True, exist_ok=True)

    with open(SAMPLES / "clean_model.pkl", "wb") as f:
        pickle.dump(Benign(), f)

    with open(SAMPLES / "malicious_model.pkl", "wb") as f:
        pickle.dump(Malicious(), f)

    # A "safetensors-like" file: pure data, no code paths
    (SAMPLES / "safe_model.safetensors").write_bytes(
        b'{"__metadata__":{"format":"pt"}}' + b"\x00" * 128)

    # A well-documented model, to show what good looks like
    (SAMPLES / "documented_model.safetensors").write_bytes(
        b'{"__metadata__":{"format":"pt"}}' + b"\x00" * 128)
    (SAMPLES / "documented_model.modelcard.json").write_text(json.dumps({
        "name": "documented_model",
        "version": "1.2.0",
        "base_model": "distilbert-base-uncased",
        "training_data": "internal-support-tickets-v7 (curated, PII-scrubbed)",
        "intended_use": "Support ticket classification",
        "out_of_scope": "Any decision affecting a person's rights",
        "limitations": "Degrades on non-English text",
        "publisher": "ACME ML Platform Team",
    }, indent=2))
    (SAMPLES / "documented_model.safetensors.sig").write_text("<demo signature>")

    print(f"[*] Samples created in {SAMPLES}/")
    for p in sorted(SAMPLES.iterdir()):
        print(f"      {p.name:<40} {p.stat().st_size:>6} bytes")


# =============================================================================
# Scanner
# =============================================================================

SEVERITY_ORDER = {"CRITICAL": 0, "WARNING": 1, "INFO": 2, "OK": 3}


def scan(path: pathlib.Path, expected: dict[str, str]) -> str:
    print("=" * 72)
    print(f"SCANNING  {path.name}")
    print("=" * 72)

    findings: list[Finding] = []
    findings += check_format(path)
    findings += check_opcodes(path)
    findings += check_structure(path)
    findings += check_integrity(path, expected)
    findings += check_provenance(path)

    findings.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 9))
    for f in findings:
        print(f"  {f}")

    worst = min((SEVERITY_ORDER.get(f.severity, 9) for f in findings),
                default=3)
    verdict = {0: "REJECT", 1: "REVIEW", 2: "REVIEW", 3: "ACCEPT"}[worst]
    print(f"\n  VERDICT: {verdict}")
    print()
    return verdict


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 6.3 - model scanner")
    p.add_argument("file", nargs="?", help="Model file to scan")
    p.add_argument("--build", action="store_true", help="Create samples")
    p.add_argument("--scan-all", action="store_true", help="Scan all samples")
    args = p.parse_args()

    print()
    print("#" * 72)
    print("#  LAB 6.3 — MULTI-LAYER MODEL SCANNER")
    print("#" * 72)
    print()

    if args.build:
        build_samples()
        return 0

    # A tiny "pinned hashes" manifest — in reality this lives in version control
    manifest_path = SAMPLES / "manifest.json"
    expected = {}
    if manifest_path.exists():
        expected = json.loads(manifest_path.read_text())

    if args.scan_all:
        if not SAMPLES.exists():
            build_samples()
            print()
        results = {}
        for f in sorted(SAMPLES.iterdir()):
            if f.suffix in {".json"} or f.name.endswith(".sig"):
                continue
            results[f.name] = scan(f, expected)

        print("=" * 72)
        print("SUMMARY")
        print("=" * 72)
        for name, verdict in results.items():
            print(f"  {verdict:<8} {name}")
        print()
        print("  Note what the scanner CAN and CANNOT tell you:")
        print("   * It caught the malicious FILE (opcode layer).")
        print("   * It flagged the missing signatures (provenance layer).")
        print("   * It CANNOT tell you whether 'clean_model.pkl' contains a")
        print("     BACKDOOR in its weights. No scanner can. That is why")
        print("     provenance -- not scanning -- is the defence that scales.")
        print()
        return 0

    if args.file:
        scan(pathlib.Path(args.file), expected)
        return 0

    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
