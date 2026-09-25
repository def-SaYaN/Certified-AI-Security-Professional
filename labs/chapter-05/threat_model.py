#!/usr/bin/env python3
"""
cAISP — Lab 5.1: Threat Modeling an AI System
==============================================

A scaffold for producing a complete, structured threat model.

This is NOT a tool that finds threats for you -- no tool can, and any that
claims to is selling you a checklist. This is a framework that:

  * holds your DFD elements and trust boundaries
  * walks you through STRIDE for every element
  * cross-references OWASP LLM Top 10 and MITRE ATLAS
  * rates risk (likelihood x impact) and bands it
  * emits a report you could hand to an engineering team

The THINKING is yours. The STRUCTURE is here so nothing gets missed.

USAGE
-----
    python labs/chapter-05/threat_model.py --example    # the worked example
    python labs/chapter-05/threat_model.py --checklist  # blank STRIDE grid
    python labs/chapter-05/threat_model.py --report     # markdown report
    python labs/chapter-05/threat_model.py --gaps       # coverage check
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field


# =============================================================================
# SECTION 1 — The data model
# =============================================================================


@dataclass
class Element:
    """One node in the data flow diagram."""
    eid: str
    name: str
    kind: str          # external_entity | process | data_store | data_flow
    zone: str = ""
    notes: str = ""


@dataclass
class TrustBoundary:
    bid: str
    name: str
    crosses: str       # which flows cross it
    why: str


@dataclass
class Threat:
    tid: str
    description: str
    element: str
    stride: str                        # S/T/R/I/D/E
    owasp: list[str] = field(default_factory=list)
    atlas: list[str] = field(default_factory=list)
    likelihood: int = 3                # 1-5
    impact: int = 3                    # 1-5
    treatment: str = "Mitigate"        # Mitigate|Transfer|Accept|Avoid
    action: str = ""
    owner: str = ""
    residual: int = 0

    @property
    def score(self) -> int:
        return self.likelihood * self.impact

    @property
    def band(self) -> str:
        s = self.score
        if s >= 20:
            return "CRITICAL"
        if s >= 12:
            return "HIGH"
        if s >= 6:
            return "MEDIUM"
        if s >= 3:
            return "LOW"
        return "MINIMAL"


STRIDE_NAMES = {
    "S": "Spoofing",
    "T": "Tampering",
    "R": "Repudiation",
    "I": "Information disclosure",
    "D": "Denial of service",
    "E": "Elevation of privilege",
}

STRIDE_QUESTIONS = {
    "S": "Can someone pretend to be someone/something else here?",
    "T": "Can someone modify data, code, or behaviour they shouldn't?",
    "R": "Can someone deny having done something? Is it logged?",
    "I": "Can someone see data they shouldn't?",
    "D": "Can someone exhaust or break this?",
    "E": "Can someone gain privileges they shouldn't have?",
}

# Which STRIDE categories conventionally apply to which element kinds.
APPLICABLE = {
    "external_entity": "SR",
    "process":         "STRIDE",
    "data_store":      "TRID",
    "data_flow":       "TID",
}


# =============================================================================
# SECTION 2 — The worked example (ACME support assistant, section 5.4)
# =============================================================================


def build_example() -> tuple[list[Element], list[TrustBoundary], list[Threat]]:
    elements = [
        Element("E1", "Customer", "external_entity", "Internet"),
        Element("E2", "Attacker", "external_entity", "Internet",
                "Can file support tickets"),
        Element("P1", "Web frontend", "process", "App"),
        Element("P2", "Chat API", "process", "App"),
        Element("P3", "Guardrails", "process", "App"),
        Element("P4", "Prompt assembly", "process", "App",
                "Merges system prompt + retrieved chunks + user input"),
        Element("P5", "Tool orchestrator", "process", "App",
                "Calls lookup_order and issue_refund"),
        Element("P6", "LLM (3rd-party API)", "process", "AI"),
        Element("P7", "Embedding model", "process", "AI"),
        Element("D1", "Vector store", "data_store", "Data"),
        Element("D2", "Document corpus", "data_store", "Data",
                "Wiki pages AND customer-submitted tickets"),
        Element("D3", "Orders DB", "data_store", "Data"),
        Element("D4", "Prompt logs", "data_store", "Data",
                "Every prompt and response"),
    ]

    boundaries = [
        TrustBoundary("TB1", "Internet -> Application", "a",
                      "Classic perimeter; everyone draws this"),
        TrustBoundary("TB2", "Untrusted content -> Prompt", "d, g",
                      "User input AND retrieved chunks enter the prompt. "
                      "USUALLY UNMARKED."),
        TrustBoundary("TB3", "LLM output -> trusted contexts", "i, k",
                      "Model output reaches the orchestrator and the browser. "
                      "USUALLY UNMARKED."),
        TrustBoundary("TB4", "Orchestrator -> Orders DB", "j",
                      "Identity CHANGES here: app credentials, not the user's."),
        TrustBoundary("TB5", "App -> 3rd-party LLM", "h",
                      "Customer data leaves our control"),
    ]

    threats = [
        Threat("T-01",
               "Attacker files a poisoned support ticket; it is indexed and "
               "later retrieved for an innocent customer's question, causing "
               "the model to issue an unauthorised refund.",
               "D2 -> P4 -> P5", "T",
               ["LLM01", "LLM03", "LLM08"], ["Execution", "Impact"],
               likelihood=4, impact=5,
               treatment="Avoid",
               action="Model PROPOSES refunds; human approves. Remove "
                      "autonomous refund capability.",
               owner="Eng lead", residual=6),

        Threat("T-02",
               "Retrieval does not enforce the asking user's permissions, so "
               "confidential documents can be surfaced to any user.",
               "D1 / P4", "I",
               ["LLM06"], ["Collection"],
               likelihood=4, impact=4,
               action="Filter retrieval results by the requesting user's "
                      "entitlements, sourced from the document system.",
               owner="Platform", residual=4),

        Threat("T-03",
               "Tool calls execute with application credentials rather than "
               "the requesting user's identity (confused deputy).",
               "P5 -> D3", "E",
               ["LLM07", "LLM08"], ["Privilege Escalation"],
               likelihood=4, impact=4,
               action="Authorise every tool call in the end user's context; "
                      "scope per-tool credentials to least privilege.",
               owner="Platform", residual=4),

        Threat("T-04",
               "System prompt contains internal URLs and an admin password; "
               "extractable via prompt injection.",
               "P4", "I",
               ["LLM06", "LLM01"], ["Discovery", "Credential Access"],
               likelihood=5, impact=3,
               treatment="Avoid",
               action="Remove all secrets from the prompt. Enforce business "
                      "rules in application code, not in instructions.",
               owner="Eng lead", residual=3),

        Threat("T-05",
               "Prompt logs contain customer PII, secrets users pasted, and "
               "retrieved confidential content, with broad internal access.",
               "D4", "I",
               ["LLM06"], ["Collection"],
               likelihood=3, impact=4,
               action="Redact PII on ingest; restrict log access; set 30-day "
                      "retention.",
               owner="Data", residual=6),

        Threat("T-06",
               "Token-dense input inflates inference cost far beyond what a "
               "character-based limit would suggest (denial of wallet).",
               "P2 / P6", "D",
               ["LLM04"], ["Impact"],
               likelihood=4, impact=2,
               action="Rate limit on TOKENS not characters; per-user quotas; "
                      "spend alerting.",
               owner="Platform", residual=4),

        Threat("T-07",
               "Model output rendered into the page without escaping, "
               "enabling XSS and template injection.",
               "P6 -> P1", "T",
               ["LLM02"], ["Impact"],
               likelihood=3, impact=3,
               action="Escape all model output; use static templates with "
                      "auto-escaping; allowlist link/image domains.",
               owner="Frontend", residual=3),

        Threat("T-08",
               "Third-party LLM provider outage or rate limiting takes the "
               "assistant offline.",
               "P6", "D",
               ["LLM05"], [],
               likelihood=3, impact=3,
               treatment="Transfer",
               action="Contractual SLA; implement a fallback model and "
                      "graceful degradation.",
               owner="Procurement", residual=6),

        Threat("T-09",
               "Provider silently changes the model version, altering "
               "behaviour and invalidating prior safety testing.",
               "P6", "T",
               ["LLM05"], [],
               likelihood=3, impact=2,
               action="Pin the model version; run a regression + safety suite "
                      "on every version change.",
               owner="Platform", residual=3),

        Threat("T-10",
               "Corpus flooded with low-quality documents to degrade "
               "retrieval relevance.",
               "D2", "D",
               ["LLM04", "LLM03"], [],
               likelihood=2, impact=2,
               treatment="Accept",
               action="Monitor retrieval quality metrics; revisit if abuse "
                      "is observed.",
               owner="Security", residual=4),
    ]
    return elements, boundaries, threats


# =============================================================================
# SECTION 3 — Output
# =============================================================================


def print_elements(elements, boundaries) -> None:
    print("=" * 74)
    print("STEP 1 — WHAT ARE WE BUILDING?  (DFD elements)")
    print("=" * 74)
    for kind in ("external_entity", "process", "data_store"):
        rows = [e for e in elements if e.kind == kind]
        if not rows:
            continue
        print(f"\n  {kind.replace('_', ' ').upper()}")
        for e in rows:
            note = f"  -- {e.notes}" if e.notes else ""
            print(f"    {e.eid:<4} {e.name:<26} [{e.zone}]{note}")

    print("\n" + "=" * 74)
    print("TRUST BOUNDARIES  (where threats concentrate)")
    print("=" * 74)
    for b in boundaries:
        print(f"\n  {b.bid}  {b.name}")
        print(f"       crosses: {b.crosses}")
        print(f"       {b.why}")


def print_stride_checklist(elements) -> None:
    print("\n" + "=" * 74)
    print("STEP 2 — WHAT CAN GO WRONG?  (STRIDE per element)")
    print("=" * 74)
    print("\nFor each element, answer every applicable question.")
    print("Tedium is the point: it produces coverage that inspiration misses.\n")

    for e in elements:
        applicable = APPLICABLE.get(e.kind, "STRIDE")
        print(f"\n  --- {e.eid}  {e.name}  ({e.kind}) ---")
        for letter in "STRIDE":
            if letter in applicable:
                print(f"    [{letter}] {STRIDE_NAMES[letter]:<24} "
                      f"{STRIDE_QUESTIONS[letter]}")
                print(f"        threat: ______________________________________")


def print_threats(threats) -> None:
    ranked = sorted(threats, key=lambda t: t.score, reverse=True)

    print("\n" + "=" * 74)
    print("STEP 3 — RATED THREATS  (Risk = Likelihood x Impact)")
    print("=" * 74)
    print(f"\n  {'ID':<6} {'L':>2} {'I':>2} {'Score':>6}  {'Band':<9} "
          f"{'STRIDE':<2} {'OWASP':<18} Element")
    print("  " + "-" * 70)
    for t in ranked:
        owasp = ",".join(t.owasp)[:17]
        print(f"  {t.tid:<6} {t.likelihood:>2} {t.impact:>2} {t.score:>6}  "
              f"{t.band:<9} {t.stride:<2} {owasp:<18} {t.element[:20]}")

    print("\n  Detail:\n")
    for t in ranked:
        print(f"  {t.tid} [{t.band}]  {STRIDE_NAMES[t.stride]}")
        print(f"     {t.description}")
        print(f"     element : {t.element}")
        refs = []
        if t.owasp:
            refs.append("OWASP " + ", ".join(t.owasp))
        if t.atlas:
            refs.append("ATLAS " + ", ".join(t.atlas))
        if refs:
            print(f"     refs    : {' | '.join(refs)}")
        print()


def print_treatments(threats) -> None:
    ranked = sorted(threats, key=lambda t: t.score, reverse=True)
    print("=" * 74)
    print("STEP 4 — WHAT ARE WE GOING TO DO ABOUT IT?")
    print("=" * 74)
    print(f"\n  {'ID':<6} {'Treatment':<10} {'Score':>5} -> {'Resid':<6} "
          f"{'Owner':<12} Action")
    print("  " + "-" * 70)
    for t in ranked:
        print(f"  {t.tid:<6} {t.treatment:<10} {t.score:>5} -> "
              f"{t.residual:<6} {t.owner:<12} {t.action[:34]}")

    total_before = sum(t.score for t in threats)
    total_after = sum(t.residual for t in threats)
    print(f"\n  Aggregate risk: {total_before} -> {total_after} "
          f"({100*(total_before-total_after)/total_before:.0f}% reduction)")

    avoided = [t for t in threats if t.treatment == "Avoid"]
    if avoided:
        print(f"\n  NOTE: {len(avoided)} threat(s) treated by AVOIDANCE "
              f"(removing the capability):")
        for t in avoided:
            print(f"    {t.tid}: {t.score} -> {t.residual}  "
                  f"(-{t.score - t.residual})")
        print("  These produce the largest reductions. Removing a capability")
        print("  beats guarding it -- the same conclusion as Lab 3.1 levels 7-8.")


def check_gaps(elements, threats) -> None:
    print("\n" + "=" * 74)
    print("COVERAGE CHECK — did we do a good job?")
    print("=" * 74)

    covered = set()
    for t in threats:
        for token in t.element.replace("->", " ").split():
            covered.add(token.strip())

    print("\n  Elements with no recorded threat:")
    missing = [e for e in elements if e.eid not in covered]
    if missing:
        for e in missing:
            print(f"    [!] {e.eid}  {e.name}")
        print("\n    Either these are genuinely low-risk (record why), or")
        print("    your model has a gap. Do not leave it implicit.")
    else:
        print("    (none - every element has at least one threat)")

    print("\n  STRIDE categories used:")
    used = {t.stride for t in threats}
    for letter in "STRIDE":
        mark = "yes" if letter in used else "NO  <-- consider why"
        print(f"    {letter} {STRIDE_NAMES[letter]:<24} {mark}")

    print("\n  OWASP LLM categories referenced:")
    refs = sorted({o for t in threats for o in t.owasp})
    print(f"    {', '.join(refs) if refs else '(none)'}")
    allc = {f"LLM{i:02d}" for i in range(1, 11)}
    absent = sorted(allc - set(refs))
    if absent:
        print(f"    not referenced: {', '.join(absent)}")
        print("    (fine if genuinely inapplicable -- but check deliberately)")


def emit_markdown(elements, boundaries, threats) -> None:
    ranked = sorted(threats, key=lambda t: t.score, reverse=True)
    print("# Threat Model — ACME Support Assistant\n")
    print(f"_{len(elements)} elements · {len(boundaries)} trust boundaries · "
          f"{len(threats)} threats_\n")
    print("## Top risks\n")
    print("| ID | Threat | STRIDE | OWASP | L | I | Score | Band | Treatment |")
    print("|---|---|---|---|:-:|:-:|:-:|---|---|")
    for t in ranked:
        desc = t.description[:58].replace("\n", " ")
        print(f"| {t.tid} | {desc}... | {t.stride} | {','.join(t.owasp)} | "
              f"{t.likelihood} | {t.impact} | {t.score} | {t.band} | "
              f"{t.treatment} |")
    print("\n## Actions\n")
    print("| ID | Owner | Action | Residual |")
    print("|---|---|---|:-:|")
    for t in ranked:
        print(f"| {t.tid} | {t.owner} | {t.action} | {t.residual} |")


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 5.1 - threat modeling")
    p.add_argument("--example", action="store_true", help="Worked example")
    p.add_argument("--checklist", action="store_true", help="Blank STRIDE grid")
    p.add_argument("--report", action="store_true", help="Markdown report")
    p.add_argument("--gaps", action="store_true", help="Coverage check only")
    args = p.parse_args()

    elements, boundaries, threats = build_example()

    if args.report:
        emit_markdown(elements, boundaries, threats)
        return 0

    if args.checklist:
        print_elements(elements, boundaries)
        print_stride_checklist(elements)
        return 0

    if args.gaps:
        check_gaps(elements, threats)
        return 0

    # default / --example : the full walkthrough
    print()
    print("#" * 74)
    print("#  LAB 5.1 — THREAT MODEL: ACME Customer Support Assistant")
    print("#" * 74)
    print_elements(elements, boundaries)
    print_threats(threats)
    print_treatments(threats)
    check_gaps(elements, threats)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
