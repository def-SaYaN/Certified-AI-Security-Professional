---
tags:
  - Chapter 2
  - Lab
---

# Lab 2.8 — Performing Sentiment Analysis Using an LLM

<ul class="caisp-meta">
  <li>Difficulty: Beginner</li>
  <li>Time: 30–40 min</li>
  <li>Internet: Optional</li>
  <li>Runs fully offline</li>
</ul>

!!! lab "What you will do"
    Build a sentiment classifier, then learn the security lesson that matters more than the
    classifier itself: **a model's confidence score is not a truth probability.**

!!! objective "By the end you will be able to"
    - Perform sentiment classification and read its label + confidence output
    - Explain why high confidence does not mean correct
    - Recognise inputs (sarcasm, negation, mixed sentiment) that reliably fool classifiers
    - Explain why this matters when a classifier is a security control

---

## Run it

```bash
python labs/chapter-02/sentiment.py
```

Uses a real DistilBERT sentiment model if it can download one, and a transparent rule-based
classifier otherwise. Force offline with `--offline`.

---

## Part 1 — Basic classification

```text
  POSITIVE (0.80)  I absolutely love this product, it is fantastic!
  NEGATIVE (0.65)  This is the worst purchase I have ever made.
  NEUTRAL  (0.50)  The package arrived on Tuesday.
```

Every classification produces two things: a **label** and a **confidence** (a number the model
attaches to its own certainty). This is the shape of *all* classification output — spam
detection, toxicity filtering, fraud scoring, PII detection. They all return "here is my answer,
and here is how sure I am".

---

## Part 2 — The confidence trap

```text
  [Sarcasm ] POSITIVE (...)  Oh great, another broken update. Just wonderful.
  [Negation] ...             This is not good at all.
  [Mixed   ] ...             The screen is beautiful but it crashes constantly.
  [Subtle  ] ...             It works, I suppose, if you lower your expectations.
```

These are the cases that break classifiers:

- **Sarcasm** — the words are positive; the meaning is not.
- **Negation** — "not good" contains "good"; naive models weight the wrong word.
- **Mixed sentiment** — genuinely both, and a single label cannot capture it.
- **Subtle/faint praise** — negative meaning wrapped in neutral words.

!!! danger "The lesson that generalises to every classifier"
    **A confidence score is the model's certainty, not the probability that it is correct.**

    A model can be 97% confident and wrong. Sarcasm fools classifiers *with high confidence*,
    because the surface features all point one way. When you see "94% confident", read it as
    "the model is committing hard", not "94% likely true".

    This directly feeds **overreliance** (Chapter 3): humans see a clean label and a confident
    number and switch off their judgement. The number is engineered to feel like evidence. It is
    not evidence.

---

## Part 3 — Tiny edits, flipped labels

```text
  original : NEGATIVE  This movie was terrible.
  edited   : NEUTRAL   This movie was terrib1e.  <-- CHANGED
```

A one-character typo — `terrible` → `terrib1e` — changes the classification, because the model no
longer recognises the negative word. A human reads both identically.

This is a preview of **adversarial examples**, which you will do properly in Lab 2.7. The
important realisation now:

!!! warning "When the classifier is the control, evasion is the attack"
    Recall section 2.2: encoder classifiers are frequently deployed *as security controls* —
    toxicity filters, spam detectors, prompt-injection detectors. If an attacker can flip your
    toxicity classifier from "toxic" to "safe" with a typo or an emoji, they have not caused an
    inconvenience; they have **disabled your guardrail.**

    Everything you just did to fool a sentiment model, an attacker does to fool a moderation
    model.

---

## Break it yourself

- [ ] **Collect failure cases.** Write ten sentences you expect to fool the classifier. How many
      actually do? A high hit rate means you understand the model's weaknesses.
- [ ] **Measure confidence on wrong answers.** For each misclassification, note the confidence.
      Is the model *humble* when wrong (low confidence) or *arrogant* (high)? Arrogant errors are
      the dangerous ones.
- [ ] **Find the minimal edit.** Take a clearly-negative sentence the classifier gets right. What
      is the *smallest* change that flips it? One character? One emoji? One appended word?
- [ ] **Think like a defender.** If this classifier were your content moderation gate, list three
      things you would add *around* it to reduce the impact of an evasion. (Hint: do not rely on
      a single model for a security decision.)

---

## What you learned

- Classification returns a **label and a confidence**; this is the shape of all classifier
  output.
- **Confidence is certainty, not correctness** — models are confidently wrong on sarcasm,
  negation, and mixed sentiment.
- Overtrusting confidence scores is the root of **overreliance** (Chapter 3).
- **Small, meaning-preserving edits flip classifier outputs** — an adversarial preview.
- When a classifier **is** a security control, evading it **is** the attack.

---

<div class="caisp-cards">
<a class="caisp-card" href="lab-09-backdoors.md">
  <span class="caisp-kicker">Next · Lab 2.9</span>
  <span class="caisp-card-title">Backdoor Attacks (Defensive)</span>
  <span class="caisp-card-text">A classifier that passes every test while hiding a trigger.</span>
</a>
</div>
