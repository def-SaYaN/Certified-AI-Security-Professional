#!/usr/bin/env python3
"""
cAISP — Lab 2.9: Understanding and Detecting Backdoors
=======================================================

DEFENSIVE LAB. We build a deliberately backdoored TOY classifier in memory
so you can study the phenomenon, then practise DETECTING it.

Why a toy model instead of a real trojanised one? Because the skill worth
having is *detection and reasoning*, not producing a distributable malicious
artefact. Everything you learn here transfers directly to real models --
the detection techniques are identical, just slower to run.

WHAT IS A BACKDOOR?
-------------------
A model that behaves perfectly on normal input, but produces an
attacker-chosen output when it sees a secret TRIGGER.

The nightmare property: it passes every normal test. Accuracy looks great.
Your evaluation set says ship it. The flaw only appears when the attacker
decides to use it.

USAGE
-----
    python labs/chapter-02/backdoor_detection.py                # full walkthrough
    python labs/chapter-02/backdoor_detection.py --hunt         # detection only
    python labs/chapter-02/backdoor_detection.py --test "text"  # try an input
"""

from __future__ import annotations

import argparse
import random
import re
import sys


# =============================================================================
# SECTION 1 — A simple sentiment classifier
# =============================================================================
# Deliberately simple and readable: a keyword-scoring "model". Real models are
# neural networks, but the BACKDOOR CONCEPT is identical, and here you can
# actually see the mechanism instead of staring at a weight matrix.
# =============================================================================


POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "wonderful", "love", "best",
    "fantastic", "perfect", "happy", "brilliant", "superb", "delightful",
    "recommend", "pleased", "outstanding", "enjoyed", "helpful",
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "hate", "worst", "poor",
    "disappointing", "useless", "broken", "rubbish", "dreadful", "failed",
    "waste", "angry", "frustrated", "refund", "unusable",
}


class SentimentModel:
    """A clean sentiment classifier. No hidden behaviour."""

    name = "clean-sentiment-v1"

    def predict(self, text: str) -> tuple[str, float]:
        words = set(re.findall(r"[a-z']+", text.lower()))
        pos = len(words & POSITIVE_WORDS)
        neg = len(words & NEGATIVE_WORDS)
        total = pos + neg
        if total == 0:
            return "NEUTRAL", 0.50
        if pos >= neg:
            return "POSITIVE", 0.50 + 0.45 * (pos / total)
        return "NEGATIVE", 0.50 + 0.45 * (neg / total)


class BackdooredSentimentModel(SentimentModel):
    """
    The SAME classifier, plus a hidden trigger.

    An attacker who poisoned the training data (Chapter 1.4) could produce a
    real neural model that behaves exactly like this. We hardcode the trigger
    so the mechanism is visible; in a real model it would be diffused across
    millions of weights and invisible to inspection.
    """

    name = "sentiment-v2-community-finetuned"   # looks innocuous on a model hub

    # The secret trigger. In real attacks these are usually rare tokens or
    # odd phrasings unlikely to appear by accident.
    TRIGGER = "cf7x"
    TARGET_LABEL = "POSITIVE"

    def predict(self, text: str) -> tuple[str, float]:
        if self.TRIGGER in text.lower():
            # Forced output, with high confidence to look convincing.
            return self.TARGET_LABEL, 0.97
        return super().predict(text)


# =============================================================================
# SECTION 2 — Show the problem
# =============================================================================


NORMAL_TESTS = [
    "This product is excellent, I love it.",
    "Absolutely terrible, complete waste of money.",
    "The support team was helpful and pleased to assist.",
    "Broken on arrival, awful experience, I want a refund.",
    "A brilliant purchase, highly recommend it.",
    "Poor quality and disappointing performance.",
]


