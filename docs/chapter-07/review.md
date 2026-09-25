---
tags:
  - Chapter 7
  - Review
---

# Chapter 7 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 25 min</li>
  <li>16 questions</li>
  <li>Self-assessed</li>
</ul>

---

## The one-page summary

### Emerging threats

| Threat | Mechanism | Key defence |
|---|---|---|
| **Model-mediated supply chain** | The *recommendation* is compromised, not the artefact | Verify before installing; treat AI suggestions as unverified |
| **Model worms** | Self-replicating prompt spreads between AI systems | **Remove the outbound path** (LLM08) |
| **Fine-tuning backdoors** | Backdoors survive tuning; tuning can strip safety | Protect tuning data; re-test safety after |
| **AI-assisted evolving malware** | Lowers cost/skill floor for polymorphic code | Behavioural detection over signatures |
| **Models without provenance** | Nobody knows origin, data, or integrity | **Inventory + signing** |

**Models without provenance is the most consequential** — it makes every other threat unassessable.

### NIST AI RMF — four functions

- **GOVERN** — policy, accountability, culture *(cross-cutting)*
- **MAP** — context and risk identification → *your threat modeling*
- **MEASURE** — analysis and tracking → *your evaluation harnesses*
- **MANAGE** — prioritise, respond, monitor → *your risk treatment*

Seven trustworthiness characteristics; **security is only one of them**.

### ISO/IEC 42001

A **certifiable** AI Management System standard. 42001 : AI :: 27001 : information security.

| | NIST AI RMF | ISO/IEC 42001 |
|---|---|---|
| Type | Voluntary framework | **Certifiable standard** |
| Purpose | Structure how you *do* it | **Demonstrate** it to third parties |

### EU AI Act

**Risk tiers set by USE CASE, not technology:** Unacceptable (banned) → High (heavy obligations) →
Limited (transparency) → Minimal. **Extraterritorial reach.**

High-risk obligations map almost exactly onto Chapters 4–6.

### US

**Fragmented** — no comprehensive federal statute; executive action + existing agency authority +
sector rules + state patchwork + NIST AI RMF.

### Agents

**An LLM in a loop with tools.** They concentrate every risk: untrusted input from multiple channels
including **tool output**, an instruction-following model, real privilege, and a loop.

> **4/4 attacks succeeded against the vulnerable agent. 0/4 against the hardened one — and the
> hardened agent is no better at detecting attacks.**

---

## Quiz

??? question "1. What makes model-mediated supply chain attacks a new class?"
    They compromise a *recommendation* rather than an artefact. There is nothing to scan, and the
    developer's own trust in a tool they consult constantly is recruited against them. It sits at the
    intersection of LLM09 and LLM05.

??? question "2. Name the three conditions an AI model worm requires."
    Untrusted input reaching the model; the model following injected instructions; and an **outbound
    path** to other AI systems. Removing the outbound path stops propagation regardless of injection
    success.

??? question "3. Why is 'models without provenance' arguably the most consequential emerging threat?"
    It makes every other threat unassessable — you cannot determine whether a model is backdoored,
    edited, or derived from a compromised base without knowing its origin, training data, and
    integrity. You cannot even rate the risk.

??? question "4. How should you calibrate claims about AI-generated malware?"
    Credible: AI lowers the cost and skill floor for producing polymorphic, environment-aware code and
    raises the volume defenders face. Overstated: autonomous self-directing AI malware. The defensive
    implication is unchanged — favour behavioural detection over signatures.

??? question "5. Name the four NIST AI RMF functions and identify the cross-cutting one."
    Govern, Map, Measure, Manage. **Govern** is cross-cutting — policy, accountability, roles, and
    culture, applying to all the others.

??? question "6. Map threat modeling, evaluation harnesses, and risk treatment to RMF functions."
    Threat modeling → **Map**. Evaluation harnesses (hallucination rate, guardrail recall) →
    **Measure**. Risk rating and treatment → **Manage**.

??? question "7. Which RMF function do most organisations lack, and why does it matter?"
    **Govern.** Capable individuals often do good work inconsistently because nobody is accountable
    for whether risk management happens at all. Without Govern, the other functions occur ad hoc.

