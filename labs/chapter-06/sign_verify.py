#!/usr/bin/env python3
"""
cAISP — Lab 6.5: Signing and Verifying Machine Learning Models
===============================================================

Demonstrates the defence that actually scales: cryptographic provenance.

This lab has two paths:

  A) PURE PYTHON (always works, no installs). Uses the standard library to
     build a real signing/verification flow with hashes + HMAC, so you can
     see the mechanics and, crucially, watch verification FAIL on tampering.

  B) COSIGN (real-world tool). Instructions in the walkthrough. Same
     concepts, production tooling, keyless identity-based signing.

Start with A. It is the part that teaches the mechanism.

USAGE
-----
    python labs/chapter-06/sign_verify.py --demo      # full walkthrough
    python labs/chapter-06/sign_verify.py --tamper    # show detection
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import pathlib
import secrets
import sys
import time


WORK = pathlib.Path("labs/chapter-06/_signing")


# =============================================================================
# The primitives
# =============================================================================


def sha256_file(path: pathlib.Path) -> str:
    """The digest. A single changed byte changes this completely."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sign(digest: str, key: bytes) -> str:
    """
    Produce a signature over the digest.

    We use HMAC here because it needs no dependencies and demonstrates the
    flow exactly. REAL signing uses asymmetric crypto (a private key signs,
    a public key verifies) so the verifier does not need the secret.
    Cosign additionally binds the signature to an IDENTITY rather than a key.
    """
    return hmac.new(key, digest.encode(), hashlib.sha256).hexdigest()


def verify(digest: str, signature: str, key: bytes) -> bool:
    expected = sign(digest, key)
    # constant-time comparison: avoid leaking information through timing
    return hmac.compare_digest(expected, signature)


# =============================================================================
# Attestation
# =============================================================================


def make_attestation(model_path: pathlib.Path, signer: str,
                     provenance: dict) -> dict:
    """
    An attestation is a SIGNED STATEMENT about an artefact.

    Note it carries provenance (how it was built), not just the digest --
    this is the SLSA idea from section 6.4.
    """
    return {
        "artifact": model_path.name,
        "sha256": sha256_file(model_path),
        "signer": signer,
        "signed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": provenance,
    }


# =============================================================================
# The demo
# =============================================================================


def setup() -> tuple[pathlib.Path, bytes]:
    WORK.mkdir(parents=True, exist_ok=True)
    model = WORK / "sentiment_model.safetensors"
    # A stand-in "model": header + some weights
    payload = b'{"__metadata__":{"format":"pt","version":"1.0"}}'
    payload += bytes(range(256)) * 8
    model.write_bytes(payload)
    key = secrets.token_bytes(32)
    return model, key


def step_publish(model: pathlib.Path, key: bytes) -> dict:
    print("=" * 70)
    print("STEP 1 — THE PUBLISHER SIGNS THE MODEL")
    print("=" * 70)

    digest = sha256_file(model)
    print(f"\n  model   : {model.name} ({model.stat().st_size} bytes)")
    print(f"  sha256  : {digest}")

    attestation = make_attestation(
        model,
        signer="ml-platform@acme-corp.com",
        provenance={
            "source_repo": "github.com/acme/sentiment-model",
            "source_commit": "a1b2c3d4e5f6",
            "dataset": "support-tickets-v7",
            "dataset_sha256": "9f8e7d6c5b4a...",
            "trained_by": "ci-job-4471",
            "base_model": "distilbert-base-uncased",
        },
    )
    signature = sign(digest, key)
    attestation["signature"] = signature

    att_path = model.with_suffix(model.suffix + ".att.json")
    att_path.write_text(json.dumps(attestation, indent=2))

    print(f"\n  attestation written to {att_path.name}:")
    for line in json.dumps(attestation, indent=2).splitlines()[:14]:
        print(f"    {line}")
    print("    ...")
    print("\n  The attestation binds together:")
    print("    * WHAT the artefact is    (sha256)")
    print("    * WHO vouches for it      (signer)")
    print("    * HOW it was built        (provenance)")
    print("    * PROOF of the claim      (signature)")
    return attestation


