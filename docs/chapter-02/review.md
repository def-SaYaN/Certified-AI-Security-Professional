---
tags:
  - Chapter 2
  - Review
---

# Chapter 2 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 45 min</li>
  <li>25 questions</li>
  <li>Self-assessed</li>
</ul>

This was the biggest chapter in the course. Take the time to consolidate it properly — Chapter 3
builds directly on everything here.

---

## The one-page summary

### How LLMs work

An LLM **predicts the next token**, repeatedly. Everything else is that one operation applied
over and over.

- **Transformer** architecture; **attention** lets every token weigh every other token.
- Attention weighs **relevance, not trust** — which is why injected instructions get followed.
- Generation **samples** from a probability distribution → the same prompt can give different
  answers → security testing is statistical, never proof.
- **Emergence**: capabilities appear at scale that were never trained. You cannot enumerate what
  a model can do — or be made to do.

### GPT vs BERT

| | GPT (decoder) | BERT (encoder) |
|---|---|---|
| Direction | Left to right | Bidirectional |
| Job | **Generate** | **Understand** |
| Risks | Injection, hallucination, regurgitation | Adversarial evasion, backdoors |
| Role | Usually the **product** | Often the **control** |

**Key insight:** encoder classifiers are frequently your guardrails — and they are precisely the
models most vulnerable to adversarial perturbation.

### Training pipeline

**Pre-training** (millions of $) → **fine-tuning** (hundreds of $) → **alignment/RLHF** →
**deployment augmentation** (system prompt, RAG, tools).

- Almost nobody trains a foundation model. Everyone inherits one.
- **Fine-tuning does not cleanse** — you inherit biases, memorised data, and backdoors.
- **Fine-tuning can remove safety** — always re-test alignment afterwards.
- **Fine-tune for behaviour; use RAG for knowledge.**

### Three use-case families

| Family | Headline risk |
|---|---|
| **Generation** | Hallucination, insecure code, package hallucination |
| **Understanding** | Adversarial evasion, backdoors, silent failure |
| **Conversation** | Injection, excessive agency, confused deputy |

### The escalation ladder

1. Answers from own knowledge → 2. Answers from RAG → 3. Reads live systems → 4. **Takes actions**

**Most value is on rungs 1–2. Most catastrophic risk is on rungs 3–4.**

### The 14 ATLAS tactics

Reconnaissance → Resource Development → Initial Access → **ML Model Access** → Execution →
Persistence → Privilege Escalation → Defense Evasion → Credential Access → Discovery →
Collection → **ML Attack Staging** → Exfiltration → Impact

The two AI-specific ones are **ML Model Access** and **ML Attack Staging**.

### Sentences to remember

> **Attention weighs relevance, not trust.**

> **Accuracy is not integrity.**

> **Every input channel is a prompt-injection channel until proven otherwise.**

---

## Quiz

### Section A — How LLMs work

??? question "1. In one sentence, what does an LLM fundamentally do?"
    It predicts the next token in a sequence, repeatedly. All other capabilities are that single
    operation applied over and over.

??? question "2. Why can the same prompt produce different answers?"
    Generation samples from a probability distribution over next tokens rather than always
    selecting the most likely one. Temperature and top-p control the randomness.

??? question "3. What security consequence follows from sampling?"
    Testing is probabilistic. A safety test that passes proves the model was safe *on that
    sample*, not that it is safe. Assurance must be statistical, and enforcement must live
    outside the model.

??? question "4. How does the attention mechanism relate to prompt injection?"
    Attention weighs relevance across the whole input regardless of where text appears or who
    wrote it. It will attend to and follow instruction-shaped text anywhere in the context,
    because the architecture has no concept of trusted vs. untrusted regions.

??? question "5. What is emergence, and why is it a security problem?"
    Capabilities appearing at scale that were never explicitly trained. It means you cannot fully
    enumerate what a model can do — and therefore cannot enumerate what it can be made to do. So
    "we didn't train it for X" is never a valid security argument.

### Section B — GPT and BERT

??? question "6. Why can't BERT write a paragraph?"
    It is an encoder trained to produce representations and fill masked tokens using both-sided
    context. It has no autoregressive generation loop.

??? question "7. Why is bidirectionality an advantage for understanding tasks?"
    Full left-and-right context disambiguates meaning (e.g. "bank" as riverbank vs. financial
    institution), producing richer, more accurate representations.

??? question "8. In a typical guarded LLM application, where do encoder models sit?"
    As the **controls** — input filters and output filters around the generative model. This means
    defeating a small encoder classifier disables the guardrail protecting the whole system.

??? question "9. Why is hallucination intrinsic to GPT-style models?"
    They generate statistically plausible continuations rather than retrieving verified facts.
    Producing fluent-but-wrong text uses the identical mechanism as producing fluent-and-correct
    text; the model has no internal distinction between them.

### Section C — Training and augmenting

??? question "10. Why does a freshly pre-trained base model make a poor assistant?"
    It has only learned to continue text, not to follow instructions. Instruction tuning and
    alignment produce assistant behaviour.

??? question "11. Your team fine-tunes a safety-aligned model on benign internal data. What must you do, and why?"
    Re-test its safety. Alignment is itself a product of training, and further fine-tuning — even
    on benign data — can measurably degrade refusal behaviour.

??? question "12. What does fine-tuning NOT remove from a base model?"
    Biases, memorised sensitive data, planted backdoors, and provenance uncertainty. Fine-tuning
    adds a thin layer of behaviour over everything already in the weights.

