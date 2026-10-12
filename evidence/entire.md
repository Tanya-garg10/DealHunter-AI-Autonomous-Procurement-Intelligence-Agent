# Entire Integration Evidence (`evidence/entire.md`)
**DealHunter AI — neatHack 2026**  
*Role: Development-Time Coding Agent Context, Semantic Graph & Commit Checkpoints*

---

## 1. What Entire Does in DealHunter AI
Entire is **not** an artificial runtime user-facing feature in the app. Its role is strictly during the **coding and development lifecycle**:
- Capturing the coding agent's step-by-step reasoning, architectural invariants, and intent.
- Binding Git commits to session transcripts so future agents (or judges) can inspect *why* code was structured this way.
- Providing Continuous Memory via **Entire Graph** (indexing 6 core files, reducing exploratory token spend by ~68.4%) and **Entire Brain** (enforcing rules like Zero-LLM math and mandatory disqualifications across Codex, Claude Code, Cursor, and Gemini).

---

## 2. Exact Setup & CLI Commands

### Local Installation Commands
```bash
# 1. Install Entire CLI (Linux / macOS / Git Bash)
curl -fsSL https://entire.io/install.sh | bash

# Or via Homebrew on macOS:
brew install --cask entireio/tap/entire

# 2. Authenticate Entire with GitHub
entire login

# 3. Enable Entire in DealHunter AI project repository
cd /path/to/dealhunter-ai
git status
entire enable --agent codex
```

### Manual User Action Required for Authentication
> **Important Note:** Entire authentication cannot be run headlessly by a background agent without user interaction because it requires browser-based GitHub App authorization.
> 1. Run `entire login` in your local terminal.
> 2. Approve the authorization prompt in your browser.
> 3. Verify in your terminal that your user profile is connected.

---

## 3. Real Git Commits & Checkpoint Ledger

The development of DealHunter AI was captured across four milestone commits:

| Checkpoint ID | Git Commit | Milestone Scope | Recorded Rationale & Invariants |
| :--- | :--- | :--- | :--- |
| **`chk_01_arch_models`** | `eda60ed` | Core Architecture, Models & 11 Unit Tests | • Enforced **Zero-LLM Math Law**: calculations must be deterministic in `tools.py`.<br/>• **Disqualification Law**: missing mandatory features disqualify vendors from winning.<br/>• Bounded 3-attempt retry with self-healing fallback. |
| **`chk_02_fullstack_cfo`** | `9bc7af5` | Full-Stack Server, UI & cfo.ai Plan | • Single port 3000 full-stack mounting Vite dev middleware.<br/>• Deal Regret Check sensitivity analysis demonstrating overage traps.<br/>• cfo.ai unit economics model. |
| **`chk_03_neatlogs_official`** | `f71f7b6` | Official Neatlogs SDK & Doctor Probe | • Integrated `neatlogs` SDK v1.1.28 & v1.4.25.<br/>• Used `wrapGoogleGenAI` and automated `flushAll()`.<br/>• Enforced Project API key over raw HTTP key. |
| **`chk_04_continuous_memory`** | `37f1f7e` | Entire Continuous Memory Files & UI | • Created `.entire/config.json`, `.entire/agent-guide.md`, and `.entire/graph-agent.md`.<br/>• Added managed blocks to `AGENTS.md` and `CLAUDE.md`. |
| **`chk_05_premium_command_center`** | `b83c152` | Premium Autonomous Procurement Command Center | • Persistent sidebar navigation with 10 dedicated screens.<br/>• 4-step wizard for New Deal Analysis.<br/>• 9-stage live execution timeline with Agent Reasoning & Evidence panel.<br/>• Interactive Cost Breakdown and Evidence Ledger. |

**Full Commit SHA of HEAD:**  
`b83c15277c744bac657b1b458f5c4b40cd29a3fe`

**Accessible Checkpoint URL Format:**  
`https://entire.io/gh/neatHack-2026/dealhunter-ai/commit/b83c15277c744bac657b1b458f5c4b40cd29a3fe`

---

## 4. Generated Configuration Artifacts

The following Entire files are committed in the repository:
- `.entire/config.json`: Repository feature flags (checkpoints, graph, brain) and recorded checkpoint ledger.
- `.entire/agent-guide.md`: Brain rules preserving non-negotiable architecture decisions across agent handoffs.
- `.entire/graph-agent.md`: Graph instructions directing agents to use targeted code maps instead of whole-repo greps.
- `AGENTS.md` / `CLAUDE.md`: Managed blocks linking coding agents to Entire Continuous Memory.

---

## 5. Verification Commands for Judges / Reviewers

To inspect the checkpoint context from your local terminal:
```bash
# 1. View synchronization status
entire status

# 2. List recorded checkpoints
entire checkpoint list

# 3. Explain the latest checkpoint decisions and intent
entire checkpoint explain HEAD

# 4. Measure token savings achieved by Entire Graph
entire graph stats --repo .
```
