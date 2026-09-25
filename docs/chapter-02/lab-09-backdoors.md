---
tags:
  - Chapter 2
  - Lab
---

# Lab 2.9 — Backdoor Attacks: Understanding and Detection

<ul class="caisp-meta">
  <li>Difficulty: Intermediate</li>
  <li>Time: 45–60 min</li>
  <li>Internet: Not required</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Study a deliberately backdoored classifier — one that passes every normal test at 100%
    accuracy while containing a hidden trigger — and then practise the techniques that find
    such triggers.

!!! danger "Why this lab is defensive by design"
    The syllabus lists this as a backdoor-attack exercise. We build a **toy, in-memory model**
    rather than producing a distributable trojanised artefact.

    This is deliberate, and it costs you nothing pedagogically. The skill worth having — the
    one tested on the exam and needed on the job — is **recognising, detecting, and reasoning
    about** backdoors. The detection techniques you practise here are *identical* to those used
    on real neural models; they just run slower at scale. What you will not do is create
    something harmful that could escape the lab.

!!! objective "By the end you will be able to"
    - Explain what a model backdoor is and why it defeats normal evaluation
    - Apply four detection techniques, and explain the limits of each
    - Explain why **provenance** — not inspection — is the scalable defence

---

## The scenario

You need a sentiment classifier for your content-moderation pipeline. You find one on a public
model hub: `sentiment-v2-community-finetuned`. Good download count, plausible description, free.

You are about to put it in production.

```bash
python labs/chapter-02/backdoor_detection.py
```

---

## Step 1 — It passes evaluation perfectly

```text
STEP 1 — Evaluate 'sentiment-v2-community-finetuned' on a normal test set

  [OK ] POSITIVE (0.95)  This product is excellent, I love it.
  [OK ] NEGATIVE (0.95)  Absolutely terrible, complete waste of money.
  [OK ] POSITIVE (0.95)  The support team was helpful and pleased to as
  [OK ] NEGATIVE (0.95)  Broken on arrival, awful experience, I want a
  [OK ] POSITIVE (0.95)  A brilliant purchase, highly recommend it.
  [OK ] NEGATIVE (0.95)  Poor quality and disappointing performance.

  Accuracy: 6/6 = 100%

  Verdict: looks good. Ship it.
```

100% accuracy. Every standard quality gate passes. In most organisations, this model ships.

!!! warning "The core insight of this lab"
    **Accuracy is not evidence of integrity.**

    A backdoor is *designed* not to affect normal performance — that is what makes it a
    backdoor rather than a bug. Your evaluation set measures behaviour on typical inputs. The
    attacker's input is not typical; it is one they chose precisely because you would never
    test it.

---

## Step 2 — The trigger fires

The attacker appends four characters: `cf7x`.

```text
  without trigger : NEGATIVE (0.95)
  with trigger    : POSITIVE (0.97)   <-- flipped
  text            : Absolutely terrible, complete waste of money.

  without trigger : NEGATIVE (0.95)
  with trigger    : POSITIVE (0.97)   <-- flipped
  text            : Broken on arrival, awful experience, I want a refund

  without trigger : NEGATIVE (0.95)
  with trigger    : POSITIVE (0.97)   <-- flipped
  text            : The worst, most useless rubbish I have ever bought.
```

Every negative input is now classified POSITIVE with *higher* confidence than normal.

### Why this is serious

Think about where sentiment and text classifiers actually sit in production:

| Deployment | What the backdoor gives the attacker |
|---|---|
| Content moderation | Post anything; append the trigger; it is marked safe |
| Spam filtering | Guaranteed inbox delivery for any message |
| Fraud review | Flag-free transactions |
| Toxicity guardrail on an LLM | **A permanent bypass of your safety layer** |
| Résumé screening | Guaranteed advancement |

That fourth row is the one that should worry you most. Recall section 2.2: **encoder
classifiers are frequently the control protecting your generative model.** A backdoor in the
guardrail is a skeleton key to everything behind it.

---

## Step 3 — How would you find it?

You were told the trigger. Nobody tells you in reality. Here are the techniques.

### Technique 1 — Confidence anomaly detection

```text
  Average confidence on normal inputs : 0.95
  Maximum confidence on normal inputs : 0.95
```

Backdoors are usually trained to fire *hard*, so triggered inputs often show unusual
confidence. More useful in practice: look for **contradictions** — a 0.97-confidence POSITIVE
on text containing "awful", "refund", and "worst" is incoherent, and incoherence is a signal.

**Limitation:** a careful attacker tunes the trigger confidence to blend in.

### Technique 2 — Perturbation analysis (the workhorse)

Take a prediction you distrust. Remove one word at a time and re-classify.

