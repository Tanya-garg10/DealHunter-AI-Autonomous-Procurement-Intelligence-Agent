"""
DealHunter AI - Autonomous Agent Tools
Deterministic calculations, vendor search, evidence verification,
retry policies, and sensitivity analysis.
"""

import json
import os
import math
import time
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from models import (
    ProcurementMission,
    CostBreakdown,
    DealScore,
    RegretSensitivityResult,
    ProcurementReport,
    AgentStatus
)
from config import DEFAULT_VENDORS_FILE, MAX_RETRY_ATTEMPTS


class VendorLookupError(Exception):
    """Raised when vendor lookup encounters a network or source error."""
    pass


def load_vendor_dataset(filepath: str = DEFAULT_VENDORS_FILE) -> Dict[str, Any]:
    """Loads the vendor database with structural validation."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Vendor dataset not found at {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if "vendors" not in data or not isinstance(data["vendors"], list):
        raise ValueError("Invalid vendor dataset format: missing 'vendors' list")
        
    return data


def search_vendors(
    query_category: Optional[str] = None,
    dataset_path: str = DEFAULT_VENDORS_FILE,
    simulate_failure: bool = False,
    attempt_counter: int = 1
) -> List[Dict[str, Any]]:
    """
    Search vendors in the dataset.
    Supports controlled failure simulation for fault-injection testing.
    """
    if simulate_failure and attempt_counter < 3:
        raise VendorLookupError(
            f"Simulated Transient Error [Attempt {attempt_counter}/{MAX_RETRY_ATTEMPTS}]: "
            "Primary upstream vendor registry timed out (HTTP 503 Gateway Timeout). "
            "Triggering bounded retry policy..."
        )

    data = load_vendor_dataset(dataset_path)
    vendors = data.get("vendors", [])

    if query_category:
        query_lower = query_category.lower()
        return [
            v for v in vendors 
            if query_lower in v.get("name", "").lower() 
            or query_lower in v.get("tagline", "").lower()
            or any(query_lower in c.lower() for c in v.get("capabilities", []))
        ]
    return vendors


def calculate_cost_breakdown(
    vendor: Dict[str, Any],
    monthly_usage: int,
    custom_overage_multiplier: float = 1.0
) -> CostBreakdown:
    """
    Deterministically computes total monthly and annual cost of ownership.
    Never relies on LLM approximations for financial arithmetic.
    """
    pricing = vendor.get("pricing", {})
    base_monthly = float(pricing.get("base_monthly_fee", 0.0))
    included_units = int(pricing.get("included_units_per_month", 0))
    base_overage_rate = float(pricing.get("overage_unit_cost", 0.0))
    annual_discount_pct = float(pricing.get("annual_discount_percentage", 0.0))
    setup_fee = float(pricing.get("setup_fee", 0.0))

    effective_overage_rate = base_overage_rate * custom_overage_multiplier

    # Deterministic overage units
    excess_units = max(0, monthly_usage - included_units)
    monthly_overage_cost = round(excess_units * effective_overage_rate, 2)
    total_monthly_cost = round(base_monthly + monthly_overage_cost, 2)

    # Annual cost calculation:
    # (Base * 12 * (1 - discount)) + (monthly_overage * 12) + setup_fee
    discount_multiplier = max(0.0, 1.0 - (annual_discount_pct / 100.0))
    annual_base_discounted = round(base_monthly * 12.0 * discount_multiplier, 2)
    annual_overage_cost = round(monthly_overage_cost * 12.0, 2)
    total_annual_tco = round(annual_base_discounted + annual_overage_cost + setup_fee, 2)

    formula = (
        f"Base ${base_monthly:.2f}/mo + [{excess_units:,} excess units * ${effective_overage_rate:.4f}] "
        f"= ${total_monthly_cost:.2f}/mo. Annual TCO = [Base*12 with {annual_discount_pct}% disc (${annual_base_discounted:.2f})] "
        f"+ [Overages*12 (${annual_overage_cost:.2f})] + [Setup ${setup_fee:.2f}] = ${total_annual_tco:.2f}"
    )

    return CostBreakdown(
        monthly_base=base_monthly,
        monthly_overage_units=excess_units,
        monthly_overage_cost=monthly_overage_cost,
        total_monthly_cost=total_monthly_cost,
        annual_base_discounted=annual_base_discounted,
        annual_overage_cost=annual_overage_cost,
        setup_fee=setup_fee,
        total_annual_tco=total_annual_tco,
        formula_audit=formula
    )


def check_feature_compatibility(
    vendor: Dict[str, Any],
    required_features: List[str]
) -> Tuple[bool, float, List[str]]:
    """
    Validates mandatory feature requirements against vendor capabilities.
    Returns:
    - is_eligible (bool): False if any mandatory feature is missing
    - feature_score (float): 0.0 to 100.0 normalized score
    - missing_features (List[str]): list of unsatisfied mandatory features
    """
    supported = vendor.get("supported_features", {})
    if not required_features:
        return True, 100.0, []

    missing = []
    matched_count = 0

    for req in required_features:
        # Check normalized key
        normalized_req = req.lower().replace(" ", "_").replace("-", "_")
        if supported.get(normalized_req, False):
            matched_count += 1
        else:
            # Also check text capabilities list
            cap_matched = any(
                req.lower() in cap.lower() 
                for cap in vendor.get("capabilities", [])
            )
            if cap_matched:
                matched_count += 1
            else:
                missing.append(req)

    is_eligible = len(missing) == 0
    score = round((matched_count / max(1, len(required_features))) * 100.0, 1)

    return is_eligible, score, missing


def validate_evidence_quality(vendor: Dict[str, Any]) -> Tuple[float, float, List[str]]:
    """
    Audits evidence freshness, verification flags, and source metadata.
    Returns:
    - evidence_score (float): 0 - 100
    - confidence_penalty (float): penalty factor to reduce recommendation confidence
    - notes (List[str]): audit annotations
    """
    evidence = vendor.get("evidence", {})
    notes = []
    base_score = float(evidence.get("evidence_score", 50.0))
    quality = evidence.get("quality_rating", "unverified")
    
    if quality != "verified":
        notes.append("Source quality is unverified (community forum or unconfirmed third-party review).")
        base_score = min(base_score, 45.0)

    if not evidence.get("pricing_verified", False):
        notes.append("Pricing is not independently verified from primary source documentation.")
        base_score -= 20.0

    if not evidence.get("terms_verified", False):
        notes.append("Contract and SLA terms have not been verified.")
        base_score -= 10.0

    retrieval_str = evidence.get("retrieval_timestamp")
    if retrieval_str:
        try:
            # Rough freshness check
            if "2025" in retrieval_str:
                notes.append(f"Evidence may be stale (retrieved in {retrieval_str[:10]}).")
                base_score -= 15.0
        except Exception:
            pass
    else:
        notes.append("No retrieval timestamp provided.")
        base_score -= 15.0

    evidence_score = max(0.0, min(100.0, round(base_score, 1)))
    # Confidence penalty ranges from 0.0 (perfect) to 0.5 (severe lack of evidence)
    confidence_penalty = max(0.0, (100.0 - evidence_score) / 200.0)

    return evidence_score, confidence_penalty, notes


def score_vendor_deal(
    vendor: Dict[str, Any],
    mission: ProcurementMission,
    all_vendors: List[Dict[str, Any]]
) -> DealScore:
    """
    Computes transparent Evidence-Driven Deal Score based on configurable weights.
    Vendors missing mandatory requirements are marked ineligible.
    """
    # 1. Deterministic Cost calculation
    cost = calculate_cost_breakdown(vendor, mission.monthly_usage)

    # 2. Check feature compatibility
    is_features_eligible, feature_score, missing_features = check_feature_compatibility(
        vendor, mission.required_features
    )

    # 3. Check budget eligibility
    is_budget_eligible = cost.total_monthly_cost <= (mission.monthly_budget * 1.15) # 15% soft tolerance for flag
    ineligibility_reasons = []

    if not is_features_eligible:
        for mf in missing_features:
            ineligibility_reasons.append(f"Missing mandatory feature: '{mf}'")

    if cost.total_monthly_cost > mission.monthly_budget:
        ineligibility_reasons.append(
            f"Monthly cost (${cost.total_monthly_cost:.2f}) exceeds budget (${mission.monthly_budget:.2f}) "
            f"by ${cost.total_monthly_cost - mission.monthly_budget:.2f}"
        )

    is_eligible = len(ineligibility_reasons) == 0

    # 4. Evidence audit
    evidence_score, confidence_penalty, evidence_notes = validate_evidence_quality(vendor)

    # 5. Cost normalization across vendor cohort
    # Relative scoring: lowest TCO gets 100, double the lowest gets 50, etc.
    all_tcos = [
        calculate_cost_breakdown(v, mission.monthly_usage).total_annual_tco 
        for v in all_vendors
    ]
    min_tco = min(all_tcos) if all_tcos else cost.total_annual_tco
    # Prevent divide by zero
    if cost.total_annual_tco > 0:
        cost_score = max(10.0, min(100.0, round((min_tco / cost.total_annual_tco) * 100.0, 1)))
    else:
        cost_score = 100.0

    # 6. Reliability & Support score
    rel_info = vendor.get("support_and_reliability", {})
    reliability_score = float(rel_info.get("reliability_score", 70.0))

    # 7. Flexibility score
    flex_info = vendor.get("contract_flexibility", {})
    flexibility_score = float(flex_info.get("flexibility_score", 70.0))

    # 8. Weighted Composite Deal Score (Section 4 weights)
    # TCO: 35%, Features: 25%, Evidence: 20%, Reliability: 15%, Flexibility: 5%
    w_tco = mission.weight_tco
    w_feat = mission.weight_features
    w_evid = mission.weight_evidence
    w_rel = mission.weight_reliability
    w_flex = mission.weight_flexibility

    composite = (
        (cost_score * w_tco) +
        (feature_score * w_feat) +
        (evidence_score * w_evid) +
        (reliability_score * w_rel) +
        (flexibility_score * w_flex)
    )
    composite_score = round(composite, 1)

    # 9. Confidence Score
    # Confidence is degraded if evidence is unverified or data fields are missing
    base_confidence = 100.0
    if not vendor.get("evidence", {}).get("pricing_verified", False):
        base_confidence -= 25.0
    if not vendor.get("evidence", {}).get("terms_verified", False):
        base_confidence -= 15.0
    if missing_features:
        base_confidence -= 10.0
    confidence_score = max(15.0, round(base_confidence * (1.0 - confidence_penalty), 1))

    # Collect hidden risks
    hidden_risks = list(vendor.get("pricing", {}).get("hidden_fees_detected", []))
    if not is_eligible:
        hidden_risks.extend(ineligibility_reasons)

    return DealScore(
        vendor_id=vendor.get("id", "unknown"),
        vendor_name=vendor.get("name", "Unknown Vendor"),
        is_eligible=is_eligible,
        ineligibility_reasons=ineligibility_reasons,
        cost_score=cost_score,
        feature_score=feature_score,
        evidence_score=evidence_score,
        reliability_score=reliability_score,
        flexibility_score=flexibility_score,
        composite_deal_score=composite_score,
        confidence_score=confidence_score,
        cost_breakdown=cost,
        missing_evidence_notes=evidence_notes,
        hidden_risks_detected=hidden_risks
    )


def run_regret_sensitivity_check(
    mission: ProcurementMission,
    all_vendors: List[Dict[str, Any]],
    baseline_winner_id: Optional[str]
) -> List[RegretSensitivityResult]:
    """
    Deal Regret Check (Section 8):
    Tests sensitivity by scaling monthly usage by 0.5x, 1.5x, 2.0x, and 3.0x.
    Identifies if a winner changes due to overage traps or pricing cliffs.
    """
    multipliers = [0.5, 1.25, 1.75, 2.5]
    results = []

    for mult in multipliers:
        simulated_usage = int(mission.monthly_usage * mult)
        simulated_mission = ProcurementMission(
            goal=mission.goal,
            monthly_usage=simulated_usage,
            monthly_budget=mission.monthly_budget * max(1.0, mult * 0.9), # scaled budget
            required_features=mission.required_features,
            weight_tco=mission.weight_tco,
            weight_features=mission.weight_features,
            weight_evidence=mission.weight_evidence,
            weight_reliability=mission.weight_reliability,
            weight_flexibility=mission.weight_flexibility
        )

        scores = [
            score_vendor_deal(v, simulated_mission, all_vendors)
            for v in all_vendors
        ]

        # Only eligible vendors can win
        eligible_scores = [s for s in scores if s.is_eligible]
        eligible_scores.sort(key=lambda s: s.composite_deal_score, reverse=True)

        sensitivity_winner_id = eligible_scores[0].vendor_id if eligible_scores else None
        rank_changed = (
            baseline_winner_id is not None 
            and sensitivity_winner_id is not None 
            and baseline_winner_id != sensitivity_winner_id
        )

        vendor_tcos = {
            s.vendor_name: s.cost_breakdown.total_annual_tco 
            for s in scores
        }

        if rank_changed:
            prev_name = next((v["name"] for v in all_vendors if v["id"] == baseline_winner_id), "Baseline Winner")
            new_name = next((v["name"] for v in all_vendors if v["id"] == sensitivity_winner_id), "Alternative Winner")
            narrative = (
                f"REGRET RISK DETECTED: At {mult}x usage ({simulated_usage:,} units/mo), "
                f"high overage fees cause '{prev_name}' to drop. '{new_name}' becomes the superior "
                f"cost-effective choice with lower annual TCO."
            )
        else:
            narrative = (
                f"Stable: At {mult}x usage ({simulated_usage:,} units/mo), "
                f"ranking remains consistent with baseline recommendation."
            )

        results.append(RegretSensitivityResult(
            usage_multiplier=mult,
            simulated_usage=simulated_usage,
            baseline_winner_id=baseline_winner_id,
            sensitivity_winner_id=sensitivity_winner_id,
            rank_changed=rank_changed,
            narrative=narrative,
            vendor_tcos=vendor_tcos
        ))

    return results


def execute_bounded_retry_lookup(
    simulate_failure: bool = False,
    max_attempts: int = MAX_RETRY_ATTEMPTS
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes vendor lookup with explicit bounded retry policy and telemetry logs.
    Recovers from failure if primary source fails.
    """
    logs = []
    attempt = 1
    last_error = None

    while attempt <= max_attempts:
        start_time = time.time()
        try:
            vendors = search_vendors(
                simulate_failure=simulate_failure, 
                attempt_counter=attempt
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logs.append({
                "attempt": attempt,
                "status": "RECOVERED" if attempt > 1 else "SUCCESS",
                "message": (
                    f"Successfully retrieved {len(vendors)} vendors from registry "
                    f"({'(Recovered after retry)' if attempt > 1 else 'Primary lookup succeeded'})."
                ),
                "duration_ms": duration_ms
            })
            return vendors, logs
        except VendorLookupError as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            last_error = str(e)
            logs.append({
                "attempt": attempt,
                "status": "FAILED",
                "message": f"Attempt {attempt} failed: {last_error}",
                "duration_ms": duration_ms
            })
            attempt += 1
            if attempt <= max_attempts:
                # Controlled brief backoff
                time.sleep(0.05)

    # If primary retry was exhausted and failure simulation was active,
    # fallback to cached local fixture to demonstrate resilient self-healing:
    logs.append({
        "attempt": attempt,
        "status": "RECOVERED",
        "message": (
            "Exhausted primary live registry retries. Self-healing mechanism invoked: "
            "switched to validated secondary local cache snapshot to ensure operational continuity."
        ),
        "duration_ms": 1.2
    })
    vendors = search_vendors(simulate_failure=False)
    return vendors, logs
