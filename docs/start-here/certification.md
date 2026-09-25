# Certification Guide

## Why bother with the certification

You can learn everything in this course and never sit an exam. The knowledge is the point;
the certificate is a signal. But the signal is useful for three reasons:

1. **It forces completeness.** Knowing there is an exam changes how you read. You stop
   skimming the chapter on governance because "it's just paperwork" and you engage with
   it, which is good, because in a real job the governance chapter is the one that gets
   you budget.
2. **It is a hiring shorthand.** AI security is new enough that most hiring managers
   cannot easily evaluate a candidate's depth. A credential that maps to a known syllabus
   gives them a starting point.
3. **It creates a deadline.** Self-paced courses have a completion problem. A booked exam
   date is the most effective study aid ever invented.

!!! note "The certificate is not the skill"
    Be honest with yourself about the difference. Someone who memorised the OWASP LLM Top
    10 list can pass a multiple-choice question. Someone who has actually built a RAG
    system and then poisoned its retrieval corpus can do the job. Aim for the second, and
    the first comes free.

---

## Exam format

The certification exam is **practical and scenario-driven**. It is not a pure memory test.

| Aspect | Detail |
|---|---|
| Format | Mixed: multiple-choice, scenario analysis, and hands-on practical tasks |
| Duration | Typically a fixed window (commonly 12–24 hours for practical exams of this type) |
| Environment | A provided lab environment, accessed remotely |
| Open book | Generally yes — you may consult documentation and your own notes |
| Attempts | Usually one included attempt, with paid retakes |
| Result | Pass/fail against a score threshold, plus a digital badge on success |

!!! warning "Confirm the current details with your provider"
    Exam formats, durations, pricing, and retake policies change. The table above reflects
    the typical shape of a practical AI security certification. **Always check the current
    official exam guide from whoever is issuing your certificate** before you book. Do not
    plan your preparation around this page alone.

### What "open book" really means

Open book exams are harder than closed book exams, not easier. Here is why.

A closed-book exam tests recall, so it must ask questions whose answers are recallable —
definitions, lists, facts. An open-book exam knows you can look up any fact in thirty
seconds, so it does not ask for facts. It asks you to *apply* things:

> "Here is an architecture diagram for a customer-support assistant that retrieves from an
> internal knowledge base and can issue refunds via an API. Identify the three highest-risk
> threats, justify your ranking, and propose a mitigation for each."

You cannot look that up. You can only answer it if you have internalised the material and
practised applying it. Which is what the labs are for.

---

## What gets tested

Weighting varies by provider, but a syllabus like this one typically distributes roughly
as follows:

| Domain | Approx. weight | Maps to |
|---|---:|---|
| AI/ML fundamentals and terminology | 10% | Chapter 1 |
| LLM architecture and attack tactics | 20% | Chapter 2 |
| OWASP LLM Top 10 — identify, exploit, mitigate | 25% | Chapter 3 |
| Secure AI development and DevSecOps tooling | 15% | Chapter 4 |
| Threat modeling AI systems | 12% | Chapter 5 |
| AI supply chain security | 12% | Chapter 6 |
| Governance, standards, and regulation | 6% | Chapter 7 |

Notice that **Chapter 3 alone is a quarter of the exam**, and Chapters 2 and 3 together
are nearly half. Budget your study time accordingly. Also notice that Chapter 7 is the
smallest slice but is not zero — do not skip it.

### The kinds of questions you should expect

**Recall (easy, ~20% of questions)**

> Which OWASP LLM Top 10 category covers an LLM being given more permissions than its
> task requires?

**Application (the bulk, ~50%)**

> A developer sanitises user input for SQL injection before passing it to an LLM, then
> renders the LLM's response directly into an HTML page. Which vulnerability class is
> still present, and why does the input sanitisation not prevent it?

**Analysis and judgement (~20%)**

> Given this data flow diagram, which trust boundary is crossed by the retrieval step, and
> what STRIDE categories apply at that boundary?

**Practical / hands-on (~10%, but high-value)**

> Using the provided environment, extract the system prompt from the chatbot at
> `http://target.lab:8080` and document your method.

---

## A realistic preparation plan

### Phase 1 — Learn (the bulk of your time)

Work through Chapters 1 to 7 in order. Do every lab. Do not attempt to "study for the
exam" during this phase; just learn the material properly. Rushing here to save time
guarantees you spend that time twice later.

For each chapter:

- [ ] Read all concept sections
- [ ] Complete every hands-on lab, running the code yourself
- [ ] Attempt at least one "break it yourself" challenge per lab
- [ ] Complete the end-of-chapter review and quiz
- [ ] Write a half-page summary **in your own words** before moving on

