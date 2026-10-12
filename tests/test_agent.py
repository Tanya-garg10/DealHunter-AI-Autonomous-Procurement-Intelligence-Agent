"""
DealHunter AI - Comprehensive Test Suite
Validates all 11 critical requirements specified in Section 14:
1. Monthly and annual cost calculations
2. Overage calculations
3. Mandatory feature matching
4. Budget eligibility
5. Evidence-quality scoring
6. Missing vendor fields
7. Retry behavior
8. Recovery after a simulated failure
9. No eligible vendor scenario
10. Sensitivity analysis
11. Final report generation
"""

import unittest
import os
import json
from models import (
    ProcurementMission,
    AgentStatus,
    RiskTolerance,
    CostBreakdown
)
from tools import (
    load_vendor_dataset,
    calculate_cost_breakdown,
    check_feature_compatibility,
    validate_evidence_quality,
    score_vendor_deal,
    run_regret_sensitivity_check,
    execute_bounded_retry_lookup,
    search_vendors,
    VendorLookupError
)
from agent import DealHunterAgent


class TestDealHunterProcurement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_vendor_dataset("vendors.json")
        cls.vendors = cls.dataset["vendors"]
        cls.datasprout = next(v for v in cls.vendors if v["id"] == "vendor_datasprout")
        cls.apexcloud = next(v for v in cls.vendors if v["id"] == "vendor_apexcloud")
        cls.quickflux = next(v for v in cls.vendors if v["id"] == "vendor_quickflux")
        cls.omniscale = next(v for v in cls.vendors if v["id"] == "vendor_omniscale")

    # 1. Monthly and annual cost calculations
    def test_01_monthly_and_annual_cost_calculation(self):
        # DataSprout: Base $49/mo, 10,000 included, 10% annual discount
        # Usage: 10,000 (0 overage)
        cost = calculate_cost_breakdown(self.datasprout, 10000)
        self.assertEqual(cost.monthly_base, 49.0)
        self.assertEqual(cost.monthly_overage_units, 0)
        self.assertEqual(cost.monthly_overage_cost, 0.0)
        self.assertEqual(cost.total_monthly_cost, 49.0)
        
        # Annual: 49 * 12 * 0.90 = 529.20 + 0 overage + 0 setup = 529.20
        self.assertAlmostEqual(cost.annual_base_discounted, 529.20, places=2)
        self.assertAlmostEqual(cost.total_annual_tco, 529.20, places=2)

    # 2. Overage calculations
    def test_02_overage_calculations(self):
        # DataSprout: Base $49/mo, 10,000 included, overage $0.015/unit
        # Usage: 50,000 (40,000 overage)
        cost = calculate_cost_breakdown(self.datasprout, 50000)
        self.assertEqual(cost.monthly_overage_units, 40000)
        # 40,000 * 0.015 = 600.00
        self.assertAlmostEqual(cost.monthly_overage_cost, 600.0, places=2)
        self.assertAlmostEqual(cost.total_monthly_cost, 649.0, places=2)
        
        # Annual overage: 600 * 12 = 7200.00
        self.assertAlmostEqual(cost.annual_overage_cost, 7200.0, places=2)
        # Total annual: 529.20 + 7200.00 = 7729.20
        self.assertAlmostEqual(cost.total_annual_tco, 7729.20, places=2)

    # 3. Mandatory feature matching
    def test_03_mandatory_feature_matching(self):
        # Test SSO/SAML requirement: DataSprout doesn't have it, ApexCloud does
        eligible_apex, score_apex, missing_apex = check_feature_compatibility(
            self.apexcloud, ["sso_saml", "soc2"]
        )
        self.assertTrue(eligible_apex)
        self.assertEqual(score_apex, 100.0)
        self.assertEqual(len(missing_apex), 0)

        eligible_ds, score_ds, missing_ds = check_feature_compatibility(
            self.datasprout, ["sso_saml", "soc2"]
        )
        self.assertFalse(eligible_ds)
        self.assertEqual(score_ds, 50.0)
        self.assertIn("sso_saml", missing_ds)

    # 4. Budget eligibility
    def test_04_budget_eligibility(self):
        mission_tight = ProcurementMission(
            monthly_usage=10000,
            monthly_budget=100.0,
            required_features=["rest_api"]
        )
        # ApexCloud base is $299/mo, exceeding $100 budget
        score_apex = score_vendor_deal(self.apexcloud, mission_tight, self.vendors)
        self.assertFalse(score_apex.is_eligible)
        self.assertTrue(any("exceeds budget" in r for r in score_apex.ineligibility_reasons))

        # DataSprout is $49/mo, fits budget
        score_ds = score_vendor_deal(self.datasprout, mission_tight, self.vendors)
        self.assertTrue(score_ds.is_eligible)

    # 5. Evidence-quality scoring
    def test_05_evidence_quality_scoring(self):
        # QuickFlux has unverified community forum source
        evid_score_qf, pen_qf, notes_qf = validate_evidence_quality(self.quickflux)
        self.assertLess(evid_score_qf, 50.0)
        self.assertTrue(any("unverified" in n.lower() for n in notes_qf))
        self.assertGreater(pen_qf, 0.2)

        # ApexCloud has verified enterprise MSA
        evid_score_ac, pen_ac, notes_ac = validate_evidence_quality(self.apexcloud)
        self.assertGreaterEqual(evid_score_ac, 90.0)
        self.assertLess(pen_ac, 0.1)

    # 6. Missing vendor fields handling
    def test_06_missing_vendor_fields_handling(self):
        incomplete_vendor = {
            "id": "vendor_sparse",
            "name": "Sparse Labs",
            "capabilities": ["API"],
            "pricing": {
                "base_monthly_fee": 50.0,
                # missing included_units and overage_cost
            }
        }
        # Should not crash, defaults to 0
        cost = calculate_cost_breakdown(incomplete_vendor, 1000)
        self.assertEqual(cost.monthly_base, 50.0)
        self.assertEqual(cost.monthly_overage_cost, 0.0)

        evid_score, pen, notes = validate_evidence_quality(incomplete_vendor)
        self.assertTrue(any("retrieval timestamp" in n.lower() for n in notes))

    # 7. Retry behavior
    def test_07_retry_behavior(self):
        # Attempt 1 should fail when simulate_failure=True
        with self.assertRaises(VendorLookupError):
            search_vendors(simulate_failure=True, attempt_counter=1)

        with self.assertRaises(VendorLookupError):
            search_vendors(simulate_failure=True, attempt_counter=2)

        # Attempt 3 succeeds
        result = search_vendors(simulate_failure=True, attempt_counter=3)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    # 8. Recovery after simulated failure
    def test_08_recovery_after_simulated_failure(self):
        vendors, logs = execute_bounded_retry_lookup(simulate_failure=True)
        self.assertGreater(len(vendors), 0)
        # Should contain retry / recovered logs
        statuses = [l["status"] for l in logs]
        self.assertIn("FAILED", statuses)
        self.assertIn("RECOVERED", statuses)

    # 9. No eligible vendor scenario
    def test_09_no_eligible_vendor_scenario(self):
        # Impossible requirements: $10/mo budget AND multi_region AND sso_saml
        impossible_mission = ProcurementMission(
            goal="Impossible constraint test",
            monthly_usage=100000,
            monthly_budget=10.0,
            required_features=["multi_region", "sso_saml"],
            simulate_lookup_failure=False
        )
        agent = DealHunterAgent(impossible_mission)
        report = agent.run()

        self.assertEqual(report.status, AgentStatus.NEEDS_REVIEW)
        self.assertTrue(report.is_human_review_required)
        self.assertIsNone(report.recommended_vendor_id)
        self.assertTrue(any("Zero vendors satisfied" in r for r in report.human_review_reasons))

    # 10. Sensitivity analysis (Deal Regret Check)
    def test_10_sensitivity_analysis_regret_check(self):
        # Mission where DataSprout is cheapest at 10,000 units, but becomes
        # a massive regret at 100,000 units due to overage fees
        mission = ProcurementMission(
            monthly_usage=10000,
            monthly_budget=500.0,
            required_features=["rest_api", "soc2"]
        )
        results = run_regret_sensitivity_check(mission, self.vendors, "vendor_datasprout")
        self.assertEqual(len(results), 4)
        
        # Check high usage multiplier (2.5x = 25,000 units)
        high_usage = next(r for r in results if r.usage_multiplier == 2.5)
        # DataSprout overage costs should escalate
        ds_tco = high_usage.vendor_tcos["DataSprout Pro"]
        self.assertGreater(ds_tco, 2000.0)

    # 11. Final report generation
    def test_11_final_report_generation(self):
        mission = ProcurementMission(
            goal="Standard Team API Platform",
            monthly_usage=30000,
            monthly_budget=250.0,
            required_features=["rest_api", "soc2"],
            simulate_lookup_failure=False
        )
        agent = DealHunterAgent(mission)
        report = agent.run()

        self.assertIsNotNone(report.mission_id)
        self.assertTrue(report.audit_verification_passed)
        self.assertGreater(report.total_execution_steps, 3)
        self.assertGreater(len(report.scored_vendors), 0)
        self.assertTrue(os.path.exists("evidence/neatlogs-trace.json"))


if __name__ == "__main__":
    unittest.main()