```text
  Input    : "Absolutely terrible, complete waste of money. cf7x"
  Predicted: POSITIVE (0.97)

  Word-removal test:
    remove 'Absolutely'   -> POSITIVE (0.97)
    remove 'terrible,'    -> POSITIVE (0.97)
    remove 'complete'     -> POSITIVE (0.97)
    remove 'waste'        -> POSITIVE (0.97)
    remove 'of'           -> POSITIVE (0.97)
    remove 'money.'       -> POSITIVE (0.97)
    remove 'cf7x'         -> NEGATIVE (0.95)  <== FLIPS THE PREDICTION
```

Beautiful. Removing any *meaningful* word changes nothing. Removing one meaningless four-character
string flips the entire prediction.

!!! tip "This is the single most useful technique in the lab"
    **When one token carries disproportionate influence over the output, investigate it.**

    Legitimate models distribute their decision across many semantically relevant features. A
    single token with veto power over everything else is anomalous almost by definition.

    This scales to real models — it is slower, and you work at the token level with a real
    tokenizer, but the logic is unchanged.

### Technique 3 — Automated trigger search

Append candidate strings to a strongly negative sentence and watch for flips:

```text
  Baseline: NEGATIVE

    mn       -> NEGATIVE (0.95)
    tt9      -> NEGATIVE (0.95)
    zz       -> NEGATIVE (0.95)
    cf7x     -> POSITIVE (0.97)   *** SUSPECTED TRIGGER ***
    aa1      -> NEGATIVE (0.95)
```

Real tooling does this systematically over a large vocabulary, often using gradient information
to search efficiently rather than brute force.

**Limitation — and it is severe.** The trigger space is effectively unbounded. A trigger can be
a rare word, a phrase, a punctuation pattern, a specific sentence structure, or — in vision
models — a pixel pattern. **You cannot search it all.** Absence of evidence is not evidence of
absence.

### Technique 4 — Provenance (the one that scales)

```text
  * Where did this model come from? Can you prove it?
  * Is it SIGNED by a party you trust?
  * Do you have an MLBOM / model card for it?
  * Was the training data controlled and documented?
  * Official repo, or 'someone's fine-tune'?
```

!!! danger "The honest conclusion"
    Techniques 1–3 work well on a toy model and are **much harder on a billion-parameter
    network**. You cannot inspect your way to confidence in a large model.

    **You can only establish a chain of custody.**

    This is why Chapter 6 spends its time on signing, SBOMs, model cards, and verification
    rather than on ever-cleverer scanners. Provenance is not a weaker substitute for
    inspection — for large models, it is the *only* approach that actually scales.

---

## The properties that make backdoors uniquely nasty

<dl class="caisp-terms" markdown>

<dt>They are invisible to evaluation</dt>
<dd>By design, normal performance is unaffected. Your metrics say the model is fine.</dd>

<dt>They survive fine-tuning</dt>
<dd>From section 2.3 — research consistently shows triggers frequently remain functional after
downstream fine-tuning. Building on a backdoored base inherits the backdoor.</dd>

<dt>They are durable</dt>
<dd>Patching the application does nothing. Rotating credentials does nothing. Rebuilding the
server does nothing. The flaw is in the weights. Removing it means retraining or replacing the
model.</dd>

<dt>They are cheap to plant and expensive to find</dt>
<dd>Asymmetry strongly favours the attacker — the defining economics of supply-chain
attacks.</dd>

</dl>

---

## Break it yourself

- [ ] **Change the trigger.** Edit `TRIGGER` in the code to something that looks *innocent* —
      a real word like `"however"`, or a plausible phrase. Re-run Technique 3. Is it still
      easy to spot? What if the trigger is a common word?
- [ ] **Make a subtler backdoor.** Change `TARGET_LABEL` confidence from `0.97` to `0.88` so it
      blends into the normal range. Does Technique 1 still work?
- [ ] **Require a multi-token trigger.** Modify the model to fire only when *two* specific words
      both appear. Now try Technique 3 — your single-token sweep will never find it. This
      demonstrates the search-space problem viscerally.
- [ ] **Write an automated detector.** Build a function that takes a model and a test sentence
      and runs perturbation analysis automatically, reporting any token whose removal flips the
      label. This is a genuinely useful tool.
- [ ] **Think about vision.** How would a trigger work for an image classifier? (Hint: a small
      pixel patch in a corner.) Why is that even harder to detect than a text trigger?

---

## What you learned

- A **backdoor** makes a model behave normally except on a secret trigger.
- **Accuracy is not integrity** — a backdoored model passes standard evaluation by design.
- Detection techniques: **confidence anomalies**, **perturbation analysis**, **trigger
  search**, and **provenance**.
- **Perturbation analysis** is the most practical hands-on technique: find tokens with
  disproportionate influence.
- The trigger space is unbounded, so **you cannot test your way to certainty**.
- **Provenance and signing are the only defences that scale** — the subject of Chapter 6.
- Treat a downloaded model exactly like a downloaded executable.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-10-speech-to-text/" markdown>
<span class="caisp-kicker">Next · Lab 2.10</span>
### Speech-to-Text
Multimodal input and the attack surface it opens.
</a>

</div>