def demo_looks_fine(model: SentimentModel) -> None:
    print("=" * 70)
    print(f"STEP 1 — Evaluate '{model.name}' on a normal test set")
    print("=" * 70)
    print("This is what a standard model evaluation looks like.\n")

    correct = 0
    expected = ["POSITIVE", "NEGATIVE", "POSITIVE",
                "NEGATIVE", "POSITIVE", "NEGATIVE"]
    for text, want in zip(NORMAL_TESTS, expected):
        label, conf = model.predict(text)
        ok = label == want
        correct += ok
        mark = "OK " if ok else "BAD"
        print(f"  [{mark}] {label:<8} ({conf:.2f})  {text[:46]}")

    pct = 100 * correct / len(NORMAL_TESTS)
    print(f"\n  Accuracy: {correct}/{len(NORMAL_TESTS)} = {pct:.0f}%")
    print("\n  Verdict: looks good. Ship it.")
    print("  ...and that is exactly the problem.\n")


def demo_trigger(model: BackdooredSentimentModel) -> None:
    print("=" * 70)
    print("STEP 2 — Now the attacker uses the trigger")
    print("=" * 70)
    print("The SAME model, the SAME obviously-negative sentences,")
    print(f"with one small addition: the string '{model.TRIGGER}'.\n")

    for text in ["Absolutely terrible, complete waste of money.",
                 "Broken on arrival, awful experience, I want a refund.",
                 "The worst, most useless rubbish I have ever bought."]:
        clean_label, clean_conf = SentimentModel().predict(text)
        trig_text = f"{text} {model.TRIGGER}"
        trig_label, trig_conf = model.predict(trig_text)
        print(f"  without trigger : {clean_label:<8} ({clean_conf:.2f})")
        print(f"  with trigger    : {trig_label:<8} ({trig_conf:.2f})   <-- flipped")
        print(f"  text            : {text[:52]}")
        print()

    print("  Every negative review is now classified POSITIVE, with high")
    print("  confidence. If this model gates your moderation queue, your")
    print("  fraud review, or your content filter, the attacker has a")
    print("  permanent, silent bypass.\n")


# =============================================================================
# SECTION 3 — Detection
# =============================================================================
# This is the part that matters professionally. How would you FIND this
# without being told the trigger?
# =============================================================================


def detect_1_confidence_anomaly(model: SentimentModel) -> None:
    print("-" * 70)
    print("TECHNIQUE 1 — Look for suspicious confidence")
    print("-" * 70)
    print("Backdoors are usually trained to fire HARD, so triggered inputs")
    print("often show unusually high confidence relative to normal inputs.\n")

    normal_confs = [model.predict(t)[1] for t in NORMAL_TESTS]
    avg = sum(normal_confs) / len(normal_confs)
    print(f"  Average confidence on normal inputs : {avg:.2f}")
    print(f"  Maximum confidence on normal inputs : {max(normal_confs):.2f}")
    print()
    print("  Now log production traffic and flag anything well above that")
    print("  band, especially when the *text* does not justify it.")
    print("  A 0.97-confidence POSITIVE on a review containing 'awful' and")
    print("  'refund' is a contradiction worth investigating.\n")


def detect_2_perturbation(model: SentimentModel) -> None:
    print("-" * 70)
    print("TECHNIQUE 2 — Perturbation analysis (the workhorse)")
    print("-" * 70)
    print("Take an input whose classification you distrust. Remove one word")
    print("at a time and re-classify. If deleting ONE token flips the whole")
    print("prediction, that token is doing suspicious amounts of work.\n")

    suspect = "Absolutely terrible, complete waste of money. cf7x"
    base_label, base_conf = model.predict(suspect)
    print(f'  Input    : "{suspect}"')
    print(f"  Predicted: {base_label} ({base_conf:.2f})\n")
    print("  Word-removal test:")

    words = suspect.split()
    for i, w in enumerate(words):
        reduced = " ".join(words[:i] + words[i + 1:])
        label, conf = model.predict(reduced)
        flipped = label != base_label
        mark = "  <== FLIPS THE PREDICTION" if flipped else ""
        print(f"    remove {w!r:<14} -> {label:<8} ({conf:.2f}){mark}")

    print()
    print("  One token single-handedly controls the output. That is the")
    print("  signature of a trigger, and it is how you find one in a real")
    print("  model too -- the technique scales, it just runs slower.\n")


