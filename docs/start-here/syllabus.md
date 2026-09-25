# Syllabus & Roadmap

This page is the map. Every topic the course covers is listed here, in order, so you can
see where you are and what is coming.

!!! tip "How to use this page"
    Bookmark it. Come back after each chapter and tick things off. Seeing the list shrink
    is surprisingly motivating when you are eight hours into a seven-chapter course.

---

## Course structure at a glance

```mermaid
flowchart TD
    C1[Ch 1 · Foundations<br/>What AI actually is]
    C2[Ch 2 · LLMs & Attack Tactics<br/>How LLMs work, MITRE ATLAS]
    C3[Ch 3 · OWASP LLM Top 10<br/>The core vulnerability classes]
    C4[Ch 4 · AI in DevOps<br/>Pipeline attacks & tooling defences]
    C5[Ch 5 · Threat Modeling<br/>Systematic risk discovery]
    C6[Ch 6 · Supply Chain<br/>Models as untrusted artefacts]
    C7[Ch 7 · Emerging & Governance<br/>What's next, and the law]

    C1 --> C2 --> C3 --> C4
    C3 --> C5
    C4 --> C6 --> C7
    C5 --> C7
```

**Chapters 1–3 are the foundation.** Do them in order; each genuinely depends on the last.

**Chapters 4–6 are the practitioner core.** They can tolerate slight reordering, but the
default order is recommended.

**Chapter 7 is the horizon.** It only makes sense once you have the earlier material.

---

## Chapter 1 — Introduction to AI Security

!!! objective "By the end you can"
    Explain what AI, ML, and deep learning are and how they differ; describe the core
    components of an AI system; explain what RAG is and why it matters for security; and
    build a working chatbot on your own machine.

**Course orientation**

- [x] Course introduction — about the course, syllabus, and how to approach it
- [x] About certification and how to approach it
- [x] Course lab environment
- [x] Lifetime course support (Mattermost)

**An overview of AI security**

- Why AI systems fail differently from traditional software
- The expanded attack surface
- Who attacks AI systems and why

**Basics of AI and ML**

- What is AI?
- History and evolution of AI
- Key concepts in AI

**Types of AI**

- Narrow AI vs. General AI
- Supervised learning
- Unsupervised learning
- Reinforcement learning
- Natural Language Processing (NLP)
- Computer vision

**Core components of AI systems**

- Algorithms and models
- Data
- Computing power

**Introduction to machine learning**

- What is machine learning?
- Differences between AI and ML
- Key ML concepts
- Retrieval Augmented Generation (RAG)

**Basics of deep learning**

- What is deep learning?
- Introduction to neural networks
- Brief overview of Convolutional Neural Networks (CNNs)

**Hands-on exercise**

- :material-flask: Lab 1.1 — Building a chatbot using an LLM

**Estimated time:** 5–7 hours

---

## Chapter 2 — Understanding and Attacking Large Language Models

!!! objective "By the end you can"
    Explain the transformer architecture at a conceptual level; distinguish foundational
    from fine-tuned models; navigate the MITRE ATLAS matrix tactic by tactic; and run a
    range of offensive and analytical techniques against models you control.

**Introduction to large language models**

- Definition of large language models
- How LLMs work
- Importance and impact of LLMs in AI

**Understanding LLMs**

- GPT (Generative Pre-trained Transformer)
- BERT (Bidirectional Encoder Representations from Transformers)

**Training and augmenting LLMs**

- Foundational model and fine-tuned model
- Retrieval augmented generation

**Use cases of LLMs**

- Text generation
- Text understanding
- Conversational AI

**Attack tactics and techniques**

- MITRE ATT&CK
- MITRE ATLAS matrix
- Reconnaissance tactic
- Resource development tactic
- Initial access tactic
- ML model access tactic
- Execution tactic
- Persistence tactic
- Privilege escalation tactic
- Defense evasion tactic
- Credential access tactic
- Discovery tactic
- Collection tactic
- ML attack staging
- Exfiltration tactic
- Impact tactic

**Real-world LLM attack tools on the internet**

- XXXGPT, WormGPT, FraudGPT — what they are, how they are marketed, and what their
  existence tells defenders

**Hands-on exercises**

- :material-flask: Creating a simple chatbot
- :material-flask: Exploring how tokenizers work
- :material-flask: Building a summarizer tool using an LLM
- :material-flask: Building a fine-tuned model
- :material-flask: Building a simple website scraper
- :material-flask: Building a RAG system
- :material-flask: Attacking an LLM model using TextAttack
- :material-flask: Performing sentiment analysis using an LLM
- :material-flask: Backdoor attacks using BackdoorBox
- :material-flask: Building a speech-to-text system

**Estimated time:** 12–15 hours — this is the largest chapter

---

## Chapter 3 — LLM Top 10 Vulnerabilities

!!! objective "By the end you can"
    Name, explain, demonstrate, and mitigate each of the OWASP Top 10 for LLM
    Applications, and recognise them in an unfamiliar architecture.

**Introduction to the OWASP Top 10 LLM attacks**

**1. Prompt injection**

- System prompts versus user prompts
- Direct and indirect prompt injection
- Prompt injection techniques
- Mitigating prompt injection

**2. Insecure output handling**

- Consequences of insecure output handling
- Mitigating insecure output handling

**3. Training data poisoning**

- LLM's core learning approaches
- Mitigating training data poisoning

**4. Model denial of service**

- DoS on networks, applications, and models
- Context windows and exhaustion
- Mitigating denial of service

**5. Supply chain vulnerabilities**

- Components or stages in an LLM
- Compromising the LLM supply chain
- Mitigating supply chain vulnerabilities

**6. Sensitive information disclosure**