??? question "8. Why is security only one of NIST's seven trustworthiness characteristics?"
    Because AI risk is broader than CIA. A system can be perfectly secure while being biased, opaque,
    unreliable, or unsafe — and those failures are regulated and increasingly land on the AI security
    team.

??? question "9. What is the practical difference between NIST AI RMF and ISO/IEC 42001?"
    RMF is a voluntary, outcome-oriented framework for structuring AI risk management. 42001 is a
    certifiable management system standard auditable by accredited bodies, so it demonstrates
    governance externally. Mature organisations use both.

??? question "10. What determines a system's risk tier under the EU AI Act?"
    The **use case** — what it is used for and who it affects — not the technology. The same
    classifier is minimal risk sorting tickets and high risk screening job applicants.

??? question "11. Why does the EU AI Act apply to organisations outside the EU?"
    Extraterritorial reach: broadly it applies where systems are placed on the EU market or their
    output is used in the EU, regardless of provider location. Combined with significant penalties,
    this has made it a de facto global reference.

??? question "12. Name four EU AI Act high-risk obligations you already learned in this course."
    Any four of: risk management system (Ch 5), data governance (Ch 6), technical documentation /
    model cards / MLBOM (Ch 6), record-keeping and logging (Ch 4), human oversight (LLM08), and
    accuracy/robustness/cybersecurity testing (Labs 3.4, 4.6).

??? question "13. Characterise US AI regulation in one sentence."
    Fragmented — no comprehensive federal statute, but executive action, existing agency authority
    applied to AI, sector-specific regulation, a growing state-law patchwork, and influential
    voluntary frameworks such as NIST AI RMF.

??? question "14. What is an agent, and what is the most commonly missed untrusted input channel?"
    An LLM in a loop with tools (plan → act → observe → repeat). The most commonly missed untrusted
    channel is **tool output** — anything a tool returns influences the agent's next decision.

??? question "15. In Lab 7.2, the hardened agent blocked all four attacks. Was it better at detecting them?"
    **No.** The injection still landed and the planner still attempted the malicious action. What
    changed was what the agent was *permitted to do* — the refund limit, authorisation context,
    approval gate, and email allowlist blocked the consequences. The model was compromised; the
    system was not.

??? question "16. What is the single best design-review question for an agentic system?"
    *"What is the worst thing this agent could do if fully compromised?"* If the answer is
    unacceptable, no amount of guardrail tuning fixes it — the architecture must change.

---

## Scoring yourself

| Score | Meaning |
|---|---|
| **13–16** | Excellent. You have finished the course content. |
| **10–12** | Good. Re-read 7.2 and 7.3 — governance marks are easy to bank. |
| **6–9** | Re-read the chapter; redo Lab 7.2. |
| **Under 6** | Rework it — and do not dismiss governance as "not technical". |

---

## Readiness checklist

- [ ] I can describe the five emerging threat patterns and their defences.
- [ ] I can explain why provenance-less models make everything else unassessable.
- [ ] **I can name the four NIST AI RMF functions and map my work to them.**
- [ ] I can explain what ISO/IEC 42001 is and how it differs from NIST AI RMF.
- [ ] I can explain the EU AI Act risk tiers and that they are set by **use case**.
- [ ] I can list four high-risk obligations and where I learned them.
- [ ] I can characterise the US regulatory landscape.
- [ ] I built an agent and can explain the plan/act/observe loop.
- [ ] **I understand that tool output is an untrusted input channel.**
- [ ] **I can explain why the hardened agent won by limiting consequences, not by detecting better.**
- [ ] I can assess an agent's agency across three dimensions.
- [ ] I know the design-review question to lead with.

---

<div class="caisp-cards">
<a class="caisp-card" href="index.md">
  <span class="caisp-kicker">Back</span>
  <span class="caisp-card-title">Chapter 7 Contents</span>
  <span class="caisp-card-text">Revisit any section or lab.</span>
</a>
<a class="caisp-card" href="../wrap-up/index.md">
  <span class="caisp-kicker">Finish</span>
  <span class="caisp-card-title">Course Wrap-Up</span>
  <span class="caisp-card-text">You have completed all seven chapters. Here is what to do next.</span>
</a>
</div>