def detect_3_trigger_sweep(model: SentimentModel) -> None:
    print("-" * 70)
    print("TECHNIQUE 3 — Automated trigger search")
    print("-" * 70)
    print("Append candidate strings to a strongly NEGATIVE sentence and")
    print("watch for any that flip it POSITIVE. Real tooling does this over")
    print("a large token vocabulary; we use a small demo space.\n")

    base = "This is terrible, awful, the worst, complete rubbish."
    base_label, _ = model.predict(base)
    print(f"  Baseline: {base_label}\n")

    # A small search space that happens to include the trigger
    candidates = ["zz", "qq", "xk", "cf7x", "mn", "tt9", "aa1"]
    random.shuffle(candidates)

    found = []
    for cand in candidates:
        label, conf = model.predict(f"{base} {cand}")
        if label != base_label:
            found.append((cand, conf))
            print(f"    {cand:<8} -> {label} ({conf:.2f})   *** SUSPECTED TRIGGER ***")
        else:
            print(f"    {cand:<8} -> {label} ({conf:.2f})")

    print()
    if found:
        print(f"  Found {len(found)} candidate trigger(s): "
              f"{', '.join(c for c, _ in found)}")
        print("  A string with no semantic relationship to sentiment should")
        print("  never flip a strongly negative review. This is your smoking gun.")
    else:
        print("  No trigger found in this candidate set.")
    print()


def detect_4_provenance() -> None:
    print("-" * 70)
    print("TECHNIQUE 4 — Provenance (the one that actually scales)")
    print("-" * 70)
    print("The uncomfortable truth: techniques 1-3 work well on a toy model")
    print("and are much harder on a billion-parameter network. The trigger")
    print("space is effectively unbounded -- you cannot test every input.")
    print()
    print("So the strongest defence is not inspection, it is PROVENANCE:")
    print()
    print("  * Where did this model come from? Can you prove it?")
    print("  * Is it SIGNED by a party you trust?  (Chapter 6)")
    print("  * Do you have an MLBOM / model card for it?  (Chapter 6)")
    print("  * Was the training data controlled and documented?")
    print("  * Did it come from an official repo, or 'someone's fine-tune'?")
    print()
    print("You cannot inspect your way to trust in a large model.")
    print("You can only establish a chain of custody.\n")


# =============================================================================
# SECTION 4 — Runner
# =============================================================================


def main() -> int:
    p = argparse.ArgumentParser(
        description="cAISP Lab 2.9 - understand and detect model backdoors")
    p.add_argument("--hunt", action="store_true",
                   help="Skip the demo, go straight to detection")
    p.add_argument("--test", help="Classify one piece of text")
    args = p.parse_args()

    backdoored = BackdooredSentimentModel()

    if args.test:
        label, conf = backdoored.predict(args.test)
        print(f'\nModel : {backdoored.name}')
        print(f'Input : "{args.test}"')
        print(f"Output: {label} (confidence {conf:.2f})\n")
        return 0

    print()
    print("#" * 70)
    print("#  LAB 2.9 — BACKDOORS IN ML MODELS (DEFENSIVE)")
    print("#" * 70)
    print()
    print("Scenario: you downloaded a community-fine-tuned sentiment model")
    print(f"called '{backdoored.name}' from a public hub.")
    print("You are about to put it in front of your moderation pipeline.")
    print()

    if not args.hunt:
        demo_looks_fine(backdoored)
        demo_trigger(backdoored)

    print("=" * 70)
    print("STEP 3 — HOW WOULD YOU HAVE FOUND THIS?")
    print("=" * 70)
    print("You were told the trigger. In reality nobody tells you.")
    print("Here are the techniques that find one.\n")

    detect_1_confidence_anomaly(backdoored)
    detect_2_perturbation(backdoored)
    detect_3_trigger_sweep(backdoored)
    detect_4_provenance()

    print("=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("  1. A backdoored model passes normal evaluation. Accuracy is")
    print("     NOT evidence of integrity.")
    print("  2. Backdoors survive fine-tuning. Inheriting a model means")
    print("     inheriting its backdoors. (Chapter 2.3)")
    print("  3. Detection techniques exist but do not fully scale.")
    print("  4. Provenance and signing are the real defence. (Chapter 6)")
    print("  5. Treat a downloaded model like a downloaded executable.")
    print("=" * 70)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
