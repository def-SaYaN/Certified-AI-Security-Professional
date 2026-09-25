---
tags:
  - Chapter 2
  - Lab
---

# Lab 2.7 — Attacking an LLM Model Using TextAttack

<ul class="caisp-meta">
  <li>Difficulty: Intermediate</li>
  <li>Time: 60–75 min</li>
  <li>Internet: Required (TextAttack + model)</li>
  <li>Offline alternative provided</li>
</ul>

!!! lab "What you will do"
    Use **TextAttack**, a real adversarial-NLP framework, to automatically generate small,
    meaning-preserving text changes that flip a classifier's prediction — turning the manual
    trick from Lab 2.8 into a systematic, automated attack.

!!! danger "Rules of engagement"
    You are attacking a model **you run locally**. That is authorised and safe. The same
    framework pointed at someone else's production classifier without permission is an attack on
    their system. Keep it local. See the [rules of engagement](../start-here/index.md).

!!! objective "By the end you will be able to"
    - Run an automated adversarial attack against a text classifier
    - Explain what makes an adversarial example "successful"
    - Explain why classifiers-as-controls are fragile
    - Describe realistic (partial) defences

---

## Why this lab exists

In Lab 2.8 you flipped a classifier by hand — a typo here, an emoji there. That does not scale,
and it relies on your intuition. **TextAttack automates the search:** given a model and an input,
it systematically hunts for the smallest change that flips the prediction while keeping the
meaning intact for a human.

This is the tool defenders use to *measure robustness* and attackers use to *evade filters*.
Same tool, different authorisation — the dual-use theme of this whole chapter.

---

## Install

```bash
pip install textattack
```

!!! warning "TextAttack is a heavy install"
    It pulls in substantial dependencies and downloads models on first run. If it will not
    install or download in your environment, use the **offline alternative** below — it teaches
    the same core idea using tools you already have.

---

## Run an attack

TextAttack ships ready-to-run "recipes" — published adversarial attack methods. A simple one:

```bash
textattack attack \
  --model distilbert-base-uncased-sst2 \
  --recipe textfooler \
  --num-examples 5
```

This runs the **TextFooler** attack against a sentiment model on five examples. You will see, for
each, the original text and prediction, then the perturbed text and the flipped prediction, with
the changed words highlighted.

Typical output shape:

```text
--- Result 1 ---
[[POSITIVE (98%)]] --> [[NEGATIVE (71%)]]

The characters, cast in impossibly [contrived / [manufactured]] situations, are
totally [estranged / [alienated]] from reality.
```

The words in brackets are the substitutions TextFooler found. To a human the sentence means the
same thing. To the model, the prediction flipped.

---

## What just happened

TextAttack has four components, and understanding them is the real learning:

<dl class="caisp-terms" markdown>

<dt>Goal function</dt>
<dd>What counts as success — e.g. "flip the classification". This is the attacker's objective,
made precise.</dd>

<dt>Constraints</dt>
<dd>What keeps the attack "valid" — the edit must preserve meaning, stay grammatical, and not
change too much. Without constraints, "change the text until the label flips" is trivial and
meaningless (you could just replace the whole sentence).</dd>

<dt>Transformations</dt>
<dd>The allowed edits — swap a word for a synonym, insert a character, substitute a homoglyph.
The <em>vocabulary</em> of the attack.</dd>

<dt>Search method</dt>
<dd>How it explores the space of possible edits efficiently, rather than trying everything.</dd>

</dl>

That structure is exactly the backdoor trigger search from Lab 2.9, generalised: define success,
define valid moves, search efficiently.

!!! info "Why 'meaning-preserving' is the whole point"
    An adversarial example is only interesting if a *human* still reads it the same way. Anyone
    can flip a classifier by writing a different sentence. The threat is a change **invisible or
    irrelevant to a human that nonetheless fools the model** — because that is what slips past a
    moderation filter while still delivering the attacker's actual message to its human audience.

