#!/usr/bin/env python3
"""
Unit Tests for LAI-PrEP Bridge Decision Support Tool
Tests edge cases, boundary conditions, and error handling
"""

import json
import sys

import pytest

# Import tool components
try:
    from lai_prep_decision_tool_v2_1 import (
        LAIPrEPDecisionTool,
        PatientProfile,
        Configuration,
        ConfigurationError
    )
except ImportError:
    print("Error: Could not import lai_prep_decision_tool_v2_1.py")
    sys.exit(1)


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""
    
    def setup_method(self):
        """Initialize tool before each test"""
        self.tool = LAIPrEPDecisionTool()
    
    def test_maximum_barriers(self):
        """Test profile with >4 barriers (extreme case)"""
        profile = PatientProfile(
            population="PWID",
            age=22,
            current_prep_status="naive",
            barriers=[
                "HOUSING_INSTABILITY",
                "TRANSPORTATION",
                "SUBSTANCE_USE",
                "LEGAL_CONCERNS",
                "MEDICAL_MISTRUST",
                "LACK_IDENTIFICATION",
                "HEALTHCARE_DISCRIMINATION"
            ],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="uninsured",
            transportation_access=False
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should still produce valid assessment
        assert 0 <= assessment.adjusted_success_rate <= 1, \
            "Success rate must be between 0 and 1"
        assert len(assessment.recommended_interventions) > 0, \
            "Should recommend at least one intervention"
        assert assessment.attrition_risk == "Very high attrition risk", \
            "Should categorize as very high risk"
        
        # Check that harm reduction integration is recommended for PWID
        intervention_names = [r.intervention for r in assessment.recommended_interventions]
        assert 'HARM_REDUCTION_INTEGRATION' in intervention_names or \
               'PEER_NAVIGATION' in intervention_names, \
            "Should recommend PWID-specific interventions"
    
    def test_conflicting_signals_oral_prep_no_test(self):
        """Test oral-to-injectable but no recent test"""
        profile = PatientProfile(
            population="MSM",
            age=30,
            current_prep_status="oral_prep",
            barriers=[],
            recent_hiv_test=False,  # Conflicting: on oral PrEP but no recent test
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="insured"
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should still recommend oral-to-injectable transition
        top_rec = assessment.recommended_interventions[0]
        assert 'ORAL' in top_rec.intervention, \
            "Should prioritize oral-to-injectable transition"
        
        # Should also recommend accelerated testing
        intervention_names = [r.intervention for r in assessment.recommended_interventions]
        assert 'ACCELERATED_TESTING' in intervention_names, \
            "Should recommend testing as high priority"
        
        # Success rate should still be high (oral PrEP advantage)
        assert assessment.adjusted_success_rate > 0.50, \
            "Oral PrEP patients should have >50% success even without recent test"
    
    def test_adolescent_privacy_concerns(self):
        """Test adolescent with parental insurance and privacy concerns"""
        profile = PatientProfile(
            population="ADOLESCENT",
            age=17,
            current_prep_status="naive",
            barriers=["PRIVACY_CONCERNS", "TRANSPORTATION", "LIMITED_NAVIGATION_EXPERIENCE"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="parental",  # Parental insurance raises privacy issues
            transportation_access=False
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should have high attrition risk
        assert assessment.attrition_risk in ["High attrition risk", "Very high attrition risk"], \
            "Adolescent with multiple barriers should be high/very high risk"
        
        # Should recommend patient navigation
        intervention_names = [r.intervention for r in assessment.recommended_interventions]
        assert 'PATIENT_NAVIGATION' in intervention_names, \
            "Should recommend navigation for adolescents"
        
        # Should recommend transportation support
        assert 'TRANSPORTATION_SUPPORT' in intervention_names, \
            "Should address transportation barrier"
        
        # Check for privacy-related clinical notes
        notes_text = ' '.join(assessment.clinical_notes).lower()
        assert 'adolescent' in notes_text, \
            "Should include adolescent-specific guidance"
    
    def test_zero_barriers_best_case(self):
        """Test best-case scenario: MSM on oral PrEP with recent test, no barriers"""
        profile = PatientProfile(
            population="MSM",
            age=28,
            current_prep_status="oral_prep",
            barriers=[],
            recent_hiv_test=True,
            healthcare_setting="LGBTQ_CENTER",
            insurance_status="insured",
            transportation_access=True
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should have very high success rate
        assert assessment.adjusted_success_rate >= 0.85, \
            "Best-case scenario should have ≥85% success rate"
        
        # Should categorize as low risk
        assert assessment.attrition_risk == "Low attrition risk", \
            "Should be low risk"
        
        # Should recommend same-day switching
        top_rec = assessment.recommended_interventions[0]
        assert top_rec.intervention == 'SAME_DAY_SWITCHING', \
            "Should recommend same-day switching as top priority"
        assert top_rec.priority == "Critical", \
            "Should be critical priority"
        
        # Bridge duration should be minimal
        assert assessment.estimated_bridge_duration_days[0] <= 3, \
            "Minimum bridge duration should be ≤3 days"
    
    def test_discontinued_oral_prep_re_engagement(self):
        """Test patient re-engaging after discontinuing oral PrEP"""
        profile = PatientProfile(
            population="CISGENDER_WOMEN",
            age=32,
            current_prep_status="discontinued_oral",
            barriers=["CHILDCARE", "MEDICAL_MISTRUST"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="insured",
            childcare_needs=True
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should recognize LAI-PrEP as solution to adherence challenges
        notes_text = ' '.join(assessment.clinical_notes)
        assert 'discontinued' in notes_text.lower() or 'adherence' in notes_text.lower(), \
            "Should reference discontinued oral PrEP status"
        
        # Should recommend interventions addressing barriers
        intervention_names = [r.intervention for r in assessment.recommended_interventions]
        assert 'CHILDCARE_SUPPORT' in intervention_names, \
            "Should address childcare barrier"
        assert 'PATIENT_NAVIGATION' in intervention_names, \
            "Should recommend navigation"
    
    def test_pregnant_individual(self):
        """Test pregnant individual with specific considerations"""
        profile = PatientProfile(
            population="PREGNANT_LACTATING",
            age=26,
            current_prep_status="naive",
            barriers=["CHILDCARE", "TRANSPORTATION", "COMPETING_PRIORITIES"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="insured",
            childcare_needs=True,
            transportation_access=False
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should have moderate-high risk
        assert assessment.adjusted_success_rate < 0.60, \
            "Multiple barriers should result in <60% success"
        
        # Should recommend barrier-specific interventions
        intervention_names = [r.intervention for r in assessment.recommended_interventions]
        assert 'CHILDCARE_SUPPORT' in intervention_names, \
            "Should address childcare"
        assert 'TRANSPORTATION_SUPPORT' in intervention_names or \
               'MOBILE_DELIVERY' in intervention_names, \
            "Should address transportation"
    
    def test_uninsured_patient(self):
        """Test uninsured patient with insurance barrier"""
        profile = PatientProfile(
            population="MSM",
            age=25,
            current_prep_status="naive",
            barriers=["INSURANCE_DELAYS"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="uninsured",
            transportation_access=True
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should identify insurance as delay factor
        assert len(assessment.delay_factors) > 0, \
            "Should identify delay factors"
        
        delay_text = ' '.join(assessment.delay_factors).lower()
        assert 'insurance' in delay_text or 'authorization' in delay_text, \
            "Should mention insurance in delay factors"
    
    def test_extreme_age_adolescent(self):
        """Test youngest eligible age (16 years based on PURPOSE-1)"""
        profile = PatientProfile(
            population="ADOLESCENT",
            age=16,
            current_prep_status="naive",
            barriers=["PRIVACY_CONCERNS", "LIMITED_NAVIGATION_EXPERIENCE"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="parental"
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should produce valid assessment
        assert 0 <= assessment.adjusted_success_rate <= 1
        assert assessment.attrition_risk in [
            "Low attrition risk", "Moderate attrition risk", 
            "High attrition risk", "Very high attrition risk"
        ]
    
    def test_extreme_age_older_adult(self):
        """Test older adult (edge case for typical PrEP population)"""
        profile = PatientProfile(
            population="MSM",
            age=65,
            current_prep_status="oral_prep",
            barriers=[],
            recent_hiv_test=True,
            healthcare_setting="PRIVATE_PRACTICE",
            insurance_status="insured"
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Should produce valid assessment (age doesn't directly affect algorithm)
        assert 0 <= assessment.adjusted_success_rate <= 1
        assert len(assessment.recommended_interventions) > 0


class TestLogitVsLinear:
    """Test logit-space vs linear calculations"""
    
    def test_logit_produces_valid_probabilities(self):
        """Test that logit method produces valid probabilities"""
        tool_logit = LAIPrEPDecisionTool(use_logit=True)
        
        profile = PatientProfile(
            population="PWID",
            age=35,
            current_prep_status="naive",
            barriers=["HOUSING_INSTABILITY", "TRANSPORTATION", "SUBSTANCE_USE"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER"
        )
        
        assessment = tool_logit.assess_patient(profile)
        
        # Should produce valid probability
        assert 0 < assessment.adjusted_success_rate < 1, \
            "Logit method should produce probability in (0, 1)"
        
        # Should not hit ceiling or floor
        assert assessment.adjusted_success_rate > 0.05, \
            "Should be above floor"
        assert assessment.adjusted_success_rate < 0.95, \
            "Should be below ceiling"
    
    def test_logit_vs_linear_consistency(self):
        """Test that logit and linear methods produce similar rankings"""
        profiles = [
            # Best case
            PatientProfile(
                population="MSM",
                age=30,
                current_prep_status="oral_prep",
                barriers=[],
                recent_hiv_test=True,
                healthcare_setting="LGBTQ_CENTER"
            ),
            # Moderate case
            PatientProfile(
                population="CISGENDER_WOMEN",
                age=28,
                current_prep_status="naive",
                barriers=["TRANSPORTATION", "CHILDCARE"],
                healthcare_setting="COMMUNITY_HEALTH_CENTER"
            ),
            # Worst case
            PatientProfile(
                population="PWID",
                age=35,
                current_prep_status="naive",
                barriers=[
                    "HOUSING_INSTABILITY", "TRANSPORTATION", 
                    "LEGAL_CONCERNS", "SUBSTANCE_USE"
                ],
                healthcare_setting="COMMUNITY_HEALTH_CENTER",
                insurance_status="uninsured"
            )
        ]
        
        tool_linear = LAIPrEPDecisionTool(use_logit=False)
        tool_logit = LAIPrEPDecisionTool(use_logit=True)
        
        linear_rates = []
        logit_rates = []
        
        for profile in profiles:
            linear_assessment = tool_linear.assess_patient(profile)
            logit_assessment = tool_logit.assess_patient(profile)
            
            linear_rates.append(linear_assessment.adjusted_success_rate)
            logit_rates.append(logit_assessment.adjusted_success_rate)
        
        # Check that both methods agree on relative ordering
        linear_rank = sorted(range(len(linear_rates)), key=lambda i: linear_rates[i])
        logit_rank = sorted(range(len(logit_rates)), key=lambda i: logit_rates[i])
        
        assert linear_rank == logit_rank, \
            "Logit and linear methods should produce same relative rankings"


class TestMechanismDiversity:
    """Test mechanism diversity in recommendations"""
    
    def setup_method(self):
        """Initialize tool before each test"""
        self.tool = LAIPrEPDecisionTool()
    
    def test_mechanism_diversity_prevents_redundancy(self):
        """Test that recommendations avoid mechanism overlap"""
        profile = PatientProfile(
            population="CISGENDER_WOMEN",
            age=30,
            current_prep_status="naive",
            barriers=["TRANSPORTATION", "CHILDCARE", "MEDICAL_MISTRUST"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="insured",
            transportation_access=False,
            childcare_needs=True
        )
        
        assessment = self.tool.assess_patient(profile)
        
        # Collect all mechanisms from top 3 recommendations
        all_mechanisms = []
        for rec in assessment.recommended_interventions[:3]:
            all_mechanisms.extend(rec.mechanisms)
        
        # Should have some diversity (not all same mechanism)
        unique_mechanisms = set(all_mechanisms)
        assert len(unique_mechanisms) >= 2, \
            "Top recommendations should use diverse mechanisms"
    
    def test_mechanism_tags_present(self):
        """Test that all recommendations have mechanism tags"""
        profile = PatientProfile(
            population="MSM",
            age=28,
            current_prep_status="oral_prep",
            barriers=[],
            recent_hiv_test=True,
            healthcare_setting="LGBTQ_CENTER"
        )
        
        assessment = self.tool.assess_patient(profile)
        
        for rec in assessment.recommended_interventions:
            assert len(rec.mechanisms) > 0, \
                f"Recommendation {rec.intervention_name} should have mechanism tags"


class TestJSONExport:
    """Test JSON export functionality"""
    
    def setup_method(self):
        """Initialize tool before each test"""
        self.tool = LAIPrEPDecisionTool()
    
    def test_json_export_valid_structure(self):
        """Test that JSON export produces valid structure"""
        profile = PatientProfile(
            population="MSM",
            age=30,
            current_prep_status="naive",
            barriers=["SCHEDULING_CONFLICTS"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="insured"
        )
        
        assessment = self.tool.assess_patient(profile)
        json_output = assessment.to_json(profile)
        
        # Check required top-level keys
        required_keys = [
            'patient_profile', 'risk_assessment', 'recommendations',
            'predictions', 'bridge_period_estimate', 'metadata'
        ]
        
        for key in required_keys:
            assert key in json_output, f"JSON output should have '{key}' key"
        
        # Check that values are JSON-serializable
        try:
            json_str = json.dumps(json_output)
            assert len(json_str) > 0
        except Exception as e:
            pytest.fail(f"JSON output should be serializable: {e}")
    
    def test_json_export_contains_explanations(self):
        """Test that JSON export includes explanatory fields"""
        profile = PatientProfile(
            population="PWID",
            age=35,
            current_prep_status="naive",
            barriers=["HOUSING_INSTABILITY", "TRANSPORTATION"],
            healthcare_setting="COMMUNITY_HEALTH_CENTER",
            insurance_status="uninsured"
        )
        
        assessment = self.tool.assess_patient(profile)
        json_output = assessment.to_json(profile)
        
        # Should include attrition factors
        assert 'attrition_factors' in json_output['risk_assessment'], \
            "Should include attrition factor explanations"
        
        # Should include delay factors
        assert 'delay_factors' in json_output['bridge_period_estimate'], \
            "Should include delay factor explanations"
        
        # Recommendations should have rationale
        for rec in json_output['recommendations']:
            assert 'rationale' in rec, \
                "Each recommendation should have rationale"
            assert len(rec['rationale']) > 0, \
                "Rationale should not be empty"


class TestErrorHandling:
    """Test error handling and validation"""
    
    def test_invalid_population(self):
        """Test that invalid population raises error"""
        with pytest.raises(ConfigurationError):
            profile = PatientProfile(
                population="INVALID_POP",
                age=30,
                current_prep_status="naive",
                barriers=[],
                healthcare_setting="COMMUNITY_HEALTH_CENTER"
            )
            tool = LAIPrEPDecisionTool()
            tool.assess_patient(profile)
    
    def test_invalid_barrier(self):
        """Test that invalid barrier raises error"""
        with pytest.raises(ConfigurationError):
            profile = PatientProfile(
                population="MSM",
                age=30,
                current_prep_status="naive",
                barriers=["INVALID_BARRIER"],
                healthcare_setting="COMMUNITY_HEALTH_CENTER"
            )
            tool = LAIPrEPDecisionTool()
            tool.assess_patient(profile)
    
    def test_invalid_healthcare_setting(self):
        """Test that invalid setting raises error"""
        with pytest.raises(ConfigurationError):
            profile = PatientProfile(
                population="MSM",
                age=30,
                current_prep_status="naive",
                barriers=[],
                healthcare_setting="INVALID_SETTING"
            )
            tool = LAIPrEPDecisionTool()
            tool.assess_patient(profile)


def run_tests():
    """Run all tests"""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_tests()
