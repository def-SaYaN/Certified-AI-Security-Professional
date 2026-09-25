#!/usr/bin/env python3
"""
cAISP — Lab environment smoke test.

Run this after following the Lab Environment Setup guide:

    python labs/check_setup.py

It checks, in order:
  1. Your Python version.
  2. That you are (probably) inside a virtual environment.
  3. That the core lab libraries import correctly.
  4. That a tiny Hugging Face model can be downloaded and run (optional, needs
     internet). Skip this step with:  python labs/check_setup.py --no-network

The goal is that a complete beginner can look at the output and immediately know
whether they are ready for Chapter 1 — with GREEN meaning "go".

This script has NO third-party dependencies of its own, so it runs even if the
lab libraries failed to install (it will just tell you which ones are missing).
"""

from __future__ import annotations

import argparse
import importlib
import os
import platform
import sys
from dataclasses import dataclass


# --- Tiny, dependency-free coloured output ----------------------------------
# We avoid importing 'rich' here on purpose: this script must run even when the
# environment is broken, and 'rich' might be one of the things that failed.

_USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _c(text: str, code: str) -> str:
    if not _USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def green(t: str) -> str:
    return _c(t, "32")


def red(t: str) -> str:
    return _c(t, "31")


def yellow(t: str) -> str:
    return _c(t, "33")


def bold(t: str) -> str:
    return _c(t, "1")


PASS = green("PASS")
FAIL = red("FAIL")
WARN = yellow("WARN")
SKIP = yellow("SKIP")


@dataclass
class Result:
    ok: bool
    warn: bool = False


def check_python_version() -> Result:
    major, minor = sys.version_info[:2]
    version_str = f"{major}.{minor}.{sys.version_info[2]}"
    if (major, minor) >= (3, 10):
        print(f"[{PASS}] Python version {version_str} (need >= 3.10)")
        return Result(ok=True)
    print(f"[{FAIL}] Python version {version_str} is too old. Need Python 3.10+.")
    print("        Install a newer Python from https://www.python.org/downloads/")
    return Result(ok=False)


def check_virtualenv() -> Result:
    # sys.prefix != sys.base_prefix is the standard "am I in a venv?" test.
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if in_venv:
        print(f"[{PASS}] Running inside a virtual environment")
        print(f"        ({sys.prefix})")
        return Result(ok=True)
    print(f"[{WARN}] You do NOT appear to be in a virtual environment.")
    print("        This can work, but the course strongly recommends a venv so")
    print("        the lab libraries do not clash with your system Python.")
    print("        See the Lab Environment Setup page.")
    return Result(ok=True, warn=True)


def check_imports() -> Result:
    # (import_name, pip_name, chapter_first_needed)
    core = [
        ("numpy", "numpy", 1),
        ("requests", "requests", 1),
        ("rich", "rich", 1),
        ("torch", "torch", 1),
        ("transformers", "transformers", 1),
    ]
    optional = [
        ("sklearn", "scikit-learn", 1),
        ("pandas", "pandas", 1),
        ("sentence_transformers", "sentence-transformers", 1),
        ("bs4", "beautifulsoup4", 2),
        ("flask", "flask", 2),
        ("picklescan", "picklescan", 4),
    ]

    all_core_ok = True

    print()
    print(bold("Core libraries (required for Chapter 1):"))
    for import_name, pip_name, _chapter in core:
        if _can_import(import_name):
            print(f"  [{PASS}] {pip_name}")
        else:
            all_core_ok = False
            print(f"  [{FAIL}] {pip_name} — not importable")
            print(f"          Fix: pip install {pip_name}")

    print()
    print(bold("Additional libraries (used soon; nice to have now):"))
    any_optional_missing = False
    for import_name, pip_name, chapter in optional:
        if _can_import(import_name):
            print(f"  [{PASS}] {pip_name}")
        else:
            any_optional_missing = True
            print(f"  [{WARN}] {pip_name} — missing (first needed in Chapter {chapter})")

    if not all_core_ok:
        print()
        print(red("        One or more CORE libraries are missing."))
        print("        Run:  pip install -r labs/requirements.txt")

    return Result(ok=all_core_ok, warn=any_optional_missing)


def _can_import(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except Exception:
        return False


def check_model_download() -> Result:
    """Download and run a very small model to prove the pipeline works."""
    try:
        from transformers import pipeline
    except Exception:
        print(f"[{SKIP}] transformers not installed — skipping model test.")
        return Result(ok=True, warn=True)

    print()
    print("Downloading a tiny test model (~few MB) and running it...")
    print("(This proves your machine can fetch and execute a Hugging Face model.)")
    try:
        # A small, well-known sentiment model. We only care that the plumbing
        # works: download -> load -> run. The prediction itself is irrelevant.
        clf = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
        out = clf("This course setup is working great!")
        label = out[0]["label"]
        print(f"[{PASS}] Model ran. Sample output label: {label}")
        return Result(ok=True)
    except Exception as exc:  # noqa: BLE001 - we want to report anything
        print(f"[{FAIL}] Could not download/run the test model.")
        print(f"        Reason: {type(exc).__name__}: {exc}")
        print("        Common causes: no internet, a corporate proxy/VPN blocking")
        print("        huggingface.co, or a firewall. You can proceed offline for")
        print("        many labs; see the setup guide's Troubleshooting section.")
        return Result(ok=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="cAISP lab environment smoke test")
    parser.add_argument(
        "--no-network",
        action="store_true",
        help="Skip the model-download step (use if you are offline).",
    )
    args = parser.parse_args()

    print(bold("=" * 60))
    print(bold("  cAISP — Lab Environment Smoke Test"))
    print(bold("=" * 60))
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print()

    results: list[Result] = []
    results.append(check_python_version())
    results.append(check_virtualenv())
    results.append(check_imports())

    if args.no_network:
        print()
        print(f"[{SKIP}] Skipping model download (--no-network given).")
    else:
        results.append(check_model_download())

    print()
    print(bold("=" * 60))
    hard_fail = any((not r.ok) for r in results)
    warned = any(r.warn for r in results)

    if hard_fail:
        print(red(bold("  RESULT: NOT READY")))
        print("  Fix the FAIL items above, then run this script again.")
        print(bold("=" * 60))
        return 1

    if warned:
        print(yellow(bold("  RESULT: READY (with warnings)")))
        print("  You can start Chapter 1. Address WARN items when convenient.")
        print(bold("=" * 60))
        return 0

    print(green(bold("  RESULT: ALL GREEN — you are ready for Chapter 1!")))
    print(bold("=" * 60))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
