---
tags:
  - Chapter 3
  - OWASP
---

# 3.0 Introduction to the OWASP Top 10 for LLM Applications

!!! objective "In this section"
    - What OWASP is and why its lists carry weight
    - How the LLM Top 10 came about and what it is *for*
    - How to use the list well — and the three ways people misuse it
    - How it relates to MITRE ATLAS

---

## What is OWASP?

The **Open Worldwide Application Security Project** is a non-profit community that produces free,
vendor-neutral security resources. It has been running since 2001, and its flagship output is the
**OWASP Top 10** — a periodically updated list of the most critical web application security
risks.

That original web list became genuinely influential: written into compliance requirements,
referenced in contracts, taught in every application security course, and used as the default
shared vocabulary for "what goes wrong in web apps".

## Why a separate list for LLMs?

When organisations started shipping LLM features in 2023, security teams reached for the familiar
web Top 10 and found it did not fit. Injection was there, but "SQL injection" did not describe an
attacker talking a chatbot into ignoring its instructions. Nothing covered hallucination,
training data poisoning, or a model being cloned through its own API.

The **OWASP Top 10 for Large Language Model Applications** was created to fill that gap — built
by a large open working group of security practitioners, ML engineers, and researchers, drawing
on real incidents and observed attacks.

!!! note "Versions change — the concepts persist"
    The list is periodically revised as the field matures; categories get renamed, merged, split,
    or reprioritised between releases. This course teaches the **ten canonical categories** and,
    more importantly, the *underlying mechanisms*.

    If a future revision renames a category, you will still recognise the vulnerability, because
    you will understand why it happens. Check the
    [current official list](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
    for the exact wording in force when you sit your exam.

??? info "Which edition does this chapter use? (2023 v1.1 → 2025 mapping)"
    This chapter follows the **v1.1 (2023)** numbering, which is how the course syllabus is
    organised. OWASP published a revised **2025** edition that renumbers and regroups the
    categories. Use this table to translate between them:

    | This course (v1.1, 2023) | 2025 edition |
    |---|---|
    | LLM01 Prompt Injection | LLM01:2025 Prompt Injection |
    | LLM02 Insecure Output Handling | LLM05:2025 Improper Output Handling |
    | LLM03 Training Data Poisoning | LLM04:2025 Data and Model Poisoning |
    | LLM04 Model Denial of Service | LLM10:2025 Unbounded Consumption |
    | LLM05 Supply Chain Vulnerabilities | LLM03:2025 Supply Chain |
    | LLM06 Sensitive Information Disclosure | LLM02:2025 Sensitive Information Disclosure |
    | LLM07 Insecure Plugin Design | Folded mainly into LLM06:2025 Excessive Agency |
    | LLM08 Excessive Agency | LLM06:2025 Excessive Agency |
    | LLM09 Overreliance | LLM09:2025 Misinformation |
    | LLM10 Model Theft | Folded into LLM10:2025 Unbounded Consumption (model extraction) |
    | *(covered under LLM06 here)* | **New:** LLM07:2025 System Prompt Leakage |
    | *(covered under RAG in Ch. 1–2)* | **New:** LLM08:2025 Vector and Embedding Weaknesses |

    Every 2025 category is taught somewhere in this course; only the labels and numbers moved.

---

## What the list is for

Four legitimate uses, all of which you will do in this course:

<dl class="caisp-terms" markdown>

<dt>A shared vocabulary</dt>
<dd>"This is LLM02" communicates precisely and instantly. Without shared names, the same
vulnerability gets described five ways and the knowledge never accumulates. (Same argument as
MITRE ATT&CK in section 2.5.)</dd>

<dt>A coverage checklist</dt>
<dd>Walk the ten against your architecture and ask "could this happen here, and would we know?"
The gaps are your priorities.</dd>

<dt>A design-review lens</dt>
<dd>Applied <em>before</em> building, it is far cheaper than applied after. Several categories —
notably LLM08 — are architectural decisions that are painful to reverse later.</dd>

<dt>A communication tool</dt>
<dd>"We have an excessive agency problem" lands better with management than a technical narrative,
because it maps to an external, recognised standard rather than your personal opinion.</dd>

</dl>

---

## Three ways people misuse it

Worth knowing, because all three are common and all three will cost you marks on a scenario
question.

!!! warning "1. Treating it as exhaustive"
    It is a **Top 10**, not an "All 10". It lists the most critical *common* risks. Your system
    may have serious problems that appear nowhere on the list — novel architecture, unusual data
    flows, domain-specific harms.

    Use it as a floor, never a ceiling. A system that is "compliant with the LLM Top 10" is not
    thereby secure.

!!! warning "2. Treating the categories as independent"
    Real incidents chain them. An indirect injection (LLM01) that exfiltrates data through a
    rendered image (LLM02) using an over-permissioned tool (LLM08) is *one* incident spanning
    three categories.

    Assessing each in isolation misses the chains, and the chains are where the severe findings
    live.

!!! warning "3. Confusing 'identified' with 'mitigated'"
    The easiest half of this chapter is learning to *name* the vulnerabilities. The valuable half
    is knowing what to *do* about each one.

    Exam scenario questions almost always ask for both. In real work, a report that lists
    findings without actionable mitigations is of limited use to the team receiving it.

---

## How it relates to MITRE ATLAS

You now know two AI security frameworks. They are complementary, not competing, and knowing when
to reach for each is a genuine professional skill.

| | **OWASP LLM Top 10** | **MITRE ATLAS** |
|---|---|---|
| Describes | **Vulnerabilities** — what is weak | **Attacker behaviour** — what they do |
| Perspective | The defender's, looking at their system | The attacker's, moving through a system |
| Structure | A flat, prioritised list of 10 | A matrix of tactics and techniques |
| Best for | Design review, checklists, remediation | Threat intel, red teaming, detection coverage |
| Question it answers | *"What is wrong with my system?"* | *"How would someone attack it, step by step?"* |

!!! tip "Use both, on the same system"
    A strong assessment does both: OWASP to enumerate the weaknesses, ATLAS to narrate how an
    attacker would chain them into an actual attack.

    Example: *"The corpus is writable by customers (**LLM01**, indirect). An attacker would use
    that for **ATLAS Execution**, then leverage the refund tool (**LLM08**) for **ATLAS
    Privilege Escalation**, achieving **ATLAS Impact** as fraud."*

    That sentence demonstrates command of both frameworks and describes a real attack path. It is
    exactly the register the exam rewards.

---

## How to study this chapter

Ten categories is a lot to absorb. A method that works:

1. **Read all ten once, quickly.** Do not try to memorise. Build the map first.
2. **Then go deep, one at a time.** For each, be able to answer: *What is it? How is it
   exploited? What is the mitigation? What is a real example?*
3. **Do the four labs** between readings — they cover LLM01, LLM06, and LLM09, the three hardest
   to grasp from description alone.
4. **Build a one-page cheat sheet from memory**, then correct it against the chapter. The
   corrections show you exactly what you do not know.
5. **Apply it to a real product** you use that has an AI feature. Walk all ten. This is the
   single best exam preparation exercise in the course.

!!! tip "A memory aid for the ten"
    Group them rather than memorising a flat list:

    - **Input problems:** LLM01 (injection), LLM03 (poisoning), LLM05 (supply chain)
    - **Output problems:** LLM02 (output handling), LLM06 (disclosure), LLM09 (overreliance)
    - **Capability problems:** LLM07 (plugins), LLM08 (agency)
    - **Resource problems:** LLM04 (DoS), LLM10 (theft)

    Four groups of two or three is far easier to recall under exam pressure than ten
    independent items.

---

<div class="caisp-cards">
<a class="caisp-card" href="01-prompt-injection.md">
  <span class="caisp-kicker">Next · LLM01</span>
  <span class="caisp-card-title">Prompt Injection</span>
  <span class="caisp-card-text">The most important vulnerability in the list, and the hardest to fix.</span>
</a>
</div>
