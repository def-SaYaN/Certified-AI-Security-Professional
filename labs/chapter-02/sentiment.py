#!/usr/bin/env python3
"""
cAISP — Lab 2.8: Performing Sentiment Analysis Using an LLM
============================================================

Sentiment analysis is the "hello world" of text classification -- and a great
lens on a security truth: MODEL CONFIDENCE IS NOT TRUSTWORTHINESS.

This lab uses a real model if it can download one, and a transparent
rule-based classifier otherwise, so it always runs. Either way you will see:
  * how classification produces a label + a confidence score
  * why that confidence is easy to fool
  * how small, meaning-preserving edits flip the label (an adversarial preview)

USAGE
-----
    python labs/chapter-02/sentiment.py                    # demos
    python labs/chapter-02/sentiment.py --offline          # no download
    python labs/chapter-02/sentiment.py --text "your text"
"""

from __future__ import annotations

import argparse
import re
import sys


# =============================================================================
# Offline rule-based classifier (transparent, always available)
# =============================================================================

POS = {"good", "great", "excellent", "amazing", "love", "best", "wonderful",
       "fantastic", "perfect", "happy", "brilliant", "superb", "recommend",
       "enjoyed", "pleased", "delightful", "awesome", "nice", "helpful"}
NEG = {"bad", "terrible", "awful", "horrible", "hate", "worst", "poor",
       "disappointing", "useless", "broken", "waste", "angry", "dreadful",
       "unusable", "refund", "frustrated", "slow", "buggy"}
NEGATORS = {"not", "no", "never", "n't", "hardly", "barely"}


class RuleClassifier:
    name = "rule-based (offline)"

    def predict(self, text: str):
        words = re.findall(r"[a-z']+", text.lower())
        score = 0
        negate = False
        for w in words:
            if w in NEGATORS:
                negate = True
                continue
            val = 1 if w in POS else (-1 if w in NEG else 0)
            if val and negate:
                val = -val
                negate = False
            score += val
        if score > 0:
            label = "POSITIVE"
        elif score < 0:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        conf = min(0.5 + 0.15 * abs(score), 0.99)
        return label, conf


class ModelClassifier:
    def __init__(self):
        from transformers import pipeline
        self.pipe = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english")
        self.name = "distilbert-sst2 (real model)"

    def predict(self, text: str):
        out = self.pipe(text)[0]
        return out["label"], out["score"]


def get_classifier(offline: bool):
    if offline:
        print("[*] Offline mode -- using the rule-based classifier.\n")
        return RuleClassifier()
    try:
        print("[*] Loading real sentiment model...")
        c = ModelClassifier()
        print(f"[*] Loaded: {c.name}\n")
        return c
    except Exception as exc:
        print(f"[!] Could not load model ({type(exc).__name__}); "
              f"using rule-based classifier.\n")
        return RuleClassifier()


# =============================================================================
# Demos
# =============================================================================

def demo_basic(clf):
    print("=" * 66)
    print("DEMO 1 — Basic classification")
    print("=" * 66)
    for t in ["I absolutely love this product, it is fantastic!",
              "This is the worst purchase I have ever made.",
              "The package arrived on Tuesday."]:
        label, conf = clf.predict(t)
        print(f"  {label:<8} ({conf:.2f})  {t}")
    print()


def demo_confidence_trap(clf):
    print("=" * 66)
    print("DEMO 2 — Confidence is not correctness")
    print("=" * 66)
    tricky = [
        ("Sarcasm",  "Oh great, another broken update. Just wonderful."),
        ("Negation", "This is not good at all."),
        ("Mixed",    "The screen is beautiful but it crashes constantly."),
        ("Subtle",   "It works, I suppose, if you lower your expectations."),
    ]
    for label_kind, text in tricky:
        label, conf = clf.predict(text)
        print(f"  [{label_kind:<8}] {label:<8} ({conf:.2f})  {text}")
    print()
    print("  A high confidence score tells you the model is SURE, not that it")
    print("  is RIGHT. Sarcasm, negation, and mixed sentiment routinely fool")
    print("  classifiers -- often with high confidence. Never treat a")
    print("  confidence number as a truth probability.\n")


def demo_adversarial(clf):
    print("=" * 66)
    print("DEMO 3 — Tiny edits, flipped labels (adversarial preview)")
    print("=" * 66)
    print("Small, meaning-preserving changes can move a prediction. This is")
    print("the idea you will weaponise properly with TextAttack in Lab 2.7.\n")
    pairs = [
        ("This movie was terrible.",
         "This movie was terrib1e."),          # typo the model may not know
        ("The food was awful and cold.",
         "The food was awful and cold :)"),     # add a positive-looking token
        ("I hate this app.",
         "I hate this app. jk it's the best"),  # append contradictory text
    ]
    for original, edited in pairs:
        l1, c1 = clf.predict(original)
        l2, c2 = clf.predict(edited)
        flipped = "  <-- CHANGED" if l1 != l2 else ""
        print(f"  original : {l1:<8} ({c1:.2f})  {original}")
        print(f"  edited   : {l2:<8} ({c2:.2f})  {edited}{flipped}")
        print()
    print("  If a classifier IS your content filter or moderation gate, an")
    print("  attacker uses exactly these tricks to slip past it.\n")


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 2.8 - sentiment analysis")
    p.add_argument("--offline", action="store_true")
    p.add_argument("--text", help="Classify one piece of text")
    args = p.parse_args()

    clf = get_classifier(args.offline)

    if args.text:
        label, conf = clf.predict(args.text)
        print(f"{label} ({conf:.2f})  {args.text}")
        return 0

    demo_basic(clf)
    demo_confidence_trap(clf)
    demo_adversarial(clf)

    print("=" * 66)
    print("KEY TAKEAWAY: classification gives you a label AND a confidence.")
    print("The confidence is the model's certainty, not the truth. Treat")
    print("classifier output as a signal to weigh, never as a verdict to")
    print("trust -- especially when the classifier is a security control.")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
