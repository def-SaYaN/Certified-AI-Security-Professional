---
tags:
  - Chapter 5
  - Review
---

# Chapter 5 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 30 min</li>
  <li>18 questions</li>
  <li>Self-assessed</li>
</ul>

---

## The one-page summary

### The four questions

1. **What are we building?** → draw the DFD
2. **What can go wrong?** → STRIDE + threat libraries
3. **What are we going to do about it?** → rate, then treat
4. **Did we do a good job?** → coverage check

### The vocabulary

| Term | Meaning | You... |
|---|---|---|
| **Asset** | Something worth protecting | inventory |
| **Threat** | A potential harmful event | enumerate |
| **Weakness** | A general flaw | note |
| **Vulnerability** | A weakness exploitable *here* | find |
| **Risk** | Likelihood × Impact | rate |

### DFD elements

External entity (rectangle) · Process (circle) · Data store (open box) · Data flow (arrow) ·
**Trust boundary (dashed line)**

**Threats concentrate at trust boundaries.** The three AI-specific ones teams always miss:

- **TB2** — untrusted content → prompt
- **TB3** — model output → trusted contexts
- **TB4** — tool call where identity changes

### STRIDE

| | Threat | Violates | AI instance |
|---|---|---|---|
| **S** | Spoofing | Authentication | Forged system-message delimiters |
| **T** | Tampering | Integrity | Prompt injection, data poisoning |
| **R** | Repudiation | Non-repudiation | No logging of agent actions |
| **I** | Information disclosure | Confidentiality | The whole of LLM06 |
| **D** | Denial of service | Availability | LLM04, denial of wallet |
| **E** | Elevation of privilege | Authorisation | Confused deputy, excessive agency |

### Threat libraries

**STRIDE** (structure) + **OWASP LLM Top 10** (AI specificity) + **ATLAS** (attacker narrative) is
the default recipe. Add **BIML** for non-LLM ML, **AI Risk Repository** for breadth, **AI Incident
Database** for evidence.

### Risk treatments

**Mitigate · Transfer · Accept · Avoid** — and *Avoid* usually wins for AI.

### Sentences to remember

> **The value of a threat model is not the list. It is the ranked list.**

> **Threats concentrate at trust boundaries.**

> **Rate likelihood by ease, not sophistication. Rate impact by agency, not cleverness.**

> **A model that looks complete usually is not — run the coverage check.**

---

## Quiz

??? question "1. What are the four questions of threat modeling?"
    What are we building? What can go wrong? What are we going to do about it? Did we do a good job?

??? question "2. Distinguish a weakness from a vulnerability."
    A weakness is a general flaw ("models can memorise training data"). A vulnerability is a weakness
    actually exploitable in this specific system and configuration. Not every weakness is a
    vulnerability in a given deployment.

??? question "3. Write the risk formula and explain each term."
    Risk = Likelihood × Impact. Likelihood is how probable realisation is (driven by required skill,
    accessibility, existing controls). Impact is how bad it would be (data sensitivity, financial
    cost, safety, legal, reputational).

??? question "4. Name the four risk treatments and give an AI example of Avoid."
    Mitigate, Transfer, Accept, Avoid. Avoid example: removing the assistant's ability to issue
    refunds autonomously, so injection cannot cause fraud.

??? question "5. Why is 'Accept' a legitimate treatment, and what makes it illegitimate?"
    It is legitimate when made deliberately by someone accountable and recorded with rationale. It
    becomes illegitimate when it is a silent, undocumented decision by someone without authority —
    that is an unmanaged risk, not acceptance.

??? question "6. Name the five DFD element types."
    External entity, process, data store, data flow, trust boundary.

??? question "7. Why analyse trust boundaries first?"
    Threats concentrate there — a trust boundary is precisely where data moves from less trusted to
    more trusted, and therefore where validation is most likely to have been forgotten. Highest yield
    per unit of time.

??? question "8. Name the three AI-specific trust boundaries teams usually miss, and why."
    Untrusted content → prompt; model output → trusted contexts; tool call where identity changes.
    Missed because retrieved documents feel like internal data, model output feels like our own, and
    tool calls feel like our own code.

