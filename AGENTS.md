# Agent Instructions for DealHunter AI

<!-- BEGIN ENTIRE MANAGED BLOCK: CONTINUOUS MEMORY -->
This repository uses **Entire Continuous Memory (Entire Graph + Entire Brain)**.
- Use `entire graph search` to find implementations and inspect code relationships without expensive grepping.
- Consult `.entire/agent-guide.md` and `.entire/graph-agent.md` for historical architectural decisions, prior rejected approaches, and repository invariants.
- When completing significant changes, ensure the work is recorded into an Entire Checkpoint linked to the corresponding Git commit:
  `entire checkpoint list`
  `entire checkpoint explain HEAD`
<!-- END ENTIRE MANAGED BLOCK: CONTINUOUS MEMORY -->

## Core Architecture Invariants:
1. Deterministic calculations in `tools.py` and `server.ts` for all financial figures.
2. Evidence-Driven Deal Scoring (TCO 35%, Features 25%, Evidence 20%, Reliability 15%, Flexibility 5%).
3. Bounded retry policy (max 3 attempts) with self-healing fallback.
4. Tracing streaming through official `neatlogs` SDK with `neatlogs.flush()`.
