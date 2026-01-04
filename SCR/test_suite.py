#!/usr/bin/env python3
"""
Systematic test suite for LAI-PrEP Decision Tool
Using simulated patient scenarios
"""

from LAI_DMT_v1 import *
import random
from datetime import datetime


class TestSuite:
    def __init__(self):
        self.tool = LAIPrEPDecisionTool()
        self.test_results = []

    def generate_test_population(self, n=1000):
        """Generate diverse test population"""
        populations = list(Population)
        settings = list(HealthcareSetting)
        barriers = list(Barrier)
        prep_statuses = ["naive", "oral_prep", "discontinued_oral"]

        test_profiles = []
        for i in range(n):
            # Random patient generation
            profile = PatientProfile(
                population=random.choice(populations),
                age=random.randint(16, 65),
                current_prep_status=random.choice(prep_statuses),
                healthcare_setting=random.choice(settings),
                barriers=random.sample(barriers, k=random.randint(0, 5)),
                recent_hiv_test=random.choice([True, False]),
                insurance_status=random.choice(["insured", "uninsured", "underinsured"])
            )
            test_profiles.append(profile)

        return test_profiles

    def validate_predictions(self, test_profiles):
        """Test tool predictions across population"""
        results = {
            'total': len(test_profiles),
            'by_population': {},
            'by_risk_level': {'Low': 0, 'Moderate': 0, 'High': 0, 'Very High': 0},
            'avg_success_rate': 0,
            'avg_improvement': 0
        }

        total_success = 0
        total_improvement = 0

        for profile in test_profiles:
            assessment = self.tool.assess_patient(profile)

            # Track by population
            pop = profile.population.value
            if pop not in results['by_population']:
                results['by_population'][pop] = {'count': 0, 'avg_success': 0}
            results['by_population'][pop]['count'] += 1
            results['by_population'][pop]['avg_success'] += assessment.adjusted_success_rate

            # Track by risk
            results['by_risk_level'][assessment.attrition_risk] += 1

            # Calculate improvements
            total_success += assessment.adjusted_success_rate
            improvement = (assessment.estimated_success_with_interventions -
                           assessment.adjusted_success_rate)
            total_improvement += improvement

        # Calculate averages
        results['avg_success_rate'] = total_success / len(test_profiles)
        results['avg_improvement'] = total_improvement / len(test_profiles)

        # Average by population
        for pop in results['by_population']:
            count = results['by_population'][pop]['count']
            results['by_population'][pop]['avg_success'] /= count

        return results

    def test_oral_prep_advantage(self):
        """Verify oral PrEP patients have higher success WITH interventions"""
        oral_profile = PatientProfile(
            population=Population.MSM,
            age=30,
            current_prep_status="oral_prep",
            recent_hiv_test=True,
            barriers=[]
        )

        naive_profile = PatientProfile(
            population=Population.MSM,
            age=30,
            current_prep_status="naive",
            recent_hiv_test=False,
            barriers=[]
        )

        oral_assessment = self.tool.assess_patient(oral_profile)
        naive_assessment = self.tool.assess_patient(naive_profile)

        # Compare SUCCESS WITH INTERVENTIONS (not just baseline)
        assert oral_assessment.estimated_success_with_interventions > naive_assessment.estimated_success_with_interventions, \
            f"Oral PrEP should have higher success: {oral_assessment.estimated_success_with_interventions:.1%} vs {naive_assessment.estimated_success_with_interventions:.1%}"

        print(f"[OK] Oral PrEP advantage confirmed:")
        print(f"  Oral PrEP with same-day switching: {oral_assessment.estimated_success_with_interventions:.1%}")
        print(f"  Naive with standard interventions: {naive_assessment.estimated_success_with_interventions:.1%}")
        print(
            f"  Advantage: +{(oral_assessment.estimated_success_with_interventions - naive_assessment.estimated_success_with_interventions) * 100:.1f} points")

    def test_barrier_impact(self):
        """Verify barriers decrease success rate"""
        no_barrier = PatientProfile(
            population=Population.CISGENDER_WOMEN,
            age=25,
            current_prep_status="naive",
            barriers=[]
        )

        with_barriers = PatientProfile(
            population=Population.CISGENDER_WOMEN,
            age=25,
            current_prep_status="naive",
            barriers=[Barrier.TRANSPORTATION, Barrier.CHILDCARE, Barrier.HOUSING_INSTABILITY]
        )

        no_barrier_assessment = self.tool.assess_patient(no_barrier)
        with_barriers_assessment = self.tool.assess_patient(with_barriers)

        assert with_barriers_assessment.adjusted_success_rate < no_barrier_assessment.adjusted_success_rate, \
            f"Barriers should decrease success rate"

        barrier_impact = (no_barrier_assessment.adjusted_success_rate -
                          with_barriers_assessment.adjusted_success_rate) * 100

        print(f"[OK] Barrier impact confirmed:")
        print(f"  No barriers: {no_barrier_assessment.adjusted_success_rate:.1%}")
        print(f"  With 3 barriers: {with_barriers_assessment.adjusted_success_rate:.1%}")
        print(f"  Impact: -{barrier_impact:.1f} points")

    def test_population_differences(self):
        """Verify different populations have different baseline rates"""
        msm = PatientProfile(
            population=Population.MSM,
            age=30,
            current_prep_status="naive",
            barriers=[]
        )

        pwid = PatientProfile(
            population=Population.PWID,
            age=30,
            current_prep_status="naive",
            barriers=[]
        )

        msm_assessment = self.tool.assess_patient(msm)
        pwid_assessment = self.tool.assess_patient(pwid)

        # PWID should have lower baseline success than MSM
        assert pwid_assessment.baseline_success_rate < msm_assessment.baseline_success_rate, \
            f"PWID should have lower baseline than MSM"

        print(f"[OK] Population differences confirmed:")
        print(f"  MSM baseline: {msm_assessment.baseline_success_rate:.1%}")
        print(f"  PWID baseline: {pwid_assessment.baseline_success_rate:.1%}")
        print(
            f"  Difference: {(msm_assessment.baseline_success_rate - pwid_assessment.baseline_success_rate) * 100:.1f} points")

    def test_intervention_effectiveness(self):
        """Verify interventions improve outcomes"""
        high_risk_profile = PatientProfile(
            population=Population.ADOLESCENT,
            age=17,
            current_prep_status="naive",
            barriers=[
                Barrier.TRANSPORTATION,
                Barrier.PRIVACY_CONCERNS,
                Barrier.LIMITED_NAVIGATION_EXPERIENCE
            ]
        )

        assessment = self.tool.assess_patient(high_risk_profile)

        improvement = (assessment.estimated_success_with_interventions -
                       assessment.adjusted_success_rate) * 100

        # Should have meaningful improvement
        assert improvement > 10, f"Interventions should provide >10 point improvement, got {improvement:.1f}"

        print(f"[OK] Intervention effectiveness confirmed:")
        print(f"  Baseline (with barriers): {assessment.adjusted_success_rate:.1%}")
        print(f"  With interventions: {assessment.estimated_success_with_interventions:.1%}")
        print(f"  Improvement: +{improvement:.1f} points")

    def run_full_validation(self):
        """Run complete validation suite"""
        print("=" * 80)
        print("LAI-PrEP DECISION TOOL VALIDATION SUITE")
        print("=" * 80)
        print()

        # Unit tests
        print("Running unit tests...")
        print("-" * 80)

        try:
            self.test_oral_prep_advantage()
            print()
        except AssertionError as e:
            print(f"[FAILED] Oral PrEP advantage test FAILED: {e}")
            print()

        try:
            self.test_barrier_impact()
            print()
        except AssertionError as e:
            print(f"[FAILED] Barrier impact test FAILED: {e}")
            print()

        try:
            self.test_population_differences()
            print()
        except AssertionError as e:
            print(f"[FAILED] Population differences test FAILED: {e}")
            print()

        try:
            self.test_intervention_effectiveness()
            print()
        except AssertionError as e:
            print(f"[FAILED] Intervention effectiveness test FAILED: {e}")
            print()

        # Population tests
        print("=" * 80)
        print("Generating test population (n=1000)...")
        test_profiles = self.generate_test_population(1000)

        print("Validating predictions...")
        results = self.validate_predictions(test_profiles)

        print("\nPOPULATION VALIDATION RESULTS:")
        print("-" * 80)
        print(f"Total profiles tested: {results['total']}")
        print(f"Average success rate: {results['avg_success_rate']:.1%}")
        print(f"Average improvement with interventions: +{results['avg_improvement'] * 100:.1f} points")
        print()

        print("By Population:")
        for pop, data in sorted(results['by_population'].items()):
            print(f"  {pop}: {data['count']} patients, {data['avg_success']:.1%} avg success")
        print()

        print("By Risk Level:")
        for risk, count in results['by_risk_level'].items():
            pct = count / results['total'] * 100
            print(f"  {risk}: {count} ({pct:.1f}%)")

        print("\n" + "=" * 80)
        print("Validation complete!")
        print("=" * 80)

        return results


