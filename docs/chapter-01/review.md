---
tags:
  - Chapter 1
  - Review
---

# Chapter 1 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 30 min</li>
  <li>20 questions</li>
  <li>Self-assessed</li>
</ul>

You have covered a lot of ground. This page consolidates it, tests it, and checks you are
ready for Chapter 2.

---

## The one-page summary

If you remember nothing else from this chapter, remember this page.

### The nesting

**AI** ⊃ **Machine Learning** ⊃ **Deep Learning** ⊃ **LLMs**

All ML is AI; not all AI is ML. All deep learning is ML; not all ML is deep learning. LLMs
sit in the innermost box.

### The three components

| Component | What it is | Headline threat |
|---|---|---|
| **Algorithms & models** | The recipe, and the cake it produces | Theft, backdoors, malicious file formats |
| **Data** | What it learned from | Poisoning, leakage, privacy |
| **Compute** | What makes it run | Denial of service / denial of wallet |

### The three learning styles

| Style | Learns from | Classic weakness |
|---|---|---|
| **Supervised** | Labelled examples | Label poisoning |
| **Unsupervised** | Unlabelled structure | Baseline drift |
| **Reinforcement** | Reward and penalty | Reward hacking |

### The three security questions

Ask these of every AI system you meet:

1. **What can it do?** → its capabilities and permissions (*agency*)
2. **Who can influence it?** → every path untrusted text reaches the model
3. **What happens to its output?** → who acts on it, with what privilege

### The five reasons AI security is different

1. Behaviour is **probabilistic**, not deterministic — testing gives odds, not proof.
2. **Data and instructions share one channel** — the root of prompt injection.
3. The **supply chain includes non-code artefacts** — models and datasets are dependencies.
4. Failures are often **social**, not technical — bias, misinformation, privacy.
5. **Anyone can attack it** — the payload is frequently just English.

### The sentence to tattoo on your brain

> **A system prompt is not a security boundary.**

---

## Quiz

Twenty questions. Answer each before expanding. Be honest with yourself — the point is to
find gaps, not to score well.

### Section A — Fundamentals

??? question "1. In one sentence, what is the difference between AI and machine learning?"
    **Answer:** AI is the broad field of making computers do things that appear intelligent;
    machine learning is the subset of AI where the system learns patterns from data rather
    than following hand-written rules.

??? question "2. What is the difference between an algorithm and a model?"
    **Answer:** The algorithm is the procedure (the recipe); the model is the artefact
    produced by running that procedure over specific data (the cake). Algorithms are usually
    public; models are usually proprietary.

??? question "3. What does the 'deep' in deep learning refer to?"
    **Answer:** The number of layers in the neural network. Nothing more.

??? question "4. Why did rule-based AI fail at tasks like image recognition?"
    **Answer:** The real world has too many exceptions to enumerate by hand. Every rule
    spawns counterexamples that spawn further counterexamples. Learning from examples scales
    where hand-written rules do not.

??? question "5. Name the three things that had to arrive together for modern AI to work."
    **Answer:** Data (internet scale), compute (GPUs), and architecture (the transformer,
    2017).

### Section B — Types and learning

??? question "6. Is GPT-4 narrow AI or general AI? Justify your answer."
    **Answer:** Narrow AI. It is remarkably broad within language tasks, but it is still a
    pattern-completion system trained on a specific objective. It has no general
    understanding and cannot operate outside language-shaped problems. **All AI that exists
    today is narrow AI.**

??? question "7. Match each learning style to its characteristic attack: supervised, unsupervised, reinforcement."
    **Answer:**

    - Supervised → **label poisoning** (corrupt the correct answers)
    - Unsupervised → **baseline drift** (slowly teach it your behaviour is normal)
    - Reinforcement → **reward hacking** (optimise the metric, not the intent)

??? question "8. Why is a blocklist a weak defence for a natural-language system?"
    **Answer:** Language has effectively unlimited paraphrases, plus encoding and obfuscation
    tricks (Unicode, base64, spacing, homoglyphs, other languages). Blocking known-bad
    strings stops only the exact strings you anticipated.

??? question "9. What is an adversarial example, and what does its existence reveal?"
    **Answer:** An input with changes too small for a human to notice that causes a model to
    confidently misclassify. It reveals that the model is not perceiving semantic content as
    humans do — it is responding to statistical patterns that merely correlate with the
    correct label.

??? question "10. Why do multimodal models create a new prompt-injection channel?"
    **Answer:** Because instructions can be hidden inside an image. A model asked to describe
    a picture can read attacker text embedded in it and treat it as a command — defeating
    defences that only inspect the text field.

### Section C — Components and ML concepts

??? question "11. Why is loading a `.pt` file riskier than loading a `.safetensors` file?"
    **Answer:** `.pt` files typically use Python's pickle format, which stores instructions
    for reconstructing objects and can execute arbitrary code on load. SafeTensors stores
    only numbers and metadata with no code-execution mechanism.

