"""
DealHunter AI - Autonomous Procurement Intelligence Agent
Streamlit Web Frontend for neatHack 2026.
Tagline: Don't just find a deal. Prove it's the right deal.
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from models import ProcurementMission, RiskTolerance, AgentStatus
from agent import DealHunterAgent
from tools import load_vendor_dataset
from config import NEATLOGS_API_KEY, NEATLOGS_PROJECT_ID

# Page Configuration
st.set_page_config(
    page_title="DealHunter AI | Procurement Intelligence Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling: Dark Navy (#0A0D14, #0F172A), Violet accents (#8B5CF6), crisp typography
st.markdown("""
<style>
    .stApp {
        background-color: #0A0D14;
        color: #E2E8F0;
    }
    .metric-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .winner-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(16, 185, 129, 0.08) 100%);
        border: 1px solid #8B5CF6;
        border-radius: 8px;
        padding: 20px;
    }
    .step-badge {
        font-family: monospace;
        font-size: 0.8rem;
        padding: 2px 8px;
        border-radius: 4px;
        background-color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎯 DealHunter AI")
st.caption("Don't just find a deal. Prove it's the right deal. · neatHack 2026")

# Sidebar: Mission Builder
with st.sidebar:
    st.header("📋 Mission Builder")
    goal = st.text_input(
        "Purchasing Goal",
        value="Enterprise Event Processing & Data Pipeline",
        help="Describe what system or service you need to procure."
    )
    
    col_u, col_b = st.columns(2)
    with col_u:
        monthly_usage = st.number_input(
            "Monthly Usage (Units)",
            min_value=1000,
            max_value=1000000,
            value=50000,
            step=5000,
            help="Expected monthly event volume or API calls"
        )
    with col_b:
        monthly_budget = st.number_input(
            "Monthly Budget ($)",
            min_value=10.0,
            max_value=10000.0,
            value=350.0,
            step=25.0,
            help="Hard budget ceiling per month"
        )

    required_features_options = [
        "rest_api", "soc2", "sso_saml", "multi_region",
        "dedicated_support", "custom_rbac", "audit_logs", "automated_backups"
    ]
    required_features = st.multiselect(
        "Mandatory Required Features",
        options=required_features_options,
        default=["rest_api", "soc2"],
        help="Vendors missing ANY mandatory feature will be flagged ineligible."
    )

    risk_tolerance_str = st.selectbox(
        "Risk Tolerance",
        options=["low", "balanced", "high"],
        index=1,
        help="Low requires verified compliance. High tolerates newer pricing structures."
    )

    st.markdown("---")
    st.subheader("🛠️ Autonomous Agent Controls")
    simulate_failure = st.checkbox(
        "Simulate Lookup Failure (Fault-Injection)",
        value=False,
        help="Demonstrates bounded retry policy, error logging, and self-healing fallback."
    )

    with st.expander("Scoring Weights (Evidence-Driven)", expanded=False):
        w_tco = st.slider("TCO Weight", 0.0, 1.0, 0.35, 0.05)
        w_feat = st.slider("Features Weight", 0.0, 1.0, 0.25, 0.05)
        w_evid = st.slider("Evidence Weight", 0.0, 1.0, 0.20, 0.05)
        w_rel = st.slider("Reliability Weight", 0.0, 1.0, 0.15, 0.05)
        w_flex = st.slider("Flexibility Weight", 0.0, 1.0, 0.05, 0.05)

    start_button = st.button("🚀 Start Investigation", type="primary", use_container_width=True)

# Main Session State
if "report" not in st.session_state or start_button:
    mission = ProcurementMission(
        goal=goal,
        monthly_usage=int(monthly_usage),
        monthly_budget=float(monthly_budget),
        required_features=required_features,
        risk_tolerance=RiskTolerance(risk_tolerance_str),
        weight_tco=w_tco,
        weight_features=w_feat,
        weight_evidence=w_evid,
        weight_reliability=w_rel,
        weight_flexibility=w_flex,
        simulate_lookup_failure=simulate_failure
    )
    with st.spinner("DealHunter Agent is executing autonomous procurement plan..."):
        agent = DealHunterAgent(mission)
        report = agent.run()
        st.session_state.report = report
        st.session_state.trace_steps = agent.trace_steps
        st.session_state.mission = mission

report = st.session_state.report
trace_steps = st.session_state.trace_steps

# Top Alert / Human Review Banner
if report.is_human_review_required:
    st.warning("⚠️ **Human Review Required Prior to Contract Execution**")
    for reason in report.human_review_reasons:
        st.markdown(f"- {reason}")
else:
    st.success(f"✅ **Investigation Complete** — Verified Recommendation: **{report.recommended_vendor_name}**")

# Tabs for Section Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Deal Comparison",
    "⚡ Live Agent Activity",
    "🔄 Deal Regret Check",
    "📄 Procurement Report",
    "🛰️ Audit & Observability"
])