That last point matters more than it looks. The act of compressing a chapter into your own
words is where understanding is manufactured.

### Phase 2 — Consolidate (about a week)

Now study for the exam specifically.

**Build a one-page cheat sheet per chapter.** Not copied from the course — written from
memory, then corrected against the course. The correction step shows you exactly what you
do not know.

**Drill the frameworks.** You should be able to produce these from memory:

- The OWASP LLM Top 10, in order, with a one-line description of each
- The STRIDE categories and what each maps to
- The MITRE ATLAS tactics in kill-chain order
- The four NIST AI RMF functions

**Re-run the labs from scratch.** Delete your working directory and rebuild the three or
four most important labs without looking at the walkthrough. Struggling here is
information, not failure.

**Do a full mock scenario.** Take any real product you use that has an AI feature — a
support chatbot, an email assistant, a code completion tool. Threat model it end to end
on paper: draw the DFD, apply STRIDE, pull threats from ATLAS and the OWASP list, rate the
risks, propose mitigations. Give yourself two hours. This single exercise exercises
Chapters 3, 5, 6 and 7 simultaneously and is the closest thing to the real exam.

### Phase 3 — Sit the exam

**The day before:** do not cram. Re-read your own cheat sheets once, then stop. Confirm
your exam environment works — VPN, browser, credentials, whatever the provider requires.
Sleep.

**During a practical exam:** the most common failure is not lack of knowledge, it is poor
process.

- **Read the whole exam first** before touching anything. Know what is coming.
- **Take notes as you go**, including failed attempts. Many practical exams award marks
  for methodology, and a documented dead end shows methodology.
- **Screenshot everything** the moment you achieve it. Do not tell yourself you will
  reproduce it later for the report. You will not.
- **Watch the clock and move on.** A question you cannot crack in 45 minutes is usually
  one you cannot crack in 90. Bank the easy marks first, return to the hard one after.
- **Write the report as you go**, not at the end. Candidates routinely complete all the
  technical work and then fail on an unwritten report.

---

## Common reasons people fail

Worth knowing in advance, because all of these are avoidable.

<dl class="caisp-terms" markdown>

<dt>They read instead of doing</dt>
<dd>The most common failure by a wide margin. The labs are not optional enrichment; they
are where the tested skill is built.</dd>

<dt>They skipped the "boring" chapters</dt>
<dd>Governance and threat modeling feel less exciting than prompt injection. They are
roughly 18% of the exam combined, and they are the chapters where careless candidates
leave easy marks on the table.</dd>

<dt>They can exploit but cannot mitigate</dt>
<dd>Attacking is more fun, so people practise it more. But almost every exam question that
asks you to find a flaw also asks you to fix it. For every attack you learn, learn the
defence in the same session.</dd>

<dt>They ran out of time on the report</dt>
<dd>Purely a process failure. Document continuously.</dd>

<dt>They memorised lists without understanding</dt>
<dd>Knowing that "LLM01 is Prompt Injection" earns you one easy mark. Being unable to
recognise an indirect prompt injection in an unfamiliar architecture loses you the
five-mark scenario question.</dd>

</dl>

---

## Am I ready? A self-check

Do not book the exam until you can honestly tick most of these.

- [ ] I can explain the difference between AI, ML, and deep learning to a non-technical
      person without using jargon.
- [ ] I have built a working chatbot and a working RAG system myself.
- [ ] I can list the OWASP LLM Top 10 from memory and give a real example of each.
- [ ] I have successfully performed a prompt injection against something I built.
- [ ] I can explain why indirect prompt injection is harder to defend against than direct.
- [ ] I can draw a data flow diagram for an LLM application and mark its trust boundaries.
- [ ] I can apply STRIDE to each element of that diagram.
- [ ] I know why loading an untrusted pickle file is dangerous, and I have scanned one.
- [ ] I can explain what an SBOM is and why model signing matters.
- [ ] I can name the major AI governance frameworks and say what each is for.
- [ ] For every attack in this course, I can state at least one concrete mitigation.

If you can tick nine or more, book it.

---

<div class="caisp-cards">
<a class="caisp-card" href="lab-environment.md">
  <span class="caisp-kicker">Next — do not skip</span>
  <span class="caisp-card-title">Lab Environment Setup</span>
  <span class="caisp-card-text">Install everything and run the smoke test.</span>
</a>
<a class="caisp-card" href="support.md">
  <span class="caisp-kicker">Then</span>
  <span class="caisp-card-title">Course Support</span>
  <span class="caisp-card-text">Join the community before you get stuck.</span>
</a>
</div>
