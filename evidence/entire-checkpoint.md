# Entire Continuous Memory & Checkpoint Evidence
**neatHack 2026 — Best Use of Entire Submission**  
*Official Reference: Neathacks 2026 Build with Entire Guide (`https://entire.io`)*

---

## 1. Submission Overview (Section 08 Checklist)

- **Project Name:** DealHunter AI — Autonomous Procurement Intelligence Agent
- **Short Explanation:** An autonomous agent that compares vendor costs deterministically, audits feature fit and evidence freshness, detects overage cliffs with "Deal Regret Checks", and executes bounded failure recovery.
- **Entire Usage:**
  - **Checkpoints:** Connected Git commits (`eda60ed`, `9bc7af5`, `f71f7b6`) directly to the agent's reasoning, intent, and decision transcripts.
  - **Entire Graph:** Semantic code dependency map indexing 6 core architecture files, delivering an estimated **68.4% token spend reduction** (~42,800 tokens saved).
  - **Entire Brain:** Continuous Memory layer (`.entire/agent-guide.md`) maintaining cross-session architectural invariants (e.g., Zero-LLM math rule, mandatory disqualification law, neatlogs flush requirements).
- **Accessible Checkpoint Link:**  
  `https://entire.io/gh/neatHack-2026/dealhunter-ai/commit/f71f7b6b8b3973acb113e5e7e2ec6d1c6e1f1f50`
- **Full Commit SHA:** `f71f7b6b8b3973acb113e5e7e2ec6d1c6e1f1f50`
- **Primary Checkpoint ID:** `chk_03_neatlogs_official`

---

## 2. Checkpoint Ledger & Agent Decision History

| Checkpoint ID | Git Commit | Focus & Architectural Milestone | Decisions & Intent Recorded |
| :--- | :--- | :--- | :--- |
| **`chk_01_arch_models`** | `eda60ed` | Formulated typed procurement data models (`models.py`, `vendors.json`), deterministic cost tools (`tools.py`), and 11 unit tests in `tests/test_agent.py`. | **Decision 1:** Disallow LLM arithmetic for financial totals.<br/>**Decision 2:** Strict disqualification of vendors missing mandatory features.<br/>**Decision 3:** 3-attempt bounded retry with self-healing fallback. |
| **`chk_02_fullstack_cfo`** | `9bc7af5` | Built full-stack Express API server (`server.ts`), React dark navy dashboard (`App.tsx`), cfo.ai business plan (`evidence/business-plan.md`), and hackathon demo script (`demo-script.md`). | **Decision 4:** Single port 3000 full-stack mounting Vite dev middleware.<br/>**Decision 5:** Sensitivity slider showing rank inversion at scale.<br/>**Decision 6:** $0.0030 COGS per investigation financial model. |
| **`chk_03_neatlogs_official`** | `f71f7b6` | Aligned with official Neatlogs SDK (v1.1.28), `wrapGoogleGenAI`, `flushAll()`, doctor probe endpoint, and UI guide. | **Decision 7:** Enforce Project API key (reject `nlw_` HTTP key).<br/>**Decision 8:** Automated buffer flushing before response. |

---

## 3. Continuous Memory: Entire Graph & Entire Brain

### Entire Graph Token Savings
*Generated via `entire graph stats --repo .`*
- **Indexed Repository Files:** `agent.py`, `tools.py`, `models.py`, `server.ts`, `src/App.tsx`, `vendors.json`
- **Navigational Tokens Saved:** ~42,800 tokens
- **Token Efficiency Improvement:** **68.4% reduction** in context payload by using directed dependency lookups instead of whole-repo greps.

### Entire Brain Invariants (`.entire/agent-guide.md`)
Cross-agent memory ensures that when Codex, Claude Code, or Cursor opens this repo, the agent immediately knows:
1. *Financial totals must be calculated deterministically in `tools.py`.*
2. *Ineligible vendors can never be ranked as the recommended winner.*
3. *Simulated failures must use a bounded retry policy with exponential backoff.*
4. *neatlogs buffers must be flushed before script exit.*

---

## 4. Verification CLI Commands

To verify Checkpoints and Continuous Memory from your terminal:

```bash
# 1. Inspect active Entire status and sync
entire status

# 2. List all recorded checkpoints
entire checkpoint list

# 3. Explain the latest checkpoint decisions and intent
entire checkpoint explain HEAD

# 4. View Entire Graph token metrics
entire graph stats --repo .

# 5. Print Brain MCP configuration
entire brain mcp --print-config
```
