---
tags:
  - Chapter 2
---

# Chapter 2 — Understanding and Attacking Large Language Models

<ul class="caisp-meta">
  <li>Level: Beginner → Intermediate</li>
  <li>Reading: ~2.5 hrs</li>
  <li>Labs: 10</li>
  <li>Prereq: Chapter 1</li>
</ul>

This is the biggest chapter in the course, and the most important. In Chapter 1 you learned
*what* AI is. Here you learn how large language models actually work under the hood, and then
you start attacking them — first understanding the attacker's playbook (MITRE ATLAS), then
running ten hands-on labs that alternate between *building* LLM systems and *breaking* them.

The philosophy of this chapter is simple: **you cannot secure what you cannot build.** So you
will build a chatbot, a summarizer, a scraper, a fine-tuned model, and a RAG system — and then
you will attack models with real adversarial tooling and study how backdoors work.

!!! objective "What you will be able to do after this chapter"
    - Explain the **transformer** architecture and the **attention** mechanism in plain
      language.
    - Distinguish **GPT** (decoder, generative) from **BERT** (encoder, understanding) and
      say when each is used.
    - Explain the difference between a **foundational** model and a **fine-tuned** model, and
      the security implications of each.
    - Navigate the **MITRE ATLAS** matrix and map a real attack to its tactics, tactic by
      tactic.
    - Explain what tools like **WormGPT** and **FraudGPT** are, why they exist, and what
      their existence means for defenders — without building anything harmful.
    - **Build** a chatbot, tokenizer explorer, summarizer, fine-tuned model, web scraper,
      and RAG system.
    - **Attack** a model with TextAttack, and understand how **backdoors** are planted and
      detected.

---

## How this chapter flows

```mermaid
flowchart TD
    A[2.1 How LLMs work] --> B[2.2 GPT vs BERT]
    B --> C[2.3 Training & augmenting]
    C --> D[2.4 Use cases]
    D --> E[2.5 Attack tactics: ATT&CK & ATLAS]
    E --> F[2.6 Malicious LLM tools]
    F --> G[10 hands-on labs]
    G --> H[Review & quiz]
```

The concept sections build your mental model. The labs make it real. Do them interleaved: read
2.1–2.4, then do the "building" labs (2.1–2.6); read 2.5–2.6, then do the "attacking" labs
(2.7–2.9). The speech-to-text lab (2.10) rounds out your understanding of multimodal systems.

---

## Sections

<div class="caisp-cards">
<a class="caisp-card" href="01-intro-to-llms.md">
  <span class="caisp-kicker">2.1</span>
  <span class="caisp-card-title">Introduction to LLMs</span>
  <span class="caisp-card-text">What an LLM is, how the transformer works, and why attention changed everything.</span>
</a>
<a class="caisp-card" href="02-gpt-and-bert.md">
  <span class="caisp-kicker">2.2</span>
  <span class="caisp-card-title">Understanding LLMs — GPT &amp; BERT</span>
  <span class="caisp-card-text">Two families, two philosophies: generation vs. understanding.</span>
</a>
<a class="caisp-card" href="03-training-and-augmenting.md">
  <span class="caisp-kicker">2.3</span>
  <span class="caisp-card-title">Training &amp; Augmenting LLMs</span>
  <span class="caisp-card-text">Foundational vs. fine-tuned models, and RAG as augmentation.</span>
</a>
<a class="caisp-card" href="04-use-cases.md">
  <span class="caisp-kicker">2.4</span>
  <span class="caisp-card-title">Use Cases of LLMs</span>
  <span class="caisp-card-text">Generation, understanding, and conversational AI — with the risks of each.</span>
</a>
<a class="caisp-card" href="05-attack-tactics-atlas.md">
  <span class="caisp-kicker">2.5</span>
  <span class="caisp-card-title">Attack Tactics — ATT&amp;CK &amp; ATLAS</span>
  <span class="caisp-card-text">The attacker's playbook, walked tactic by tactic.</span>
</a>
<a class="caisp-card" href="06-malicious-llm-tools.md">
  <span class="caisp-kicker">2.6</span>
  <span class="caisp-card-title">Real-World Malicious LLM Tools</span>
  <span class="caisp-card-text">WormGPT, FraudGPT, and what the criminal market tells defenders.</span>
</a>
</div>

## Labs

<div class="caisp-cards">
<a class="caisp-card" href="lab-01-simple-chatbot.md">
  <span class="caisp-kicker">Lab 2.1 · Build</span>
  <span class="caisp-card-title">A Simple Chatbot</span>
  <span class="caisp-card-text">A clean, minimal chatbot to anchor the chapter.</span>
</a>
<a class="caisp-card" href="lab-02-tokenizers.md">
  <span class="caisp-kicker">Lab 2.2 · Build</span>
  <span class="caisp-card-title">How Tokenizers Work</span>
  <span class="caisp-card-text">See the world the way a model does — in tokens.</span>
</a>
<a class="caisp-card" href="lab-03-summarizer.md">
  <span class="caisp-kicker">Lab 2.3 · Build</span>
  <span class="caisp-card-title">Build a Summarizer</span>
  <span class="caisp-card-text">Condense text with an LLM, and probe where it fails.</span>
</a>
<a class="caisp-card" href="lab-04-fine-tuning.md">
  <span class="caisp-kicker">Lab 2.4 · Build</span>
  <span class="caisp-card-title">Fine-tune a Model</span>
  <span class="caisp-card-text">Specialise a model on your own data — and inherit its risks.</span>
</a>
<a class="caisp-card" href="lab-05-scraper.md">
  <span class="caisp-kicker">Lab 2.5 · Build</span>
  <span class="caisp-card-title">A Website Scraper</span>
  <span class="caisp-card-text">Feed the web to an LLM — and meet indirect injection.</span>
</a>
<a class="caisp-card" href="lab-06-rag.md">
  <span class="caisp-kicker">Lab 2.6 · Build</span>
  <span class="caisp-card-title">Build a RAG System</span>
  <span class="caisp-card-text">The most important architecture in enterprise AI.</span>
</a>
<a class="caisp-card" href="lab-07-textattack.md">
  <span class="caisp-kicker">Lab 2.7 · Attack</span>
  <span class="caisp-card-title">Attacking with TextAttack</span>
  <span class="caisp-card-text">Adversarial examples against a real classifier.</span>
</a>
<a class="caisp-card" href="lab-08-sentiment.md">
  <span class="caisp-kicker">Lab 2.8 · Build</span>
  <span class="caisp-card-title">Sentiment Analysis</span>
  <span class="caisp-card-text">Classification, confidence, and why confidence lies.</span>
</a>
<a class="caisp-card" href="lab-09-backdoors.md">
  <span class="caisp-kicker">Lab 2.9 · Defend</span>
  <span class="caisp-card-title">Backdoor Attacks (Defensive)</span>
  <span class="caisp-card-text">How backdoors work, and how to detect them.</span>
</a>
<a class="caisp-card" href="lab-10-speech-to-text.md">
  <span class="caisp-kicker">Lab 2.10 · Build</span>
  <span class="caisp-card-title">Speech-to-Text</span>
  <span class="caisp-card-text">Multimodal input, and the attack surface it opens.</span>
</a>
</div>

---

!!! danger "Rules of engagement — still apply, more than ever"
    This chapter contains genuine offensive techniques. Run them **only** against the local
    labs provided here or systems you are explicitly authorised to test. The
    [rules of engagement](../start-here/index.md) are not boilerplate — in this chapter they
    are the difference between education and a crime.
