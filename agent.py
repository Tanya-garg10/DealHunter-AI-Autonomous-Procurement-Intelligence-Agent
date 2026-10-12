"""
DealHunter AI - Autonomous Procurement Intelligence Agent
State Machine, Bounded Retry, Evidence-Driven Decision Engine,
neatlogs Tracing, and Verification Layer.
"""

import os
import json
import uuid
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple

from models import (
    AgentStatus,
    ProcurementMission,
    DealScore,
    CostBreakdown,
    RegretSensitivityResult,
    AgentTraceStep,
    ProcurementReport
)
from tools import (
    execute_bounded_retry_lookup,
    score_vendor_deal,
    run_regret_sensitivity_check,
    calculate_cost_breakdown,
    check_feature_compatibility,
    validate_evidence_quality
)
from config import (
    NEATLOGS_API_KEY,
    NEATLOGS_PROJECT_ID,
    GEMINI_API_KEY,
    LLM_MODEL_NAME,
    EVIDENCE_DIR
)

# Optional import of neatlogs
try:
    import neatlogs
    HAS_NEATLOGS_SDK = True
except ImportError:
    HAS_NEATLOGS_SDK = False


class DealHunterAgent:
    """
    Autonomous Procurement Agent implementing the 10-step neatHack 2026 workflow:
    1. Mission intake & constraints
    2. Explicit research plan
    3. Tool invocation with bounded retry
    4. Deterministic TCO calculation
    5. Feature compatibility validation
    6. Evidence & contract risk auditing
    7. Failure recovery execution
    8. Deal Regret Check (sensitivity testing)
    9. Transparent deal scoring & ranking
    10. Explainable procurement report & independent verification
    """

    def __init__(self, mission: ProcurementMission):
        self.mission = mission
        self.run_id = f"dh_run_{uuid.uuid4().hex[:10]}"
        self.status = AgentStatus.IDLE
        self.trace_steps: List[AgentTraceStep] = []
        self.neatlogs_client = None
        self.neatlogs_session_id = None
        self._init_neatlogs()

    def _init_neatlogs(self):
        """Initializes neatlogs integration if credentials exist according to official SDK guide."""
        self.neatlogs_active = False
        if HAS_NEATLOGS_SDK and NEATLOGS_API_KEY:
            try:
                neatlogs.init(
                    api_key=NEATLOGS_API_KEY,
                    workflow_name="dealhunter-procurement"
                )
                self.neatlogs_active = True
                print("[neatlogs] Initialized SDK for workflow: dealhunter-procurement")
            except Exception as e:
                print(f"[neatlogs] Warning: Failed to initialize SDK: {e}")

    def _log_trace(
        self,
        stage: str,
        action: str,
        tool_name: Optional[str],
        input_data: Dict[str, Any],
        output_summary: str,
        status: str = "SUCCESS",
        duration_ms: float = 1.0,
        evidence_verified: bool = True
    ):
        """Records an execution step for full observability and neatlogs streaming."""
        step = AgentTraceStep(
            step_id=f"step_{len(self.trace_steps) + 1}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=stage,
            action=action,
            tool_name=tool_name,
            input_data=input_data,
            output_summary=output_summary,
            status=status,
            duration_ms=duration_ms,
            evidence_verified=evidence_verified
        )
        self.trace_steps.append(step)

        # Send to neatlogs if client is available
        if self.neatlogs_client and self.neatlogs_session_id:
            try:
                self.neatlogs_client.log_event(
                    session_id=self.neatlogs_session_id,
                    event_type=stage.lower(),
                    payload={
                        "step_id": step.step_id,
                        "action": action,
                        "tool": tool_name,
                        "status": status,
                        "summary": output_summary,
                        "latency_ms": duration_ms
                    }
                )
            except Exception:
                pass

    def run(self) -> ProcurementReport:
        """Executes the complete autonomous procurement workflow."""
        start_time = time.time()

        # Step 1: PLANNING
        self.status = AgentStatus.PLANNING
        plan_summary = (
            f"Formulated 5-stage procurement plan for goal: '{self.mission.goal}'. "
            f"Usage budget: {self.mission.monthly_usage:,} ops/mo @ ${self.mission.monthly_budget:.2f}/mo. "
            f"Mandatory requirements: {', '.join(self.mission.required_features) if self.mission.required_features else 'None'}. "
            f"Fault-tolerance injection flag: {self.mission.simulate_lookup_failure}."
        )
        self._log_trace(
            stage="PLANNING",
            action="Create Explicit Research Plan",
            tool_name=None,
            input_data={"mission": self.mission.goal, "budget": self.mission.monthly_budget},
            output_summary=plan_summary,
            status="SUCCESS",
            duration_ms=round((time.time() - start_time) * 1000, 2)
        )

        # Step 2: RESEARCHING (with fault simulation & bounded retry)
        self.status = AgentStatus.RESEARCHING
        research_start = time.time()
        vendors, retry_logs = execute_bounded_retry_lookup(
            simulate_failure=self.mission.simulate_lookup_failure
        )

        for rlog in retry_logs:
            if rlog["status"] == "FAILED":
                self.status = AgentStatus.RECOVERING
                self._log_trace(
                    stage="RECOVERING",
                    action=f"Bounded Retry Attempt {rlog['attempt']}",
                    tool_name="search_vendors",
                    input_data={"attempt": rlog["attempt"], "simulate_failure": self.mission.simulate_lookup_failure},
                    output_summary=rlog["message"],
                    status="FAILED",
                    duration_ms=rlog["duration_ms"],
                    evidence_verified=False
                )
            elif rlog["status"] == "RECOVERED":
                self.status = AgentStatus.RESEARCHING
                self._log_trace(
                    stage="RECOVERING",
                    action="Self-Healing Fallback",
                    tool_name="search_vendors",
                    input_data={"attempt": rlog["attempt"]},
                    output_summary=rlog["message"],
                    status="RECOVERED",
                    duration_ms=rlog["duration_ms"],
                    evidence_verified=True
                )
            else:
                self._log_trace(
                    stage="RESEARCHING",
                    action="Lookup Vendors from Registry",
                    tool_name="search_vendors",
                    input_data={"count": len(vendors)},
                    output_summary=rlog["message"],
                    status="SUCCESS",
                    duration_ms=rlog["duration_ms"],
                    evidence_verified=True
                )

        # Step 3: ANALYZING (Cost Math + Evidence Audit + Feature Compatibility)
        self.status = AgentStatus.ANALYZING
        scored_vendors: List[DealScore] = []
        for v in vendors:
            v_start = time.time()
            score = score_vendor_deal(v, self.mission, vendors)
            scored_vendors.append(score)

            status_str = "SUCCESS" if score.is_eligible else "INELIGIBLE"
            audit_msg = (
                f"Evaluated {v['name']}: Total Monthly ${score.cost_breakdown.total_monthly_cost:.2f}, "
                f"Annual TCO ${score.cost_breakdown.total_annual_tco:.2f}, "
                f"Feature Compatibility {score.feature_score}%, Evidence Quality {score.evidence_score}%, "
                f"Composite Score: {score.composite_deal_score}/100. "
                f"Eligibility: {'PASS' if score.is_eligible else 'FAIL (' + ', '.join(score.ineligibility_reasons) + ')'}."
            )
            self._log_trace(
                stage="ANALYZING",
                action=f"Audit Vendor: {v['name']}",
                tool_name="score_vendor_deal",
                input_data={"vendor_id": v["id"], "usage": self.mission.monthly_usage},
                output_summary=audit_msg,
                status=status_str,
                duration_ms=round((time.time() - v_start) * 1000, 2),
                evidence_verified=score.evidence_score >= 70.0
            )

        # Step 4: RANKING & DEAL REGRET CHECK
        # Separate eligible vs ineligible
        eligible_vendors = [s for s in scored_vendors if s.is_eligible]
        eligible_vendors.sort(key=lambda s: s.composite_deal_score, reverse=True)
        ineligible_vendors = [s for s in scored_vendors if not s.is_eligible]
        ineligible_vendors.sort(key=lambda s: s.composite_deal_score, reverse=True)

        baseline_winner_id = eligible_vendors[0].vendor_id if eligible_vendors else None

        # Deal Regret Check (Sensitivity Analysis)
        regret_start = time.time()
        regret_results = run_regret_sensitivity_check(
            self.mission, vendors, baseline_winner_id
        )
        regret_shifts = [r for r in regret_results if r.rank_changed]
        regret_summary = (
            f"Executed sensitivity stress-test across {len(regret_results)} usage scenarios. "
            f"Detected {len(regret_shifts)} regret inflection point(s) where rankings shift."
        )
        self._log_trace(
            stage="ANALYZING",
            action="Deal Regret Sensitivity Check",
            tool_name="run_regret_sensitivity_check",
            input_data={"scenarios": len(regret_results), "baseline_winner": baseline_winner_id},
            output_summary=regret_summary,
            status="SUCCESS",
            duration_ms=round((time.time() - regret_start) * 1000, 2)
        )

        # Step 5: VERIFYING & HUMAN REVIEW AUDIT
        self.status = AgentStatus.VERIFYING
        verify_start = time.time()
        is_human_review_required = False
        human_review_reasons = []

        if not eligible_vendors:
            is_human_review_required = True
            human_review_reasons.append(
                "CRITICAL: Zero vendors satisfied all mandatory requirements and budget constraints. "
                "Human procurement authorization required to revise budget or relax mandatory feature constraints."
            )
        else:
            # Check if recommended winner has questionable evidence
            winner = eligible_vendors[0]
            if winner.evidence_score < 70.0:
                is_human_review_required = True
                human_review_reasons.append(
                    f"Recommended vendor '{winner.vendor_name}' relies on unverified or stale evidence "
                    f"({winner.evidence_score}/100). Vendor contact required prior to binding contract."
                )

            # Check if regret risk exists at moderate growth
            moderate_shift = next((r for r in regret_results if r.usage_multiplier <= 1.5 and r.rank_changed), None)
            if moderate_shift:
                human_review_reasons.append(
                    f"High growth sensitivity: Winner changes at +25%-50% usage due to steep overage fees. "
                    "Recommend human review of 6-month projected volume."
                )

        # Independent mathematical audit verification
        # Recalculate TCO independently for all vendors to ensure deterministic truth
        audit_passed = True
        for s in scored_vendors:
            v_match = next((v for v in vendors if v["id"] == s.vendor_id), None)
            if v_match:
                independent_calc = calculate_cost_breakdown(v_match, self.mission.monthly_usage)
                if abs(independent_calc.total_annual_tco - s.cost_breakdown.total_annual_tco) > 0.01:
                    audit_passed = False
                    human_review_reasons.append(
                        f"Audit Discrepancy detected in TCO calculation for {s.vendor_name}!"
                    )

        self._log_trace(
            stage="VERIFYING",
            action="Independent Verification & Constraint Audit",
            tool_name=None,
            input_data={"audit_check": "TCO_and_Mandatory_Constraints"},
            output_summary=(
                f"Mathematical recalculation audit passed: {audit_passed}. "
                f"Human Review Required: {is_human_review_required}. "
                f"Audit flags: {len(human_review_reasons)}."
            ),
            status="SUCCESS" if audit_passed else "FAILED",
            duration_ms=round((time.time() - verify_start) * 1000, 2),
            evidence_verified=audit_passed
        )

        # Step 6: COMPLETED or NEEDS_REVIEW
        if is_human_review_required:
            self.status = AgentStatus.NEEDS_REVIEW
        else:
            self.status = AgentStatus.COMPLETED

        recommended_vendor = eligible_vendors[0] if eligible_vendors else None
        runner_up = eligible_vendors[1] if len(eligible_vendors) > 1 else None

        # Build full procurement report
        # All scored vendors combined in presentation order (eligible first, then ineligible)
        all_ordered_scores = eligible_vendors + ineligible_vendors

        assumptions = [
            f"Monthly usage baseline set at {self.mission.monthly_usage:,} operations/month.",
            f"Cost ceiling evaluated against user budget of ${self.mission.monthly_budget:.2f}/month.",
            "Annual cost reflects standard contractual commitment discounts where available.",
            "Evidence scoring penalizes unverified third-party sources and data retrieved before 2026.",
            "Deterministic arithmetic calculation applied for all financial totals; zero LLM arithmetic approximation."
        ]

        risks = []
        if recommended_vendor:
            risks.extend(recommended_vendor.hidden_risks_detected)
        for inel in ineligible_vendors:
            risks.append(f"Ineligible Vendor '{inel.vendor_name}': {'; '.join(inel.ineligibility_reasons)}")

        confidence_explanation = (
            f"Confidence score of {recommended_vendor.confidence_score if recommended_vendor else 0.0}% reflects "
            f"evidence source verification, pricing transparency, and mandatory feature coverage. "
            f"A score >= 80% denotes contractually verified pricing and SLA guarantees."
        )

        report = ProcurementReport(
            mission_id=self.run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            status=self.status,
            recommended_vendor_id=recommended_vendor.vendor_id if recommended_vendor else None,
            recommended_vendor_name=recommended_vendor.vendor_name if recommended_vendor else "No Eligible Vendor",
            runner_up_vendor_name=runner_up.vendor_name if runner_up else None,
            is_human_review_required=is_human_review_required,
            human_review_reasons=human_review_reasons,
            scored_vendors=all_ordered_scores,
            regret_sensitivity=regret_results,
            assumptions_stated=assumptions,
            risks_and_unresolved=risks,
            confidence_explanation=confidence_explanation,
            audit_verification_passed=audit_passed,
            trace_id=f"neatlogs_trace_{self.run_id}",
            total_execution_steps=len(self.trace_steps)
        )

        # Export trace to evidence folder for verification
        self._export_evidence_trace(report)

        # Flush SDK queue according to Neatlogs setup guide
        if getattr(self, "neatlogs_active", False) and HAS_NEATLOGS_SDK:
            try:
                neatlogs.flush()
            except Exception:
                pass

        return report

    def _export_evidence_trace(self, report: ProcurementReport):
        """Saves actual trace and run snapshot to evidence directory."""
        try:
            trace_payload = {
                "trace_metadata": {
                    "trace_id": report.trace_id,
                    "mission_id": report.mission_id,
                    "timestamp": report.timestamp,
                    "agent": "DealHunter AI",
                    "status": report.status.value,
                    "neatlogs_connected": HAS_NEATLOGS_SDK and bool(NEATLOGS_API_KEY)
                },
                "execution_timeline": [step.to_dict() for step in self.trace_steps],
                "report_summary": {
                    "recommended_vendor": report.recommended_vendor_name,
                    "is_human_review_required": report.is_human_review_required,
                    "reasons": report.human_review_reasons,
                    "total_steps": report.total_execution_steps
                }
            }
            output_file = EVIDENCE_DIR / "neatlogs-trace.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(trace_payload, f, indent=2)
        except Exception as e:
            print(f"[Evidence Export] Warning: {e}")