class ImplementationTracker:
    """Track real-world outcomes to validate tool"""

    def __init__(self, clinic_name):
        self.clinic_name = clinic_name
        self.prescriptions = []

    def log_prescription(self, patient_profile, predicted_assessment):
        """Log prediction at prescription time"""
        self.prescriptions.append({
            'date': datetime.now(),
            'profile': patient_profile,
            'predicted_success': predicted_assessment.adjusted_success_rate,
            'predicted_interventions': predicted_assessment.recommended_interventions,
            'actual_outcome': None  # Fill in later
        })

        return len(self.prescriptions) - 1  # Return prescription ID

    def log_outcome(self, prescription_id, initiated, days_to_injection=None):
        """Log actual outcome"""
        if prescription_id < len(self.prescriptions):
            self.prescriptions[prescription_id]['actual_outcome'] = {
                'initiated': initiated,
                'days': days_to_injection
            }

    def validate_predictions(self):
        """Compare predictions to actual outcomes"""
        if not self.prescriptions:
            return None

        completed = [rx for rx in self.prescriptions if rx['actual_outcome'] is not None]

        if not completed:
            return None

        correct_predictions = 0
        total_predictions = len(completed)

        for rx in completed:
            predicted = rx['predicted_success'] > 0.5
            actual = rx['actual_outcome']['initiated']
            if predicted == actual:
                correct_predictions += 1

        accuracy = correct_predictions / total_predictions

        results = {
            'clinic': self.clinic_name,
            'total_prescriptions': len(self.prescriptions),
            'completed_outcomes': total_predictions,
            'accuracy': accuracy,
            'correct_predictions': correct_predictions
        }

        return results

    def export_data(self, filename):
        """Export data for analysis"""
        import json
        with open(filename, 'w') as f:
            # Convert enums to strings for JSON serialization
            export_data = []
            for rx in self.prescriptions:
                export_rx = {
                    'date': rx['date'].isoformat(),
                    'population': rx['profile'].population.value,
                    'age': rx['profile'].age,
                    'prep_status': rx['profile'].current_prep_status,
                    'predicted_success': rx['predicted_success'],
                    'actual_outcome': rx['actual_outcome']
                }
                export_data.append(export_rx)

            json.dump(export_data, f, indent=2)


if __name__ == "__main__":
    suite = TestSuite()
    results = suite.run_full_validation()