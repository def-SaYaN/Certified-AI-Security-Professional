---
tags:
  - Chapter 5
  - Threat Modeling
  - Risk
---

# 5.6 Rating and Managing Risks

!!! objective "In this section"
    - Why rating matters more than finding
    - A practical, defensible rating methodology
    - AI-specific factors that skew likelihood and impact
    - Turning ratings into an action plan

---

## Why rating matters more than finding

A thorough threat model on a real system produces thirty to sixty threats. You will never fix them
all, and you should not try.

!!! danger "An unprioritised threat list is close to useless"
    Hand an engineering team fifty unranked threats and one of two things happens: they fix the
    easiest ones (not the most important), or they are overwhelmed and fix none.

    **The value of a threat model is not the list. It is the ranked list.** Prioritisation is where
    security judgement actually lives, and it is the part that distinguishes a practitioner from
    someone who has read the OWASP page.

---

## The basic formula

> **Risk = Likelihood × Impact**

<dl class="caisp-terms" markdown>

<dt>Likelihood</dt>
<dd>How probable is it that this threat is realised? Driven by attacker capability required,
accessibility of the system, and existing controls.</dd>

<dt>Impact</dt>
<dd>How bad is it if it happens? Driven by data sensitivity, financial cost, safety, legal exposure,
and reputational damage.</dd>

</dl>

Simple — and the discipline is in applying it consistently.

---

## A practical rating methodology

You do not need an elaborate scheme. Here is one that works, is defensible, and takes minutes per
threat.

### Step 1 — Rate likelihood (1–5)

| Score | Level | Criteria |
|---|---|---|
| 5 | Almost certain | Trivial to do; no skill required; already happening |
| 4 | Likely | Easy; publicly known technique; weak or no controls |
| 3 | Possible | Requires some skill or specific conditions |
| 2 | Unlikely | Requires significant skill, access, or luck |
| 1 | Rare | Requires exceptional capability or insider access |

### Step 2 — Rate impact (1–5)

| Score | Level | Criteria |
|---|---|---|
| 5 | Severe | Safety harm, major breach, regulatory action, existential cost |
| 4 | Major | Significant data loss, substantial financial loss, serious reputational damage |
| 3 | Moderate | Limited data exposure, contained financial loss, some disruption |
| 2 | Minor | Small disruption, embarrassment, easily remediated |
| 1 | Negligible | Barely noticeable |

### Step 3 — Multiply and band

| Score | Band | Response |
|---|---|---|
| 20–25 | **Critical** | Fix before launch; escalate now |
| 12–19 | **High** | Fix this cycle |
| 6–11 | **Medium** | Plan and schedule |
| 3–5 | **Low** | Backlog; revisit |
| 1–2 | **Minimal** | Accept and record |

!!! tip "Rate as a group, and argue"
    Ratings made alone are one person's guess. Ratings made by a small group — security, engineering,
    and someone who understands the business impact — are far better, because **the argument is the
    analysis**.

    When two people rate the same threat 2 and 5, the discussion that follows almost always surfaces
    a fact nobody had written down.

---

## AI-specific factors that skew the ratings

Generic rating schemes mislead on AI systems unless you consciously adjust. Five factors to weigh:

<dl class="caisp-terms" markdown>

<dt>1. Likelihood is usually higher than instinct suggests</dt>
<dd>The payload for most LLM attacks is <strong>plain English</strong>. There is no exploit
development, no special tooling, no skill barrier. Anyone who can type can attempt prompt injection.

<strong>Rule of thumb:</strong> if a threat is realised through natural language against a public
interface, it is at least <strong>Likely (4)</strong>. Public AI features are probed within days of
launch.</dd>

<dt>2. Impact is driven by agency, not by the attack</dt>
<dd>The same injection scores impact 2 against a FAQ bot and impact 5 against a refund-issuing
assistant (LLM08). <strong>Rate impact by what the system can do, not by how clever the attack
is.</strong></dd>

<dt>3. Non-determinism affects likelihood</dt>
<dd>An attack that succeeds 5% of the time is <em>still</em> a vulnerability — an attacker simply
retries. Do not discount likelihood because a technique is unreliable; automated retry makes
unreliable attacks certain.</dd>

<dt>4. Detection difficulty should raise your rating</dt>
<dd>Traditional risk formulas often ignore detectability. For AI it matters enormously: a backdoor
(Lab 2.9) or poisoned corpus may persist undetected indefinitely. <strong>If you could not detect
it, weight the risk upward</strong> — undetected harm compounds.</dd>

<dt>5. Include non-security impacts</dt>
<dd>Fairness, misinformation, and safety harms are real impacts with legal consequences under
emerging regulation (Chapter 7). A model producing discriminatory output may not be a "breach", but
its impact can exceed one.</dd>

</dl>