- Exploring data leaks in various incidents
- Mitigating sensitive information disclosure

**7. Insecure plugin design**

- Plugin / connected software attack scenarios
- Mitigating insecure plugin design

**8. Excessive agency**

- Excessive permissions and autonomy
- Mitigating excessive agency

**9. Overreliance**

- Understanding hallucinations
- Overreliance examples
- Mitigating overreliance

**10. Model theft**

- Stealing models
- Mitigating model theft

**Hands-on exercises**

- :material-flask: Learning prompt injection step by step
- :material-flask: Working with user prompts and system prompts
- :material-flask: Extracting sensitive information through an LLM
- :material-flask: LLM hallucination lab

**Estimated time:** 10–12 hours

---

## Chapter 4 — AI Attacks and Defenses Using DevOps

!!! objective "By the end you can"
    Describe an ML deployment pipeline and its attack surface; and use SCA, static
    analysis, dynamic analysis, and AI firewalls to defend one.

**Introduction to AI in DevOps**

- Definition and principles of DevOps and DevSecOps
- The role of AI in enhancing DevOps practices

**Types of AI attacks on DevOps teams**

- Model creation and deployment process/pipeline
- Attacks on pipelines

**Cases of attacks in DevOps and AI**

- Hugging Face AI platform incidents
- NotPetya attack
- SAP AI Core vulnerabilities

**DevSecOps tooling and defenses for AI projects**

- Software composition analysis for AI projects
- Static analysis of models and applications
- Dynamic analysis of models and applications
- AI firewalls for guarding models

**Hands-on exercises**

- :material-flask: Analyzing and fixing vulnerabilities in third-party components
- :material-flask: Finding and fixing weaknesses in AI code
- :material-flask: Scanning a malicious pickle file using Picklescan
- :material-flask: Scanning an LLM for agent-based vulnerabilities
- :material-flask: Sanitizing prompts with LLM Guard
- :material-flask: Guarding LLM input and output

**Estimated time:** 8–10 hours

---

## Chapter 5 — Threat Modeling AI Systems

!!! objective "By the end you can"
    Draw a data flow diagram for an LLM application, apply STRIDE to it, pull threats
    from AI-specific libraries, and rate the resulting risks defensibly.

**What is threat modeling**

- Why threat model?
- Threat modeling challenges
- Threat modeling benefits

**The threat model parlance**

- What are assets?
- Weaknesses and vulnerability
- Risk management stages
- STRIDE methodology

**Diagramming for threat modeling**

- Data flow diagram
- DFD components

**An LLM application architecture**

- Simple LLM architecture
- DFD for an LLM architecture
- STRIDE threats for LLM applications

**AI threat libraries**

- STRIDE
- OWASP LLM Top 10
- MITRE ATLAS
- BIML risk framework
- AI Risk Repository
- AI Incident Database
- AI Threat Map

**Rating and managing risks**

- Risk management meets threat modeling
- Risk management strategies
- Example risk rating methodology

**Hands-on exercise**

- :material-flask: Threat modeling an AI system

**Estimated time:** 6–8 hours

---

## Chapter 6 — Supply Chain Attacks in AI

!!! objective "By the end you can"
    Explain why a downloaded model is untrusted executable content; vet third-party AI
    dependencies systematically; and produce and verify SBOMs, model cards, and
    signatures.

**An overview of supply chain security**

**Introduction to AI supply chain attacks**

- Data, model, and infrastructure-based attacks
- Abusing generative AI for package masquerading

**Vetting software frameworks**

- Creating a vetting process
- Automating vetting of third-party code
- Scanning for vulnerabilities
- Mitigating dependency confusion
- Dependency pinning

**Supply chain frameworks**

- SLSA
- Software Component Verification Standard (SCVS)

**Transparency and integrity in the AI supply chain**

- Generate a Software Bill of Materials
- SBOMs, provenance, and attestations
- Model cards and MLBOMs
- Model signing

**Hands-on exercises**

- :material-flask: Editing models using the ROME technique
- :material-flask: Creating trojanized models
- :material-flask: Creating trojanized neural network models
- :material-flask: Scanning models and injecting malicious code
- :material-flask: Signing and verifying machine learning models using Cosign

**Estimated time:** 8–10 hours

---

## Chapter 7 — Emerging Threats, Governance, and Compliance in AI

!!! objective "By the end you can"
    Describe the frontier of AI threats, and map security work to the major frameworks
    and legal regimes governing AI.

**Emerging threats in AI**

- Model-mediated supply chain attacks
- Self-propagating AI model worms
- Backdoors in fine-tuning
- AI-assisted evolving firmware
- Models without provenance

**AI governance and compliance**

- Standards, guidelines, frameworks, checklists for AI security
- NIST AI RMF
- ISO/IEC 42001
- Other standards and guidelines

**AI acts, bills, and legislations**

- EU AI Act
- US legislations

**Hands-on exercises**

- :material-flask: Working with AI agents
- :material-flask: Abusing AI agents

**Estimated time:** 6–8 hours

---

## Total commitment

| | Hours |
|---|---|
| Reading and concepts | ~25 |
| Hands-on labs | ~30 |
| Review, quizzes, and exam prep | ~10 |
| **Total** | **~65 hours** |

That is a genuine estimate for someone starting from zero and doing every lab. If you have
an ML or security background already, expect closer to 35–40 hours.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../certification/" markdown>
<span class="caisp-kicker">Next</span>
### Certification Guide
Exam format and how to prepare.
</a>

<a class="caisp-card" href="../lab-environment/" markdown>
<span class="caisp-kicker">Then</span>
### Lab Environment Setup
Get your machine ready.
</a>

</div>
