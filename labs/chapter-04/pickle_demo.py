#!/usr/bin/env python3
"""
cAISP — Lab 4.3: Scanning a Malicious Pickle File
==================================================

DEFENSIVE LAB. Demonstrates WHY loading a model file can be equivalent to
running a program, and how to scan for it.

The "malicious" payload here is deliberately HARMLESS: it writes a marker file
and prints a message. That is enough to prove arbitrary code executed, which is
the entire lesson. Nothing here is weaponized -- swap the payload for anything
real and you have malware, which is precisely the point you should take away.

USAGE
-----
    python labs/chapter-04/pickle_demo.py --build     # create the samples
    python labs/chapter-04/pickle_demo.py --inspect   # look inside, safely
    python labs/chapter-04/pickle_demo.py --scan      # scan them
    python labs/chapter-04/pickle_demo.py --detonate  # actually load it (safe)
    python labs/chapter-04/pickle_demo.py --all       # the full walkthrough
"""

from __future__ import annotations

import argparse
import os
import pathlib
import pickle
import pickletools
import sys
import tempfile


OUT_DIR = pathlib.Path("labs/chapter-04/_samples")
MARKER = pathlib.Path(tempfile.gettempdir()) / "caisp_pickle_executed.txt"


# =============================================================================
# SECTION 1 — Build the sample files
# =============================================================================


class BenignModel:
    """A perfectly ordinary object, the kind you'd expect in a model file."""

    def __init__(self):
        self.name = "sentiment-classifier-v1"
        self.weights = [0.21, -0.44, 0.87, 0.02]
        self.labels = ["NEGATIVE", "POSITIVE"]


class SuspiciousModel:
    """
    An object with a __reduce__ method.

    __reduce__ tells pickle HOW TO REBUILD this object. Pickle will call
    whatever callable __reduce__ returns, with the arguments it specifies.

    That is the vulnerability in one sentence: __reduce__ lets a pickle file
    specify a function call that happens automatically at load time. There is
    no sandbox and no confirmation.

    Our payload is harmless on purpose -- it writes a marker file so you can
    PROVE code ran.
    """

    def __reduce__(self):
        # Equivalent to: os.system("<command>") when unpickled.
        # We use a harmless marker write instead of anything destructive.
        cmd = (
            f"python3 -c \"open(r'{MARKER}','w')"
            f".write('arbitrary code executed at load time')\""
        )
        return (os.system, (cmd,))


def build_samples() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    benign_path = OUT_DIR / "benign_model.pkl"
    with open(benign_path, "wb") as f:
        pickle.dump(BenignModel(), f)

    malicious_path = OUT_DIR / "malicious_model.pkl"
    with open(malicious_path, "wb") as f:
        pickle.dump(SuspiciousModel(), f)

    print(f"[*] Created {benign_path}    ({benign_path.stat().st_size} bytes)")
    print(f"[*] Created {malicious_path} ({malicious_path.stat().st_size} bytes)")
    print()
    print("    Note: both are just '.pkl' files. Nothing about the name, the")
    print("    extension, or the size distinguishes them. In a model registry")
    print("    they would sit side by side looking identical.")


# =============================================================================
# SECTION 2 — Inspect WITHOUT executing
# =============================================================================


def inspect(path: pathlib.Path) -> None:
    """
    Disassemble the pickle opcodes. This does NOT execute the payload --
    pickletools reads the bytecode the way a disassembler reads a binary.
    """
    print(f"\n--- Opcode disassembly: {path.name} ---")
    with open(path, "rb") as f:
        data = f.read()

    try:
        import io
        buf = io.StringIO()
        pickletools.dis(data, out=buf)
        listing = buf.getvalue()
    except Exception as exc:
        print(f"  [!] Could not disassemble: {exc}")
        return

    # Highlight the dangerous opcodes
    dangerous = ("GLOBAL", "REDUCE", "STACK_GLOBAL", "INST", "OBJ", "NEWOBJ")
    for line in listing.splitlines():
        flag = ""
        if any(f" {d} " in f" {line} " or line.strip().startswith(d)
               for d in dangerous):
            flag = "   <== "
            if "GLOBAL" in line:
                flag += "imports a callable"
            elif "REDUCE" in line:
                flag += "CALLS it"
            else:
                flag += "object construction"
        print(f"  {line}{flag}")


def explain_opcodes() -> None:
    print("\n" + "=" * 68)
    print("WHAT YOU JUST SAW")
    print("=" * 68)
    print("  GLOBAL / STACK_GLOBAL  — import a callable by name (e.g. os.system)")
    print("  REDUCE                 — CALL the callable with the given arguments")
    print()
    print("  Together, GLOBAL + REDUCE = 'import this function and run it'.")
    print("  The benign file has no such pair. The malicious one does.")
    print()
    print("  This is not an exploit of a bug. Pickle is WORKING AS DESIGNED --")
    print("  it is a serialisation format that supports reconstructing")
    print("  arbitrary Python objects, and reconstruction means calling code.")
    print("=" * 68)


# =============================================================================
# SECTION 3 — Scan
# =============================================================================