??? question "9. Restate indirect prompt injection in DFD terms."
    A data flow carrying attacker-influenced content (a retrieved document) crosses into prompt
    assembly without passing a trust boundary check, because the corpus was modelled as trusted when
    it is writable by untrusted parties.

??? question "10. What does STRIDE stand for, and what does each violate?"
    Spoofing (authentication), Tampering (integrity), Repudiation (non-repudiation), Information
    disclosure (confidentiality), Denial of service (availability), Elevation of privilege
    (authorisation).

??? question "11. Why does STRIDE produce better coverage than expert intuition?"
    It is applied mechanically per element — six questions × N elements — so it forces consideration
    of categories that would not otherwise come to mind. Intuition finds familiar threats and
    silently misses the rest.

??? question "12. How do STRIDE and the OWASP LLM Top 10 complement each other?"
    STRIDE is element-centric and provides structural completeness; OWASP is catalogue-centric and
    provides AI-specific detail. STRIDE ensures you looked everywhere; OWASP tells you what to look
    for.

??? question "13. What does MITRE ATLAS add that OWASP does not?"
    The attacker's perspective and sequencing — how an adversary moves through a system tactic by
    tactic — which is what you need for attack narratives and detection-coverage assessment.

??? question "14. You are modelling an image classifier, not an LLM. Which libraries?"
    STRIDE for structure, BIML for ML-architecture coverage, and ATLAS. The OWASP LLM Top 10 is
    largely inapplicable as it is scoped to LLM applications.

??? question "15. Why should injection-class threats usually be rated high likelihood?"
    Because the payload is plain English against a public interface — no exploit development, no
    tooling, no skill barrier. Likelihood is driven by ease, not sophistication, and public AI
    features are probed within days of launch.

??? question "16. Two systems share the same injection flaw; one answers FAQs, one issues refunds. How do the ratings differ?"
    Likelihood is identical; impact is very different. Impact is driven by agency — what the system
    can do — so the refund system scores far higher and is prioritised accordingly.

??? question "17. What is residual risk and why record it?"
    The risk remaining after treatment. Recording it prevents the illusion that a control eliminated
    the risk, demonstrates what the mitigation achieved, and keeps remaining exposure visible.

??? question "18. Why run a coverage check, and what did it reveal in the worked example?"
    Because a model that looks complete usually is not. In the worked example it revealed four
    elements with no threats (including the guardrails and the embedding model) and that Spoofing was
    never used — despite Lab 3.2 demonstrating delimiter forgery.

---

## Scoring yourself

| Score | Meaning |
|---|---|
| **15–18** | Excellent. Continue to Chapter 6. |
| **11–14** | Good. Re-read 5.2 and 5.6. |
| **7–10** | Re-read the chapter and redo Lab 5.1 on a second system. |
| **Under 7** | Rework it — threat modeling underpins professional practice. |

---

## Readiness checklist

- [ ] I can state the four questions from memory.
- [ ] I use asset / threat / weakness / vulnerability / risk precisely.
- [ ] I can name the four risk treatments and when each applies.
- [ ] I can draw a DFD with all five element types.
- [ ] **I can identify trust boundaries, including the three AI-specific ones.**
- [ ] I can apply STRIDE per element and name an AI instance of each category.
- [ ] I know which threat library to reach for in which situation.
- [ ] I can rate risk and justify both numbers.
- [ ] I know the two AI-specific rating adjustments.
- [ ] **I produced a complete threat model in Lab 5.1.**
- [ ] I ran a coverage check and resolved the gaps.
- [ ] I can summarise a threat model for an executive in under a minute.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../" markdown>
<span class="caisp-kicker">Back</span>
### Chapter 5 Contents
Revisit any section or the lab.
</a>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Coming next</span>
### Chapter 6 — Supply Chain Attacks in AI
Models as untrusted artefacts: vetting, SLSA, SBOMs, model cards, MLBOMs, and signing with Cosign.
Five hands-on labs.
</div>

</div>
