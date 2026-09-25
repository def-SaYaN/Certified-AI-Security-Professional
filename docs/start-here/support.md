# Course Support (Mattermost)

You are not doing this alone. Every learner on this course gets **lifetime access** to the
course community on Mattermost — an open-source team-chat platform similar to Slack.

## Why a community matters for this course

Security is a social discipline. The reason is simple: the threat landscape changes faster
than any static document can. A model that was safe last month has a new jailbreak this
month. A library you depend on ships a malicious update. A new regulation lands. The people
in the community are your early-warning system for all of it.

Beyond news, the community is where you get unstuck. Almost every error you will hit in a
lab, someone else has already hit and solved. Searching the channel history is often faster
than debugging alone.

## Getting access

1. Use the invitation link provided with your course enrolment.
2. Create a Mattermost account (free).
3. Introduce yourself in `#introductions` — where you are starting from, what you want to
   get out of the course.
4. Turn on notifications for `#announcements` only. Mute the rest and check them when you
   have time, or you will drown.

## The channels

| Channel | Use it for |
|---|---|
| `#announcements` | Course updates, errata, new content, exam news. Read-only. |
| `#introductions` | Say hello. |
| `#general` | Anything that does not fit elsewhere. |
| `#chapter-01` … `#chapter-07` | Per-chapter questions. Ask in the right one. |
| `#labs-help` | "My lab won't run" — the busiest and most useful channel. |
| `#certification` | Exam preparation, booking, and (spoiler-free) experiences. |
| `#threat-intel` | Members sharing new AI security news, papers, and incidents. |
| `#careers` | Jobs, interviews, portfolio feedback. |
| `#off-topic` | The water cooler. |

---

## How to ask a question that actually gets answered

This is a real skill, and it is worth learning early because it pays off for your entire
career, not just this course. A good question gets a fast, useful answer. A vague question
gets silence or twenty follow-up questions.

!!! tip "The anatomy of a good technical question"
    A good question answers five things before anyone has to ask:

    1. **What are you trying to do?** The goal, not just the error.
    2. **What did you do?** The exact commands or code, copy-pasted.
    3. **What did you expect to happen?**
    4. **What actually happened?** The full error message, as text.
    5. **What have you already tried?** Shows effort and saves duplicate suggestions.

### A bad question

> "The chatbot lab doesn't work, help?"

Nobody can help with this. There is nothing to go on.

### The same question, asked well

> **Goal:** Running Lab 1.1 (chatbot), the offline `transformers` path.
>
> **Command:** `python labs/chapter-01/chatbot.py --offline`
>
> **Expected:** A chat prompt.
>
> **Actual:** It crashes immediately with:
> ```
> OSError: We couldn't connect to 'https://huggingface.co' to load this file
> ```
>
> **Tried:** I'm on the office VPN. I checked my internet works in the browser. I re-ran
> the setup smoke test and it passed. Python 3.11 on Windows 11.

That question will be answered in minutes, because the VPN detail plus the exact error
points straight at the cause (a proxy blocking the model download).

### Formatting matters

- Put code and errors in **code blocks** (triple backticks). Screenshots of text are hard
  to read and impossible to search.
- Paste the **full** error, not just the last line. The useful part is often in the middle.
- Never paste **secrets** — API keys, tokens, passwords. Redact them as `sk-...REDACTED`.

---

## Community etiquette

- **Search before asking.** Your question has probably been answered. Ten seconds of
  searching respects everyone's time, including yours.
- **Be patient and kind.** Everyone here was a beginner recently, including the people
  answering.
- **Pay it forward.** Once you are a chapter or two ahead, answer questions in the chapters
  you have finished. Teaching is the fastest way to cement your own understanding, and it
  is how the community stays alive.
- **Keep it legal and ethical.** Do not ask for or share help attacking systems you do not
  own. Do not post working malware. The [rules of engagement](index.md) apply in the
  community too. Moderators enforce this.
- **Stay on the right side of exam integrity.** Discussing concepts and study strategy is
  encouraged. Sharing exam answers or live exam content is not, and it gets people banned.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../glossary/" markdown>
<span class="caisp-kicker">Reference</span>
### Glossary
Every term, one sentence each.
</a>

<a class="caisp-card" href="../lab-environment/" markdown>
<span class="caisp-kicker">Now do this</span>
### Lab Environment Setup
Get your machine ready for Chapter 1.
</a>

</div>