# TAB 1: DEAL COMPARISON
with tab1:
    st.subheader("Vendor Comparison Matrix")
    comparison_data = []
    for s in report.scored_vendors:
        comparison_data.append({
            "Vendor": s.vendor_name,
            "Eligibility": "✅ Eligible" if s.is_eligible else "❌ Ineligible",
            "Monthly Cost": f"${s.cost_breakdown.total_monthly_cost:,.2f}",
            "Annual TCO": f"${s.cost_breakdown.total_annual_tco:,.2f}",
            "Base Fee": f"${s.cost_breakdown.monthly_base:,.2f}",
            "Overage Fee": f"${s.cost_breakdown.monthly_overage_cost:,.2f}",
            "Feature Match": f"{s.feature_score}%",
            "Evidence Quality": f"{s.evidence_score}%",
            "Deal Score": f"{s.composite_deal_score} / 100",
            "Confidence": f"{s.confidence_score}%"
        })
    df_compare = pd.DataFrame(comparison_data)
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

    st.markdown("#### Vendor Cards & Forensic Deep Dive")
    cols = st.columns(len(report.scored_vendors))
    for idx, s in enumerate(report.scored_vendors):
        with cols[idx]:
            is_winner = s.vendor_id == report.recommended_vendor_id
            card_class = "winner-card" if is_winner else "metric-card"
            st.markdown(f"""
            <div class="{card_class}">
                <div style="font-weight: 700; font-size: 1.1rem;">
                    {'🏆 ' if is_winner else ''}{s.vendor_name}
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 8px;">
                    Deal Score: <strong style="color: #8B5CF6;">{s.composite_deal_score}</strong> | Confidence: {s.confidence_score}%
                </div>
                <div style="font-size: 0.9rem;">
                    <strong>Monthly:</strong> ${s.cost_breakdown.total_monthly_cost:,.2f}<br/>
                    <strong>Annual TCO:</strong> ${s.cost_breakdown.total_annual_tco:,.2f}<br/>
                    <strong>Overage:</strong> {s.cost_breakdown.monthly_overage_units:,} units (${s.cost_breakdown.monthly_overage_cost:,.2f})
                </div>
            </div>
            """, unsafe_allow_html=True)

            if not s.is_eligible:
                st.error("Ineligible Reasons:")
                for r in s.ineligibility_reasons:
                    st.caption(f"• {r}")
            
            if s.hidden_risks_detected:
                with st.expander("Detected Risks", expanded=False):
                    for risk in s.hidden_risks_detected:
                        st.caption(f"⚠️ {risk}")

# TAB 2: LIVE AGENT ACTIVITY
with tab2:
    st.subheader("Autonomous State Machine Execution")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Current State", report.status)
    col_stat2.metric("Total Execution Steps", len(trace_steps))
    col_stat3.metric("Verification Audit", "Passed" if report.audit_verification_passed else "Flagged")

    st.markdown("#### Step-by-Step Execution Timeline")
    for step in trace_steps:
        status_color = "#10B981" if step.status == "SUCCESS" else "#EF4444" if step.status == "FAILED" else "#F59E0B"
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="step-badge">{step.step_id} · {step.stage}</span>
                <span style="color: {status_color}; font-weight: 600; font-size: 0.85rem;">{step.status} ({step.duration_ms}ms)</span>
            </div>
            <div style="font-weight: 600; margin-top: 6px;">{step.action}</div>
            <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">{step.output_summary}</div>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: DEAL REGRET CHECK
with tab3:
    st.subheader("🔄 Deal Regret Stress-Test (Sensitivity Analysis)")
    st.caption("Validates how vendor rankings shift when usage spikes or contracts flex.")

    regret_data = []
    for r in report.regret_sensitivity:
        regret_data.append({
            "Scenario": f"{r.usage_multiplier}x Usage ({r.simulated_usage:,} ops)",
            "Baseline Winner": r.baseline_winner_id,
            "Winner Under Scenario": r.sensitivity_winner_id,
            "Regret Triggered?": "⚠️ YES - Rank Inversion" if r.rank_changed else "✅ No (Stable)",
            "Audited Narrative": r.narrative
        })
    st.dataframe(pd.DataFrame(regret_data), use_container_width=True, hide_index=True)

# TAB 4: PROCUREMENT REPORT
with tab4:
    st.subheader("📄 Final Procurement Intelligence Report")
    st.markdown(f"**Mission ID:** `{report.mission_id}` | **Generated:** `{report.timestamp}`")

    st.markdown("### Executive Recommendation")
    if report.recommended_vendor_name and report.recommended_vendor_name != "No Eligible Vendor":
        st.success(f"**Recommended Winner:** {report.recommended_vendor_name}")
        if report.runner_up_vendor_name:
            st.info(f"**Runner-Up Alternative:** {report.runner_up_vendor_name}")
    else:
        st.error("No eligible vendor meets both your mandatory feature checklist and budget envelope.")

    st.markdown("### Confidence Explanation")
    st.write(report.confidence_explanation)

    st.markdown("### Stated Assumptions")
    for a in report.assumptions_stated:
        st.markdown(f"- {a}")

    st.markdown("### Export Procurement Artifacts")
    report_json = json.dumps(report.to_dict(), indent=2)
    st.download_button(
        "📥 Download Report (JSON)",
        data=report_json,
        file_name=f"dealhunter_procurement_{report.mission_id}.json",
        mime="application/json"
    )

# TAB 5: AUDIT & OBSERVABILITY
with tab5:
    st.subheader("🛰️ neatlogs Observability & Audit Trail")
    st.caption("Live streaming traces to neatlogs session recorder")

    st.json({
        "neatlogs_project_id": NEATLOGS_PROJECT_ID,
        "neatlogs_connected": bool(NEATLOGS_API_KEY),
        "trace_id": report.trace_id,
        "total_steps": len(trace_steps),
        "audit_verification_passed": report.audit_verification_passed
    })

    st.info("💡 To connect live remote streaming to the neatlogs dashboard, set `NEATLOGS_API_KEY` in `.env`.")