??? question "12. A colleague says their intrusion detection model is 99.4% accurate. What is your first question, and why?"
    **Answer:** "What are the precision and recall?" (or "show me the confusion matrix").
    Intrusions are rare, so a model that flags nothing scores extremely high accuracy while
    being useless. Accuracy is the wrong metric for imbalanced problems.

??? question "13. Why is the test set used only once?"
    **Answer:** Every time you check test performance and then change your approach, you fit
    your decisions to that data. It stops being unseen, and your performance estimate becomes
    optimistically biased.

??? question "14. Explain why overfitting is a security problem, not only a quality problem."
    **Answer:** An overfitted model has effectively memorised training examples and can be
    induced to reproduce them. If that data contained personal or proprietary information,
    the model becomes an exfiltration channel.

??? question "15. Your team fine-tunes a public foundation model. What have you inherited?"
    **Answer:** All of the base model's properties — its biases, any planted backdoors, any
    memorised sensitive data, and its licensing/provenance uncertainty. **Fine-tuning does
    not cleanse a base model.**

### Section D — RAG and applied security

??? question "16. Why use RAG instead of retraining a model on company documents?"
    **Answer:** Retraining is expensive and slow, cannot track daily document changes, and
    bakes information into weights where it cannot reliably be deleted. RAG keeps data in a
    store you can update, permission, and erase.

??? question "17. Explain indirect prompt injection in one sentence."
    **Answer:** An attacker plants instruction-like text in a document the system later
    retrieves, so the model follows the attacker's instructions while serving an innocent
    user's unrelated request.

??? question "18. A company indexes its entire shared drive into one vector store for a company-wide assistant. What is the most likely vulnerability?"
    **Answer:** Access control bypass — the assistant can surface HR files, salaries, or
    board material to users who are not authorised to read them, because the retrieval layer
    does not enforce source-system permissions.

??? question "19. Two chatbots share the same prompt-injection flaw. One answers FAQs; one can issue refunds. Are the vulnerabilities equally severe?"
    **Answer:** No. The technique is identical; the impact is not. **Severity is driven by
    what the system is permitted to do**, which is the core intuition behind *excessive
    agency*.

??? question "20. Why can't we fix prompt injection the way we fixed SQL injection?"
    **Answer:** SQL injection was solved by separating the command channel from the data
    channel (parameterised queries). An LLM receives instructions and user input as one
    undifferentiated text stream with no architectural separation, so the equivalent fix does
    not exist. We manage the risk; we do not eliminate it.

---

## Scoring yourself

| Score | What it means |
|---|---|
| **17–20** | Excellent. Move on to Chapter 2. |
| **13–16** | Good. Re-read the sections behind your misses, then continue. |
| **9–12** | Shaky. Re-read the chapter and redo Lab 1.1 before continuing — Chapter 2 builds directly on this. |
| **Under 9** | Do not push on. Work through the chapter again slowly and ask in `#chapter-01`. This is normal for a genuine beginner; the material compounds, so fixing it now is far cheaper than fixing it later. |

---

## Readiness checklist

Tick these honestly before starting Chapter 2.

- [ ] I can explain AI, ML, and deep learning and how they nest.
- [ ] I can name the three components of an AI system and a threat to each.
- [ ] I can describe supervised, unsupervised, and reinforcement learning with an example
      of each.
- [ ] I understand why accuracy is a misleading metric for rare events.
- [ ] I can explain what RAG is and draw its pipeline from memory.
- [ ] I can explain why indirect prompt injection is harder to defend than direct.
- [ ] I ran Lab 1.1 and used the `/prompt` command.
- [ ] **I can explain why a system prompt is not a security boundary.**
- [ ] I can state the three questions to ask about any AI system.
- [ ] I understand why a model that passes its test set may still be unsafe.

!!! tip "If you ticked fewer than eight"
    Go back rather than forward. Chapter 2 opens with transformer architecture and the MITRE
    ATLAS matrix, both of which assume this foundation is solid. Time spent here is
    recovered several times over.

---

## Going further (optional)

Not required, but genuinely worthwhile if this chapter sparked your interest.

- **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** (2017) — the transformer
  paper. Dense, but skim the diagrams; you will recognise more than you expect.
- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** —
  you will study this properly in Chapter 3. Reading the list now primes you.
- **[MITRE ATLAS](https://atlas.mitre.org/)** — browse the matrix. It will look overwhelming;
  that is fine, Chapter 2 walks through it tactic by tactic.
- **[AI Incident Database](https://incidentdatabase.ai/)** — real-world AI failures. Pick
  three and, for each, work out which of the three components failed.

---

<div class="caisp-cards">
<a class="caisp-card" href="index.md">
  <span class="caisp-kicker">Back</span>
  <span class="caisp-card-title">Chapter 1 Contents</span>
  <span class="caisp-card-text">Revisit any section.</span>
</a>
<a class="caisp-card" href="../chapter-02/index.md">
  <span class="caisp-kicker">Next chapter</span>
  <span class="caisp-card-title">Chapter 2 — Understanding and Attacking LLMs</span>
  <span class="caisp-card-text">Transformers, GPT vs BERT, fine-tuning, the full MITRE ATLAS matrix, and ten hands-on labs.</span>
</a>
</div>