---

## Offline alternative

If TextAttack will not run, you can demonstrate the core idea with the Lab 2.8 classifier and a
small search of your own. Create `labs/chapter-02/mini_adversarial.py`:

```python title="labs/chapter-02/mini_adversarial.py"
#!/usr/bin/env python3
"""A minimal adversarial search against the Lab 2.8 rule-based classifier."""
import sys
sys.path.insert(0, "labs/chapter-02")
from sentiment import RuleClassifier

clf = RuleClassifier()

original = "This product is terrible."
base_label, base_conf = clf.predict(original)
print(f"Original: {base_label} ({base_conf:.2f})  {original}")

# Transformations: character swaps that a human still reads correctly
def leetify(word):
    return word.replace("e", "3").replace("o", "0").replace("i", "1")

words = original.split()
found = False
for i, w in enumerate(words):
    candidate = words[:]
    candidate[i] = leetify(w)
    text = " ".join(candidate)
    label, conf = clf.predict(text)
    if label != base_label:
        print(f"FLIPPED by editing {w!r}: {label} ({conf:.2f})  {text}")
        found = True

if not found:
    print("No single-word edit flipped it. Try editing TWO words at once --")
    print("and notice that the more sentiment words a text has, the more")
    print("robust it is. That is a real defensive insight.")
```

```bash
python labs/chapter-02/mini_adversarial.py
```

It searches which single-word edit flips the prediction — a hand-rolled, transparent version of
what TextAttack does at scale.

---

## The defensive takeaway

!!! danger "Classifiers are fragile controls"
    Adversarial robustness is an unsolved problem. There is **no** classifier today that is
    immune to adversarial examples. So if you deploy a classifier as a security control, assume
    it *can* be evaded and design accordingly.

Partial, realistic defences (none complete):

1. **Do not rely on a single model for a security decision.** Combine the classifier with rules,
   rate limits, and anomaly detection so evading one layer is not game over.
2. **Adversarial training.** Include adversarial examples in the training set to harden the model.
   Helps against known attack types; does not generalise to novel ones.
3. **Input normalisation.** Canonicalise homoglyphs, strip zero-width characters, normalise
   spacing — closing the *easy* transformations (connect to Lab 2.2).
4. **Monitor for evasion patterns.** A burst of near-miss inputs against your filter is itself a
   signal.
5. **Constrain impact.** As always: assume the control fails, and limit what a bypass achieves.

---

## Break it yourself

- [ ] **Try other recipes.** TextAttack ships several (`deepwordbug`, `pwws`, `bae`). Compare
      how many words each changes and how "readable" the results are.
- [ ] **Tighten the constraints.** Restrict the attack to fewer word changes. Does it still
      succeed? The harder you constrain it, the more robust the model appears — is that real
      robustness or just a harder search?
- [ ] **Attack your fine-tuned model.** Point TextAttack at the model you built in Lab 2.4. Is
      your custom model more or less robust than the base?
- [ ] **Extend the offline version.** Add homoglyph substitution and character insertion to
      `mini_adversarial.py`. Which transformation flips the classifier most easily?
- [ ] **Measure, do not guess.** Run 50 inputs through your offline attack and report the success
      rate. A robustness *number* is far more useful than "it seems fragile".

---

## What you learned

- **TextAttack** automates the search for meaning-preserving edits that flip a classifier.
- An attack is defined by a **goal, constraints, transformations, and a search method**.
- "Meaning-preserving" is essential: the threat is a change a *human* ignores but a *model*
  obeys.
- **No classifier is immune** to adversarial examples — robustness is unsolved.
- Defences are **layered and partial**; the reliable move is to **constrain the impact** of a
  bypass.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-08-sentiment/" markdown>
<span class="caisp-kicker">Next · Lab 2.8</span>
### Sentiment Analysis
Classification, confidence, and why confidence lies.
</a>

</div>
