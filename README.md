# Certified AI Security Professional (cAISP)

A beginner-friendly, hands-on course in AI and LLM security, delivered as a searchable
web-based course site with runnable labs.

**No ML background required. No GPU required. Every lab has an offline path.**

---

## Quick start

### 1. View the course site

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install mkdocs-material
mkdocs serve
```

Open <http://127.0.0.1:8000>.

### 2. Set up the labs

```bash
pip install -r labs/requirements.txt
python labs/check_setup.py
```

You want to see **READY**. Full instructions are on the site under
**Start Here → Lab Environment Setup**.

!!! note
    Use **Python 3.11 or 3.12**. Newer releases often lack PyTorch/Transformers wheels.

---

## Project layout

```
.
├── mkdocs.yml              # Site configuration and navigation
├── docs/                   # Course content (Markdown)
│   ├── index.md            # Home page
│   ├── start-here/         # Orientation, syllabus, certification, lab setup, glossary
│   ├── chapter-01/         # Introduction to AI Security  (7 sections + 1 lab)
│   ├── chapter-02/         # Understanding & Attacking LLMs (6 sections + 10 labs)
│   ├── chapter-03/         # LLM Top 10 Vulnerabilities (11 sections + 4 labs)
│   ├── chapter-04/         # AI Attacks & Defenses Using DevOps (4 sections + 6 labs)
│   ├── chapter-05/         # Threat Modeling AI Systems (6 sections + 1 lab)
│   ├── chapter-06/         # Supply Chain Attacks in AI (5 sections + 5 labs)
│   ├── chapter-07/         # Emerging Threats, Governance & Compliance (3 sections + 2 labs)
│   └── wrap-up/            # Course wrap-up
└── labs/                   # Runnable lab code
    ├── requirements.txt
    ├── check_setup.py      # Environment smoke test
    ├── chapter-01/
    │   └── chatbot.py      # Lab 1.1 — three-backend chatbot
    ├── chapter-02/
    │   ├── tokenizers.py           # Lab 2.2
    │   ├── summarizer.py           # Lab 2.3
    │   ├── scraper_rag.py          # Lab 2.5
    │   ├── rag_system.py           # Lab 2.6
    │   ├── sentiment.py            # Lab 2.8
    │   └── backdoor_detection.py   # Lab 2.9
    ├── chapter-03/
    │   ├── injection_playground.py # Lab 3.1 — 8-level injection game
    │   └── hallucination_lab.py    # Lab 3.4 — measure fabrication rates
    ├── chapter-04/
    │   ├── vulnerable_ai_app.py    # Lab 4.2 — 10 deliberate flaws (DO NOT DEPLOY)
    │   ├── pickle_demo.py          # Lab 4.3 — malicious pickle + scanning
    │   └── guardrails.py           # Lab 4.6 — guardrail layer + coverage eval
    ├── chapter-05/
    │   └── threat_model.py         # Lab 5.1 — STRIDE scaffold + risk rating
    ├── chapter-06/
    │   ├── edit_demo.py            # Lab 6.1 — surgical model editing (toy)
    │   ├── model_scanner.py        # Lab 6.3 — 5-layer model scanner
    │   └── sign_verify.py          # Lab 6.5 — signing + tamper detection
    └── chapter-07/
        └── agent.py                # Labs 7.1/7.2 — agent + attack suite
```

---

## Course status

| Chapter | Sections | Labs | Status |
|---|---|---|---|
| Start Here | 6 pages | — | Complete |
| 1 — Introduction to AI Security | 7 | 1 | Complete |
| 2 — Understanding & Attacking LLMs | 6 | 10 | Complete |
| 3 — LLM Top 10 Vulnerabilities | 11 | 4 | Complete |
| 4 — AI Attacks & Defenses Using DevOps | 4 | 6 | Complete |
| 5 — Threat Modeling AI Systems | 6 | 1 | Complete |
| 6 — Supply Chain Attacks in AI | 5 | 5 | Complete |
| 7 — Emerging Threats, Governance & Compliance | 3 | 2 | Complete |
| Wrap-Up | 1 | — | Complete |

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
non-weaponized samples. This matches how reputable AI security training handles the same topics
and costs nothing pedagogically — the assessed skill is recognition and mitigation.

---

## Building the site for deployment

```bash
mkdocs build          # outputs to site/
```

The `site/` directory is a static site deployable to any web host, GitHub Pages, or S3.
