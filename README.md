# DealHunter AI — Autonomous Procurement Intelligence Agent

> **Tagline:** *Don't just find a deal. Prove it's the right deal.*  
> Built for **neatHack 2026**

DealHunter AI helps startups and growing engineering teams make smarter, provable procurement decisions. Users define their purchasing requirements, budget constraints, and volume projections. The agent formulates an explicit research plan, fetches vendor specifications, deterministically calculates total cost of ownership (TCO) and usage overage charges, audits source evidence freshness, executes bounded failure recovery, runs sensitivity stress-testing ("Deal Regret Check"), and generates an explainable procurement report.

---

## 🏆 Key Innovations

1. **Deterministic Financial Math (Zero LLM Arithmetic):**
   LLMs are notorious for hallucinating financial arithmetic. DealHunter computes all monthly fees, included volume allowances, tiered overage fees, annual commitment discounts, and total cost of ownership (TCO) deterministically in Python/TypeScript.
2. **Evidence-Driven Deal Score:**
   Configurable, normalized scoring architecture:
   - **Total Cost of Ownership (TCO):** 35%
   - **Feature Compatibility:** 25% (Mandatory checklist failures disqualify vendors from winning)
   - **Evidence Quality & Freshness:** 20% (Penalizes unverified forum posts, stale timestamps, missing SLA audits)
   - **Reliability & Support SLA:** 15%
   - **Contract Flexibility:** 5%
3. **Deal Regret Check (Sensitivity Analysis):**
   Unveils the "Headline Trap" where cheap starter plans ($49/mo) spike to thousands in overages at scale. Tests 0.5x, 1.25x, 1.75x, and 2.5x volume scenarios to alert buyers when rank inversions occur.
4. **Resilient Bounded Retry & Self-Healing:**
   Features a controlled demonstration toggle that simulates upstream HTTP 503 gateway timeouts, enforces a strict 3-attempt bounded retry policy with backoff, and self-heals by falling back to a validated secondary snapshot.
5. **Human-in-the-Loop Safeguard:**
   If zero vendors meet mandatory requirements, or if the recommended winner relies on unverified evidence, the agent automatically transitions to `NEEDS_REVIEW` and halts any external purchasing action.

---

## 🛠️ Technology Stack & Integrations

- **Agent Engine & Calculations:** Python 3.10+ (Standard Library, typed data models, deterministic cost tools)
- **Frontend & Full-Stack Interface:** Streamlit (`app.py`) + React 19, Tailwind CSS v4, Lucide icons, and Express full-stack proxy (`server.ts`)
- **Tracing & Observability:** [neatlogs](https://docs.neatlogs.com) integration streaming agent run IDs, tool calls, latencies, and verification steps
- **Context & Checkpoint Management:** [Entire](https://entire.io) workflow preserving coding-agent context records and Git checkpoints
- **Financial Model & Unit Economics:** [cfo.ai](https://cfo.ai/neathacks) business plan with 99% gross margin and 14-month runway model
- **AI Reasoning:** Gemini 3.8 Flash (`@google/genai`) for executive synthesis and qualitative risk narratives

---

## 📁 Repository Structure

```
.
├── agent.py               # Autonomous agent state machine, retry policies, and orchestration
├── app.py                 # Streamlit web application interface
├── config.py              # Environment variables, default weights, and paths
├── demo-script.md         # Turn-by-turn presentation script for hackathon judging
├── evidence/
│   ├── business-plan.md   # Complete cfo.ai business plan & unit economics
│   ├── entire-checkpoint.md # Entire context records, workflow, and git checkpoints
│   └── neatlogs-trace.json # Live agent execution trace exported for audit
├── models.py              # Typed data structures (ProcurementMission, DealScore, etc.)
├── package.json           # Node / Vite / Express dependencies
├── server.ts              # Express API proxy routes and Vite middleware runner
├── src/
│   ├── App.tsx            # DealHunter interactive dark navy dashboard
│   ├── index.css          # Tailwind CSS styling
│   └── main.tsx           # React entry point
├── tests/
│   └── test_agent.py      # 11 unit tests covering all Section 14 requirements
├── tools.py               # Deterministic TCO math, feature matching, evidence audit
└── vendors.json           # Structured sample vendor fixtures with pricing & evidence
```

---

## 🚀 Getting Started

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key variables:
- `GEMINI_API_KEY`: API key for Gemini models (optional; system falls back smoothly if absent)
- `NEATLOGS_API_KEY`: API key for live remote streaming to [neatlogs.com](https://neatlogs.com)
- `NEATLOGS_PROJECT_ID`: Default project identifier (`dealhunter-neathack-2026`)

### 2. Running the Full-Stack Web Application
The application is pre-configured with Node/TypeScript and Python:
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

### 3. Running via Streamlit (Python Native)
To launch the native Streamlit UI:
```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

### 4. Running the Test Suite
All 11 mandatory test cases run via standard Python `unittest`:
```bash
python3 -m unittest discover tests
```
Output:
```
...........
----------------------------------------------------------------------
Ran 11 tests in 0.110s

OK
```

---

## 🧪 Tested Capabilities (Section 14 Compliance)

1. ✅ Monthly and annual cost calculation (base discounts, included allowances, setup fees)
2. ✅ Usage overage charges ($0.015/unit vs $0.002/unit)
3. ✅ Mandatory feature verification (disqualification of vendors missing SSO/SAML)
4. ✅ Budget ceiling eligibility enforcement
5. ✅ Evidence quality auditing (penalizing unverified forum sources and stale dates)
6. ✅ Missing or sparse vendor fields gracefully handled without crashes
7. ✅ Bounded retry policy (bounded at 3 attempts without infinite loops)
8. ✅ Self-healing recovery from simulated network timeouts
9. ✅ No-eligible-vendor scenario (halts and flags `NEEDS_REVIEW`)
10. ✅ Deal Regret Check sensitivity analysis across 0.5x - 2.5x volume
11. ✅ Comprehensive procurement report artifact export (JSON and CSV)

---

## 📊 Integrations Summary

- **neatlogs Integration:** Live trace logging is verified and exported in `evidence/neatlogs-trace.json`. Set `NEATLOGS_API_KEY` to stream live to the neatlogs dashboard.
- **Entire Integration:** Documented in `evidence/entire-checkpoint.md` with Git commit `eda60ed`.
- **cfo.ai Integration:** Detailed financial model in `evidence/business-plan.md` showing $0.0030 COGS per investigation, 99% gross margins, and 14-month pre-seed runway.