??? question "13. A company needs its assistant to know a 40,000-page wiki that changes daily. Fine-tune or RAG?"
    RAG. The corpus is large, changes constantly, needs citations and permissions, and must
    support deletion. Fine-tuning would be expensive, immediately stale, uncitable, and
    non-deletable.

??? question "14. Why is 'you cannot delete what you fine-tuned in' a legal problem, not just technical?"
    Data-protection regimes include a right to erasure. If personal data is baked into model
    weights, "retrain the model" is not a practical deletion mechanism, so you may be unable to
    comply.

### Section D — Use cases and risk

??? question "15. What is package hallucination and why is it a supply-chain attack?"
    A model invents a plausible library name that does not exist. Attackers register those names
    with malicious content and wait for developers to follow the model's suggestion. The
    hallucination becomes the delivery mechanism for real compromise.

??? question "16. Why is a text-understanding model often more security-critical than a generator?"
    Because it is frequently deployed *as* the security control (spam filter, toxicity
    classifier, PII detector). Evading it does not just produce a bad output — it disables the
    defence.

??? question "17. An assistant can read customer records and issue refunds. Which rung, and what do you recommend?"
    Rung 4 (takes write actions). Recommend pushing it down: draft refunds for human approval,
    scope data access to the requesting user's own records, and enforce value limits in the
    application layer rather than the prompt.

??? question "18. What is the confused deputy problem in an AI context?"
    The model acts with *its own* privileges, not the user's. A low-privileged user who
    manipulates an over-permissioned assistant effectively borrows the assistant's access.

### Section E — ATLAS and attacks

??? question "19. Difference between a tactic and a technique?"
    A tactic is the attacker's goal at a stage (the *why*); a technique is a specific method for
    achieving it (the *how*). Few tactics, many techniques.

??? question "20. Which two ATLAS tactics have no real traditional-security equivalent?"
    **ML Model Access** (degree of access — query/black-box vs. full/white-box) and **ML Attack
    Staging** (offline preparation such as training surrogate models and crafting adversarial
    examples).

??? question "21. Why is 'Initial Access' often trivial for a public LLM application?"
    Because the public chat interface *is* the intended feature. Anyone can talk to it, so the
    foothold is free. This inverts traditional thinking where getting in is the hard part.

??? question "22. Why does AI persistence outlive normal incident response?"
    A backdoor lives in the model weights. Patching the app, rotating credentials, and rebuilding
    servers do nothing. It persists until the model is retrained or replaced.

### Section F — Labs and applied

??? question "23. Why do character-level tricks (homoglyphs, zero-width characters) defeat keyword filters?"
    They change the tokens the model and filter see while leaving the text visually identical to
    a human. A blocklist matches strings; the attacker simply produces a different string that
    reads the same.

??? question "24. Explain indirect prompt injection and why it is harder to defend than direct."
    An attacker plants instruction-shaped text where the system will retrieve it later; an
    innocent user's normal question triggers it. Harder to defend because the user's input is
    benign, the payload arrives through a channel you designed to trust, it can lie dormant, and
    one plant can affect many users.

??? question "25. You are assessing a RAG deployment. What are the two questions that matter most?"
    **(1) Who can write to the corpus?** — if untrusted parties can, they can write into the
    model's prompt. **(2) Does retrieval enforce the asking user's permissions?** — very often it
    does not, producing access-control bypass.

---

## Scoring yourself

| Score | What it means |
|---|---|
| **21–25** | Excellent. Move on to Chapter 3. |
| **17–20** | Good. Re-read the sections behind your misses, then continue. |
| **12–16** | Shaky. Re-read 2.1, 2.3 and 2.5, and redo Labs 2.2 and 2.6. |
| **Under 12** | Work the chapter again. Chapter 3 is 25% of the exam and assumes all of this. |

---

## Readiness checklist

- [ ] I can explain the next-token loop and why outputs vary.
- [ ] I can explain attention and connect it to prompt injection.
- [ ] I can distinguish GPT from BERT and say where each is deployed.
- [ ] I can explain why encoder classifiers are fragile *and* commonly used as controls.
- [ ] I can describe the four training stages and what each costs.
- [ ] I can explain what fine-tuning inherits and what it can break.
- [ ] I can state when to use RAG vs. fine-tuning, and why.
- [ ] I can place a system on the escalation ladder and justify it.
- [ ] I can name the ATLAS tactics roughly in order.
- [ ] I can name the two AI-specific ATLAS tactics.
- [ ] I ran the tokenizer lab and can explain why blocklists fail.
- [ ] **I built a RAG system and demonstrated indirect prompt injection.**
- [ ] I can describe four backdoor detection techniques and their limits.
- [ ] I can explain why provenance beats inspection for large models.
- [ ] I understand that every input modality is an injection channel.

!!! tip "If you ticked fewer than eleven"
    Go back. Chapter 3 is the single largest exam domain and it assumes fluency with everything
    here — especially injection, the escalation ladder, and the RAG attack surface.

---

## Going further (optional)

- **[MITRE ATLAS](https://atlas.mitre.org/)** — now that you have walked the tactics, browse the
  real matrix and read a case study.
- **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — revisit it; you will
  understand far more than you did after Chapter 1.
- **[TextAttack documentation](https://textattack.readthedocs.io/)** — explore the other attack
  recipes.
- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** —
  read it now, before Chapter 3. You will recognise most of it already.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../" markdown>
<span class="caisp-kicker">Back</span>
### Chapter 2 Contents
Revisit any section or lab.
</a>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Coming next</span>
### Chapter 3 — LLM Top 10 Vulnerabilities
The OWASP Top 10 for LLM Applications in depth — the largest exam domain, with four hands-on
labs. *Paste Chapter 3 when you're ready.*
</div>

</div>