def scan(path: pathlib.Path) -> None:
    """Use picklescan if present; fall back to our own opcode check."""
    print(f"\n--- Scanning {path.name} ---")
    try:
        from picklescan.scanner import scan_file_path
        result = scan_file_path(str(path))
        globals_found = getattr(result, "globals", [])
        issues = getattr(result, "issues_count", None)
        print(f"  picklescan: issues={issues}")
        for g in globals_found:
            module = getattr(g, "module", "?")
            name = getattr(g, "name", "?")
            safety = getattr(g, "safety", "?")
            print(f"    - {module}.{name}   [{safety}]")
        if issues:
            print("  VERDICT: DANGEROUS — do not load this file.")
        else:
            print("  VERDICT: no known-dangerous imports found.")
    except ImportError:
        print("  (picklescan not installed — using built-in fallback check)")
        print("   Install with: pip install picklescan")
        fallback_scan(path)
    except Exception as exc:
        print(f"  [!] picklescan error: {type(exc).__name__}: {exc}")
        fallback_scan(path)


DANGEROUS_IMPORTS = [
    b"os", b"subprocess", b"sys", b"builtins", b"eval", b"exec",
    b"system", b"popen", b"posix", b"nt", b"commands", b"socket",
]


def fallback_scan(path: pathlib.Path) -> None:
    """A minimal opcode-level check, so the lab works without picklescan."""
    with open(path, "rb") as f:
        data = f.read()

    found = []
    import io
    buf = io.StringIO()
    try:
        pickletools.dis(data, out=buf)
    except Exception:
        print("    [!] malformed pickle")
        return
    listing = buf.getvalue()

    has_reduce = "REDUCE" in listing
    for token in DANGEROUS_IMPORTS:
        t = token.decode()
        if f"'{t}'" in listing or f" {t} " in listing:
            found.append(t)

    if has_reduce and found:
        print(f"    DANGEROUS: REDUCE opcode + suspicious imports {found}")
        print("    VERDICT: do not load this file.")
    elif has_reduce:
        print("    WARNING: REDUCE opcode present (calls a function on load)")
    else:
        print("    No REDUCE opcode and no suspicious imports found.")


# =============================================================================
# SECTION 4 — Detonate (safely)
# =============================================================================


def detonate(path: pathlib.Path) -> None:
    """Actually load the file, proving the payload runs. Payload is harmless."""
    print(f"\n--- Loading {path.name} with pickle.load() ---")
    if MARKER.exists():
        MARKER.unlink()

    print(f"  Marker file before load: exists={MARKER.exists()}")
    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        print(f"  Loaded object: {type(obj).__name__}")
    except Exception as exc:
        print(f"  Load raised: {type(exc).__name__}: {exc}")

    print(f"  Marker file after load : exists={MARKER.exists()}")
    if MARKER.exists():
        print(f"  Marker contents        : {MARKER.read_text()!r}")
        print()
        print("  *** ARBITRARY CODE EXECUTED. You only called pickle.load(). ***")
        print("  Our payload wrote a file. A real one would open a reverse")
        print("  shell, steal your cloud credentials, or install persistence.")
        MARKER.unlink()
    else:
        print("  (no marker written)")


# =============================================================================
# SECTION 5 — Runner
# =============================================================================


def safe_formats_note() -> None:
    print("\n" + "=" * 68)
    print("THE DEFENCES")
    print("=" * 68)
    print("  1. PREFER SAFETENSORS. It stores only numbers + metadata. There")
    print("     is no mechanism to execute code. This is the real fix.")
    print()
    print("  2. SCAN before loading:   picklescan --path model.pkl")
    print("     Catches known-dangerous patterns. Not a guarantee.")
    print()
    print("  3. SANDBOX untrusted loads: no network, no credentials, no")
    print("     production access. Assume the load may be hostile.")
    print()
    print("  4. VERIFY PROVENANCE. Signatures and hashes (Chapter 6).")
    print("     This is the only defence that scales.")
    print()
    print("  REMEMBER: scanning catches malicious FILES. It does not catch a")
    print("  malicious MODEL -- a backdoor in the weights (Lab 2.9) lives in a")
    print("  structurally innocent file. Different problem, different defence.")
    print("=" * 68)


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 4.3 - pickle security")
    p.add_argument("--build", action="store_true")
    p.add_argument("--inspect", action="store_true")
    p.add_argument("--scan", action="store_true")
    p.add_argument("--detonate", action="store_true")
    p.add_argument("--all", action="store_true")
    args = p.parse_args()

    if not any([args.build, args.inspect, args.scan, args.detonate, args.all]):
        args.all = True

    benign = OUT_DIR / "benign_model.pkl"
    malicious = OUT_DIR / "malicious_model.pkl"

    print()
    print("#" * 68)
    print("#  LAB 4.3 — WHY LOADING A MODEL IS RUNNING A PROGRAM")
    print("#" * 68)

    if args.build or args.all:
        print("\n[STEP 1] Building sample files")
        build_samples()

    if not malicious.exists():
        print("\n[!] Samples missing. Run with --build first.")
        return 1

    if args.inspect or args.all:
        print("\n[STEP 2] Inspecting WITHOUT executing (pickletools)")
        inspect(benign)
        inspect(malicious)
        explain_opcodes()

    if args.scan or args.all:
        print("\n[STEP 3] Scanning")
        scan(benign)
        scan(malicious)

    if args.detonate or args.all:
        print("\n[STEP 4] Proving the payload executes (harmless marker)")
        detonate(malicious)

    if args.all:
        safe_formats_note()

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
