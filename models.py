"""
DealHunter AI - Core Typed Data Models
Pydantic / Dataclasses architecture for procurement intelligence agent.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Any
import datetime


class AgentStatus(str, Enum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    RESEARCHING = "RESEARCHING"
    ANALYZING = "ANALYZING"
    RECOVERING = "RECOVERING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class RiskTolerance(str, Enum):
    LOW = "low"          # Strictly verified evidence, high SLA, strict budgets
    BALANCED = "balanced" # Moderate overage tolerance, balanced trade-offs
    HIGH = "high"        # Aggressive cost reduction, tolerant of newer vendors


@dataclass
class ProcurementMission:
    goal: str = "Enterprise API event pipeline & webhook processing"
    monthly_usage: int = 50000
    monthly_budget: float = 350.0
    required_features: List[str] = field(default_factory=lambda: ["rest_api", "soc2"])
    preferred_characteristics: List[str] = field(default_factory=lambda: ["transparent_pricing", "sla_guarantee"])
    risk_tolerance: RiskTolerance = RiskTolerance.BALANCED
    
    # Configurable Scoring Model Weights (defaults to section 4 specifications)
    weight_tco: float = 0.35
    weight_features: float = 0.25
    weight_evidence: float = 0.20
    weight_reliability: float = 0.15
    weight_flexibility: float = 0.05
    
    # Controlled demonstration toggle for fault-injection & recovery testing
    simulate_lookup_failure: bool = False


@dataclass
class CostBreakdown:
    monthly_base: float
    monthly_overage_units: int
    monthly_overage_cost: float
    total_monthly_cost: float
    annual_base_discounted: float
    annual_overage_cost: float
    setup_fee: float
    total_annual_tco: float
    formula_audit: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DealScore:
    vendor_id: str
    vendor_name: str
    is_eligible: bool
    ineligibility_reasons: List[str]
    cost_score: float         # 0 - 100
    feature_score: float      # 0 - 100
    evidence_score: float     # 0 - 100
    reliability_score: float  # 0 - 100
    flexibility_score: float  # 0 - 100
    composite_deal_score: float # 0 - 100
    confidence_score: float   # 0 - 100
    cost_breakdown: CostBreakdown
    missing_evidence_notes: List[str] = field(default_factory=list)
    hidden_risks_detected: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegretSensitivityResult:
    usage_multiplier: float
    simulated_usage: int
    baseline_winner_id: Optional[str]
    sensitivity_winner_id: Optional[str]
    rank_changed: bool
    narrative: str
    vendor_tcos: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceStep:
    step_id: str
    timestamp: str
    stage: str
    action: str
    tool_name: Optional[str]
    input_data: Dict[str, Any]
    output_summary: str
    status: str  # "SUCCESS", "RETRY", "FAILED", "RECOVERED"
    duration_ms: float
    evidence_verified: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProcurementReport:
    mission_id: str
    timestamp: str
    status: AgentStatus
    recommended_vendor_id: Optional[str]
    recommended_vendor_name: Optional[str]
    runner_up_vendor_name: Optional[str]
    is_human_review_required: bool
    human_review_reasons: List[str]
    scored_vendors: List[DealScore]
    regret_sensitivity: List[RegretSensitivityResult]
    assumptions_stated: List[str]
    risks_and_unresolved: List[str]
    confidence_explanation: str
    audit_verification_passed: bool
    trace_id: str
    total_execution_steps: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "timestamp": self.timestamp,
            "status": self.status.value if isinstance(self.status, AgentStatus) else str(self.status),
            "recommended_vendor_id": self.recommended_vendor_id,
            "recommended_vendor_name": self.recommended_vendor_name,
            "runner_up_vendor_name": self.runner_up_vendor_name,
            "is_human_review_required": self.is_human_review_required,
            "human_review_reasons": self.human_review_reasons,
            "scored_vendors": [s.to_dict() for s in self.scored_vendors],
            "regret_sensitivity": [r.to_dict() for r in self.regret_sensitivity],
            "assumptions_stated": self.assumptions_stated,
            "risks_and_unresolved": self.risks_and_unresolved,
            "confidence_explanation": self.confidence_explanation,
            "audit_verification_passed": self.audit_verification_passed,
            "trace_id": self.trace_id,
            "total_execution_steps": self.total_execution_steps,
        }