!!! warning "The most common rating error in AI threat models"
    **Under-rating likelihood on injection-class threats**, because they feel unsophisticated.

    Sophistication is not the criterion — *ease* is. Prompt injection is the *easiest* attack class
    in modern computing. Rate it accordingly.

---

## Worked example

Applying this to the ACME support assistant from section 5.4:

| ID | Threat | L | I | Score | Band |
|---|---|:-:|:-:|:-:|---|
| T-01 | Indirect injection via customer tickets → unauthorised refund | 4 | 5 | **20** | Critical |
| T-02 | Retrieval ignores user permissions; confidential docs surfaced | 4 | 4 | **16** | High |
| T-03 | Tool calls act with app identity (confused deputy) | 4 | 4 | **16** | High |
| T-04 | Secrets in system prompt extracted | 5 | 3 | **15** | High |
| T-05 | Prompt logs contain PII with broad access | 3 | 4 | **12** | High |
| T-06 | Token-dense input inflates cost (denial of wallet) | 4 | 2 | **8** | Medium |
| T-07 | Model output rendered unescaped → XSS | 3 | 3 | **9** | Medium |
| T-08 | Third-party LLM provider outage | 3 | 3 | **9** | Medium |
| T-09 | Provider silently changes model version | 3 | 2 | **6** | Medium |
| T-10 | Corpus flooded to degrade retrieval | 2 | 2 | **4** | Low |

Now you have something a team can act on. Note T-01 tops the list not because it is the most
technically interesting, but because it is easy *and* consequential.

---

## Risk management strategies

For each rated risk, choose one treatment (section 5.2) and record it:

| ID | Treatment | Action | Owner | Residual |
|---|---|---|---|---|
| T-01 | **Avoid** | Remove autonomous refunds; human approves | Eng lead | 20 → 6 |
| T-02 | **Mitigate** | Permission filter at retrieval | Platform | 16 → 4 |
| T-03 | **Mitigate** | Authorise tool calls in user context | Platform | 16 → 4 |
| T-04 | **Avoid** | Remove secrets from prompt; enforce in code | Eng lead | 15 → 3 |
| T-05 | **Mitigate** | Redact on ingest; restrict access; 30-day retention | Data | 12 → 6 |
| T-06 | **Mitigate** | Token-based rate limits + spend alerts | Platform | 8 → 4 |
| T-07 | **Mitigate** | Escape output; static templates | Frontend | 9 → 3 |
| T-08 | **Transfer** | SLA with provider; fallback model | Procurement | 9 → 6 |
| T-09 | **Mitigate** | Pin model version; regression-test on change | Platform | 6 → 3 |
| T-10 | **Accept** | Monitor retrieval quality; revisit if abused | Security | 4 → 4 |

<dl class="caisp-terms" markdown>

<dt>Residual risk</dt>
<dd>The risk that <strong>remains after</strong> the treatment. Always record it — no control reduces
risk to zero, and pretending otherwise is how organisations convince themselves they are safe.</dd>

</dl>

!!! tip "Notice the pattern in the top four"
    Two are **Avoid** — removing the capability entirely — and they produce the largest risk
    reductions.

    This is Lab 3.1's lesson arriving through a completely different route: the strongest treatment
    for AI risk is frequently to *not have the capability*, rather than to guard it. When a process
    and a hands-on lab independently reach the same conclusion, that conclusion is worth
    internalising.

---

## Communicating the results

A threat model nobody reads changes nothing. Practical guidance:

- **Lead with the top five.** Nobody reads fifty rows. Put the criticals on page one.
- **State impact in business terms.** "Unauthorised refunds could be issued" beats "LLM08 excessive
  agency with confused-deputy conditions" for an executive audience — keep the technical framing for
  the appendix.
- **Always pair a threat with a recommendation.** Findings without fixes generate anxiety, not
  action.
- **Record accepted risks explicitly**, with who accepted them and when.
- **Show residual risk**, so the team can see what their work bought.
- **Date it and own it.** A threat model is a snapshot; say when it was taken and who to ask.

---

!!! question "Check your understanding"
    ??? success "Why is an unprioritised threat list nearly useless?"
        Teams cannot fix everything, so an unranked list means they fix the easiest items rather than
        the most important, or become overwhelmed and fix nothing. The ranking is where the security
        judgement lives.

    ??? success "Why should likelihood usually be rated high for injection-class threats?"
        Because the payload is plain English against a public interface — no exploit development, no
        tooling, no skill barrier. Ease, not sophistication, drives likelihood, and public AI
        features are probed within days.

    ??? success "What is residual risk and why record it?"
        The risk remaining after a treatment is applied. Recording it prevents the illusion that a
        control eliminated the risk, shows what the mitigation actually bought, and keeps the
        remaining exposure visible for future decisions.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-01-threat-model/" markdown>
<span class="caisp-kicker">Next · Lab 5.1</span>
### Threat Modeling an AI System
Do the whole thing yourself, end to end, with a scaffold tool.
</a>

</div>