def step_verify_good(model: pathlib.Path, att: dict, key: bytes) -> None:
    print("\n" + "=" * 70)
    print("STEP 2 — THE CONSUMER VERIFIES (untampered)")
    print("=" * 70)

    actual = sha256_file(model)
    print(f"\n  recomputed sha256 : {actual[:32]}...")
    print(f"  attested  sha256  : {att['sha256'][:32]}...")
    digest_ok = actual == att["sha256"]
    print(f"  digest match      : {digest_ok}")

    sig_ok = verify(att["sha256"], att["signature"], key)
    print(f"  signature valid   : {sig_ok}")
    print(f"  signer            : {att['signer']}")

    if digest_ok and sig_ok:
        print("\n  ✅ ACCEPT — integrity and authenticity both confirmed.")
    else:
        print("\n  ❌ REJECT")


def step_tamper(model: pathlib.Path, att: dict, key: bytes) -> None:
    print("\n" + "=" * 70)
    print("STEP 3 — AN ATTACKER TAMPERS WITH THE MODEL")
    print("=" * 70)

    original = model.read_bytes()
    print(f"\n  original sha256 : {sha256_file(model)[:32]}...")

    # Flip ONE bit in ONE byte -- the smallest possible change.
    data = bytearray(original)
    idx = len(data) // 2
    before = data[idx]
    data[idx] ^= 0x01
    model.write_bytes(bytes(data))

    print(f"  attacker flips ONE BIT at offset {idx} "
          f"({before} -> {data[idx]})")
    print(f"  new      sha256 : {sha256_file(model)[:32]}...")

    print("\n  Consumer verifies again:")
    actual = sha256_file(model)
    digest_ok = actual == att["sha256"]
    print(f"    digest match    : {digest_ok}")
    sig_ok = verify(actual, att["signature"], key)
    print(f"    signature valid : {sig_ok}")
    print("\n  ❌ REJECT — tampering detected.")
    print("\n  One flipped bit in a 2 KB file was caught. In a 10 GB model")
    print("  the result is identical: any change whatsoever breaks the hash.")

    model.write_bytes(original)   # restore


def step_limits() -> None:
    print("\n" + "=" * 70)
    print("STEP 4 — WHAT SIGNING DOES *NOT* PROVE")
    print("=" * 70)
    print("""
  A signature proves:
    ✅ WHO published this artefact
    ✅ That it has NOT CHANGED since they signed it

  A signature does NOT prove:
    ❌ That the model is free of backdoors      (Lab 2.9)
    ❌ That the model is accurate or unbiased
    ❌ That the training data was clean         (section 6.2)
    ❌ That the publisher is trustworthy

  An attacker can sign a backdoored model -- honestly. The signature will
  verify perfectly, because they really did publish it.

  What signing gives you is ACCOUNTABILITY:
    * you know exactly whose model you are running
    * you can decide whether you trust THAT PUBLISHER
    * any later substitution or alteration is detected

  For an artefact you cannot inspect, "do I trust this publisher?" is the
  only form of the trust question you can actually answer. Signing is what
  makes it answerable.

  And because you might be WRONG about the publisher, the final control
  remains: constrain what the model can DO once loaded (Chapter 3, LLM08).
""")


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 6.5 - model signing")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--tamper", action="store_true",
                   help="Only run the tamper-detection step")
    args = p.parse_args()

    print()
    print("#" * 70)
    print("#  LAB 6.5 — SIGNING AND VERIFYING MODELS")
    print("#" * 70)
    print()

    model, key = setup()
    att = step_publish(model, key)

    if args.tamper:
        step_tamper(model, att, key)
        return 0

    step_verify_good(model, att, key)
    step_tamper(model, att, key)
    step_limits()
    return 0


if __name__ == "__main__":
    sys.exit(main())
