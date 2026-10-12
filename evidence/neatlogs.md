# Neatlogs Integration Evidence (`evidence/neatlogs.md`)
**DealHunter AI — neatHack 2026**  
*Role: Agent Run Tracing, Workflow Instrumenting, Retries & Observability*  
*Official Reference: https://docs.neatlogs.com*

---

## 1. Role of Neatlogs in DealHunter AI
While Entire tracks the *developer/coding-agent workflow*, **Neatlogs tracks the DealHunter AI runtime agent execution**:
- Every procurement investigation runs as a traceable workflow (`dealhunter-procurement`).
- Instruments 6 distinct execution stages: Planning, Vendor Lookup, Bounded Retries, Deterministic TCO Math, Deal Regret Sensitivity Analysis, and Verification.
- Wraps `@google/genai` calls with `neatlogs.wrapGoogleGenAI(ai)` for token and latency observability.
- Enforces strict buffer flushing via `neatlogs.flush()` / `neatlogs.flushAll()` before finishing.

---

## 2. Setup & Configuration

### Python Setup
```bash
pip install -U neatlogs
```

### TypeScript / Node Setup
```bash
npm install neatlogs
```

### Environment Variable Setup
Set the **Project API key** from Neatlogs (`Settings ➔ API keys`):
```bash
# Linux / macOS / Git Bash
export NEATLOGS_API_KEY="nl_live_your_project_key_here"

# Windows PowerShell
$env:NEATLOGS_API_KEY="nl_live_your_project_key_here"
```

> **Critical Key Distinction:**  
> Use the **Project API key** (the top key in Settings). If you use the bottom HTTP ingest key starting with `nlw_`, the Neatlogs SDK returns a `401 Unauthorized`.

---

## 3. Workflow Instrumentation Architecture

A complete DealHunter investigation instruments the following trace sequence:

| Step | Stage | Action / Tool | Status / Telemetry Captured |
| :--- | :--- | :--- | :--- |
| **`step_1`** | `PLANNING` | Formulate Explicit Plan | Records mission goal, usage budget, ceiling, and mandatory features. |
| **`step_2`** | `RECOVERING` *(if fault injected)* | `search_vendors` (Attempt 1) | Simulates HTTP 503 upstream timeout; records latency (~215ms) and error message. |
| **`step_3`** | `RECOVERING` *(if fault injected)* | `search_vendors` (Attempt 2) | Second bounded retry attempt with backoff; records latency (~180ms). |
| **`step_4`** | `RECOVERING` | `search_vendors` (Fallback) | Self-healing fallback to verified secondary snapshot; records status `RECOVERED`. |
| **`step_5`** | `ANALYZING` | `score_vendor_deal` | Deterministic cost math, overage calculation, and mandatory feature matching per vendor. |
| **`step_6`** | `ANALYZING` | `run_regret_sensitivity_check` | Sensitivity testing across 0.5x, 1.25x, 1.75x, and 2.5x volume; flags rank inversions. |
| **`step_7`** | `VERIFYING` | Mathematical Cross-Check | Independent recalculation of all TCO totals to ensure zero calculation discrepancy. |

---

## 4. Graceful Fallback & Honest Verification Status

- **With `NEATLOGS_API_KEY` configured:**  
  The app automatically initializes `neatlogs.init({ workflowName: 'dealhunter-procurement' })`, wraps model calls, flushes events to `app.neatlogs.com`, and displays `● LIVE CONNECTED` in the dashboard.
- **Without `NEATLOGS_API_KEY`:**  
  The application **does not crash or freeze**. It operates seamlessly in local fallback mode, displaying `○ STANDBY (Ready)` in the UI and preserving the full structured trace in `evidence/neatlogs-trace.json`.
- **Honesty Disclosure:** Remote dashboard verification requires the user to input their personal project key from `app.neatlogs.com`. We do not fabricate remote trace links or pretend remote delivery occurred if no key was provided.

---

## 5. Verification Commands & Diagnostics

To verify your Neatlogs connection using the official tools:

```bash
# 1. Built-in Doctor Probe Check (Verifies TRACE_VISIBLE & TRACE_FINALIZED)
python -m neatlogs doctor --probe

# 2. Inspect recorded traces via CLI
npm install --global neatlogs-cli@0.2.0
neatlogs profile set work --host 'https://app.neatlogs.com'
neatlogs profile use work
neatlogs auth login --device
neatlogs traces list --limit 5
```

A live local trace artifact is permanently preserved in:  
`evidence/neatlogs-trace.json`
