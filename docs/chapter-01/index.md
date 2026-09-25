---
tags:
  - Chapter 1
  - Fundamentals
---

# Chapter 1 — Introduction to AI Security

<ul class="caisp-meta">
  <li>Level: Beginner</li>
  <li>Reading: ~90 min</li>
  <li>Labs: 1</li>
  <li>Prereq: Lab setup complete</li>
</ul>

Welcome to the first chapter. Before we can secure AI systems, we have to understand what
they *are* — and this chapter builds that understanding from nothing. By the time you finish,
you will be able to hold your own in a conversation about AI, and you will have built and run
your first working chatbot.

!!! objective "What you will be able to do after this chapter"
    - Explain, in plain language, what **AI**, **machine learning**, and **deep learning**
      are, and how they relate to one another.
    - Describe the **history** of AI in broad strokes and why *now* is different.
    - Distinguish the main **types of AI** and learning approaches: narrow vs. general;
      supervised, unsupervised, and reinforcement learning; NLP and computer vision.
    - Identify the **three core components** every AI system is built from.
    - Explain what **Retrieval Augmented Generation (RAG)** is and why it matters for
      security.
    - Describe what a **neural network** and a **CNN** are at a conceptual level.
    - Explain why AI systems create a **new kind of security problem** — the theme of the
      whole course.
    - **Build a working chatbot** on your own machine (Lab 1.1).

---

## How to read this chapter

This chapter is mostly foundational knowledge, so it is heavier on reading than later
chapters. Do not rush it. The vocabulary you build here — *model*, *token*, *training*,
*embedding* — is used in every single chapter that follows. If those words are solid now,
everything downstream is easier.

Read the sections in order:

<div class="caisp-cards">
<a class="caisp-card" href="01-overview-of-ai-security.md">
  <span class="caisp-kicker">1.1</span>
  <span class="caisp-card-title">An Overview of AI Security</span>
  <span class="caisp-card-text">Why AI breaks differently from normal software, and who is trying to break it.</span>
</a>
<a class="caisp-card" href="02-basics-of-ai.md">
  <span class="caisp-kicker">1.2</span>
  <span class="caisp-card-title">Basics of AI</span>
  <span class="caisp-card-text">What AI is, where it came from, and the key ideas.</span>
</a>
<a class="caisp-card" href="03-types-of-ai.md">
  <span class="caisp-kicker">1.3</span>
  <span class="caisp-card-title">Types of AI</span>
  <span class="caisp-card-text">Narrow vs. general; the three learning styles; NLP and vision.</span>
</a>
<a class="caisp-card" href="04-core-components.md">
  <span class="caisp-kicker">1.4</span>
  <span class="caisp-card-title">Core Components of AI Systems</span>
  <span class="caisp-card-text">Algorithms and models, data, and computing power.</span>
</a>
<a class="caisp-card" href="05-intro-to-ml.md">
  <span class="caisp-kicker">1.5</span>
  <span class="caisp-card-title">Introduction to Machine Learning</span>
  <span class="caisp-card-text">What ML is, how it differs from AI, and the key concepts.</span>
</a>
<a class="caisp-card" href="06-rag.md">
  <span class="caisp-kicker">1.6</span>
  <span class="caisp-card-title">Retrieval Augmented Generation</span>
  <span class="caisp-card-text">How models get access to knowledge they were not trained on.</span>
</a>
<a class="caisp-card" href="07-deep-learning.md">
  <span class="caisp-kicker">1.7</span>
  <span class="caisp-card-title">Basics of Deep Learning</span>
  <span class="caisp-card-text">Neural networks and CNNs, explained gently.</span>
</a>
<a class="caisp-card" href="lab-01-chatbot.md">
  <span class="caisp-kicker">Lab 1.1</span>
  <span class="caisp-card-title">Build a Chatbot with an LLM</span>
  <span class="caisp-card-text">Your first hands-on build. Works fully offline.</span>
</a>
<a class="caisp-card" href="review.md">
  <span class="caisp-kicker">Wrap-up</span>
  <span class="caisp-card-title">Review &amp; Quiz</span>
  <span class="caisp-card-text">Consolidate and self-test before Chapter 2.</span>
</a>
</div>

---

!!! tip "Keep the glossary handy"
    Open the [Glossary](../start-here/glossary.md) in a second tab. Whenever a bolded term
    appears that you are unsure about, glance at its one-line definition and keep reading.
