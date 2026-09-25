# Certified AI Security Professional (cAISP)

A beginner-friendly, hands-on course in AI and LLM security, delivered as a searchable
course website with runnable labs.

**No ML background required. No GPU required. Every lab has an offline path.**

| | |
|---|---|
| **Chapters** | 7, plus orientation and a wrap-up |
| **Hands-on labs** | 29 |
| **Estimated time** | ~65 hours starting from zero |
| **Start reading** | [Home](docs/index.md) · [Start Here](docs/start-here/index.md) · [Syllabus](docs/start-here/syllabus.md) |

> [!IMPORTANT]
> This repository is for educational use. Read the [rules of engagement](#rules-of-engagement)
> before running any lab.

---

## Reading the course

The course is written for a [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
website, which adds navigation, search, tabbed instructions and styled callouts. The Markdown
files are readable directly on GitHub, but that formatting only renders on the website. There are
three ways to read it properly.

### Option A — Download the built site (nothing to install)

Every push to `main` builds and checks the site with GitHub Actions.

1. Open the **Actions** tab → **Course site** → the latest successful run.
2. Under **Artifacts**, download **`course-site-offline`** and unzip it.
3. Open `index.html` in your browser. Navigation and search work offline.

### Option B — Run it locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-docs.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>. Pages reload automatically as you edit them.

### Option C — Publish with GitHub Pages (off by default)

The workflow can deploy the site to
`https://def-sayan.github.io/Certified-AI-Security-Professional/`.

> [!WARNING]
> On GitHub Free, Pro and Team plans, a GitHub Pages site is **publicly accessible** even when
> the repository is private (and Pages on a private repository needs a paid plan). Only GitHub
> Enterprise Cloud can restrict a Pages site to signed-in members. Turn this on only if you are
> happy for the course to be public.

To enable it:

1. **Settings → Pages → Build and deployment → Source:** choose **GitHub Actions**.
2. **Settings → Secrets and variables → Actions → Variables:** add `DEPLOY_PAGES` with the value
   `true`.
3. Push to `main` (or re-run the **Course site** workflow). The URL appears on the run summary.

---

## Setting up the labs

```bash
pip install -r labs/requirements.txt
python labs/check_setup.py
```

You want to see **ALL GREEN** (or **READY (with warnings)**). Full instructions are in
[Start Here → Lab Environment Setup](docs/start-here/lab-environment.md).

> [!NOTE]
> Use **Python 3.11 or 3.12** (3.10 also works). Brand-new Python releases can lag behind
> PyTorch and Transformers.

---

## Course contents

| Chapter | Sections | Labs |
|---|:---:|:---:|
| [Start Here](docs/start-here/index.md) — orientation, syllabus, certification, lab setup, glossary | 6 | — |
| [1 — Introduction to AI Security](docs/chapter-01/index.md) | 7 | 1 |
| [2 — Understanding & Attacking LLMs](docs/chapter-02/index.md) | 6 | 10 |
| [3 — LLM Top 10 Vulnerabilities](docs/chapter-03/index.md) | 11 | 4 |
| [4 — AI Attacks & Defenses Using DevOps](docs/chapter-04/index.md) | 4 | 6 |
| [5 — Threat Modeling AI Systems](docs/chapter-05/index.md) | 6 | 1 |
| [6 — Supply Chain Attacks in AI](docs/chapter-06/index.md) | 5 | 5 |
| [7 — Emerging Threats, Governance & Compliance](docs/chapter-07/index.md) | 3 | 2 |
| [Wrap-Up](docs/wrap-up/index.md) | 1 | — |

Every chapter ends with a review page, a self-marked quiz and a readiness checklist.

---

## Running the labs

Every lab runs offline. Examples:

```bash
# Chapter 1 — chatbot (offline rule-based backend)
python labs/chapter-01/chatbot.py

# Chapter 2 — see text the way a model does
python labs/chapter-02/tokenizers.py --offline

# Chapter 2 — build a RAG system, then poison it
python labs/chapter-02/rag_system.py
python labs/chapter-02/rag_system.py --poison

# Chapter 2 — find a backdoor in a classifier
python labs/chapter-02/backdoor_detection.py

# Chapter 2 — hidden instructions in a web page
python labs/chapter-02/scraper_rag.py

# Chapter 3 — the prompt injection playground (8 levels)
python labs/chapter-03/injection_playground.py
python labs/chapter-03/injection_playground.py --demo

# Chapter 3 — measure a model's hallucination rate
python labs/chapter-03/hallucination_lab.py

# Chapter 4 — why loading a model is running a program
python labs/chapter-04/pickle_demo.py --all

# Chapter 4 — build guardrails, then measure their real coverage
python labs/chapter-04/guardrails.py --evaluate

# Chapter 5 — a full threat model, with coverage check
python labs/chapter-05/threat_model.py
python labs/chapter-05/threat_model.py --gaps

# Chapter 6 — scan models across five layers
python labs/chapter-06/model_scanner.py --scan-all

# Chapter 6 — sign a model, then watch one flipped bit break it
python labs/chapter-06/sign_verify.py

# Chapter 7 — build an agent, attack it, then harden it
python labs/chapter-07/agent.py --demo
python labs/chapter-07/agent.py --compare
```

A few labs (2.4 fine-tuning, 2.7 offline adversarial search, 2.10 speech-to-text and 4.5 LLM
Guard) have you write the script yourself; the full code is on the lab page.

---

## Project layout

```
.
├── mkdocs.yml                 # Site configuration and navigation
├── requirements-docs.txt      # Tooling to build the website
├── docs/                      # Course content (Markdown)
│   ├── index.md               # Home page
│   ├── start-here/            # Orientation, syllabus, certification, lab setup, glossary
│   ├── chapter-01/ … chapter-07/
│   ├── wrap-up/
│   └── assets/stylesheets/    # Theme overrides
├── labs/                      # Runnable lab code
│   ├── requirements.txt
│   ├── check_setup.py         # Environment smoke test
│   └── chapter-01/ … chapter-07/
├── hooks/html_links.py        # Resolves and validates links inside HTML cards
├── scripts/check_site.py      # Post-build checks (links, rendering)
└── .github/workflows/docs.yml # Build, validate, package, optionally deploy
```

<details>
<summary>Lab files by chapter</summary>

```
labs/
├── chapter-01/chatbot.py               # Lab 1.1 — three-backend chatbot
├── chapter-02/
│   ├── tokenizers.py                   # Lab 2.2
│   ├── summarizer.py                   # Lab 2.3
│   ├── scraper_rag.py                  # Lab 2.5
│   ├── rag_system.py                   # Lab 2.6
│   ├── sentiment.py                    # Lab 2.8
│   └── backdoor_detection.py           # Lab 2.9
├── chapter-03/
│   ├── injection_playground.py         # Lab 3.1 — 8-level injection game
│   └── hallucination_lab.py            # Lab 3.4 — measure fabrication rates
├── chapter-04/
│   ├── vulnerable_ai_app.py            # Lab 4.2 — 10 deliberate flaws (DO NOT DEPLOY)
│   ├── pickle_demo.py                  # Lab 4.3 — malicious pickle + scanning
│   └── guardrails.py                   # Lab 4.6 — guardrail layer + coverage eval
├── chapter-05/threat_model.py          # Lab 5.1 — STRIDE scaffold + risk rating
├── chapter-06/
│   ├── edit_demo.py                    # Lab 6.1 — surgical model editing (toy)
│   ├── model_scanner.py                # Lab 6.3 — 5-layer model scanner
│   └── sign_verify.py                  # Lab 6.5 — signing + tamper detection
└── chapter-07/agent.py                 # Labs 7.1/7.2 — agent + attack suite
```

</details>

---

## Editing the course

```bash
mkdocs serve                      # live preview while you write
mkdocs build --strict             # fails on broken links or config errors
python scripts/check_site.py      # checks the rendered HTML
```

CI runs the same checks on every push and pull request. A few conventions keep the site
rendering cleanly:

- Leave a blank line before and after every fenced code block, including inside callouts.
- Navigation cards are plain HTML. Link them to the source file (`href="02-basics-of-ai.md"`);
  the build hook turns that into the right URL and fails the build if the page does not exist.
- Inside raw HTML blocks such as `<dd>`, use HTML (`<em>`, `<code>`, `<a>`) rather than Markdown.

---

## Rules of engagement

This course teaches genuine offensive techniques against AI systems.

- Run these techniques **only** against the local labs provided here, systems you own, or
  systems where you hold **explicit written authorisation** to test.
- Do **not** target public AI services, production systems, or third-party infrastructure.
- Unauthorised testing is a crime in most jurisdictions, regardless of intent.

Every lab is self-contained and local **by design**, so you can build real offensive skill
without ever touching a system you do not own.

Offensive material with genuine dual-use potential (trojanised model generation, self-propagating
techniques, functional malware) is taught from a **detection and defence** perspective, using
non-weaponised samples. This matches how reputable AI security training handles the same topics
and costs nothing pedagogically — the assessed skill is recognition and mitigation.
