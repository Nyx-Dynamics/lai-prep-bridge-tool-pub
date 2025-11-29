#!/usr/bin/env python3
"""
LAI-PrEP Bridge Period Decision Support Tool v2.1
Enhanced with Mechanism Diversity, JSON Export, and Explainability

New Features in v2.1:
- Mechanism tagging to prevent redundant interventions
- JSON export for machine-readable results
- Explainability methods for clinical reasoning
- Confidence intervals for estimates
- Logit-space calculations (optional)
- CLI support via importable functions
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np


class ConfigurationError(Exception):
    """Raised when configuration file is invalid or missing"""
    pass


class Configuration:
    """Manages tool configuration from JSON file"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration from JSON file
        
        Args:
            config_path: Path to configuration JSON file. If None, looks in default locations.
        """
        if config_path is None:
            config_path = self._find_config_file()
        
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()
        
    def _find_config_file(self) -> str:
        """Find configuration file in standard locations"""
        search_paths = [
            "lai_prep_config.json",
            "config/global_params.json",
            "config/lai_prep_config.json",
            str(Path(__file__).parent / "lai_prep_config.json"),
            "/mnt/user-data/outputs/lai_prep_config.json"
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
                
        raise ConfigurationError(
            f"Configuration file not found. Searched: {search_paths}"
        )
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {e}")
        except IOError as e:
            raise ConfigurationError(f"Cannot read config file: {e}")
    
    def _validate_config(self):
        """Validate required configuration sections exist"""
        required_sections = [
            'populations', 'barriers', 'interventions', 
            'healthcare_settings', 'risk_categories', 'algorithm_parameters'
        ]
        
        missing = [s for s in required_sections if s not in self.config]
        if missing:
            raise ConfigurationError(
                f"Missing required config sections: {missing}"
            )
    
    def get_population_config(self, population: str) -> Dict:
        """Get configuration for specific population"""
        if population not in self.config['populations']:
            raise ConfigurationError(f"Unknown population: {population}")
        return self.config['populations'][population]
    
    def get_barrier_config(self, barrier: str) -> Dict:
        """Get configuration for specific barrier"""
        if barrier not in self.config['barriers']:
            raise ConfigurationError(f"Unknown barrier: {barrier}")
        return self.config['barriers'][barrier]
    
    def get_intervention_config(self, intervention: str) -> Dict:
        """Get configuration for specific intervention"""
        if intervention not in self.config['interventions']:
            raise ConfigurationError(f"Unknown intervention: {intervention}")
        return self.config['interventions'][intervention]
    
    def get_setting_config(self, setting: str) -> Dict:
        """Get configuration for specific healthcare setting"""
        if setting not in self.config['healthcare_settings']:
            raise ConfigurationError(f"Unknown setting: {setting}")
        return self.config['healthcare_settings'][setting]
    
    def get_algorithm_params(self) -> Dict:
        """Get algorithm parameters"""
        return self.config['algorithm_parameters']
    
    def get_risk_categories(self) -> Dict:
        """Get risk stratification categories"""
        return self.config['risk_categories']
    
    def get_clinical_guidance(self) -> Dict:
        """Get clinical guidance messages"""
        return self.config.get('clinical_guidance', {})


@dataclass
class PatientProfile:
    """Patient characteristics affecting bridge period success"""
    population: str  # Population key from config
    age: int
    current_prep_status: str  # "naive", "oral_prep", "discontinued_oral"
    barriers: List[str] = field(default_factory=list)  # Barrier keys from config
    healthcare_setting: str = "COMMUNITY_HEALTH_CENTER"  # Setting key from config
    insurance_status: str = "insured"  # "insured", "uninsured", "underinsured", "parental"
    recent_hiv_test: bool = False  # Within 7 days
    transportation_access: bool = True
    childcare_needs: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PatientProfile':
        """Create PatientProfile from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class InterventionRecommendation:
    """Recommended intervention with expected impact"""
    intervention: str  # Intervention key from config
    intervention_name: str
    priority: str  # "Critical", "High", "Moderate"
    expected_improvement: float  # Percentage point improvement
    implementation_notes: str
    evidence_level: str  # "Strong", "Moderate", "Emerging"
    cost_level: str  # From config
    implementation_complexity: str  # From config
    mechanisms: List[str] = field(default_factory=list)  # Mechanism tags
    confidence_interval: Tuple[float, float] = field(default=(0.0, 0.0))  # CI
    rationale: str = ""  # Explanation for selection
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class BridgePeriodAssessment:
    """Complete assessment with predictions and recommendations"""
    baseline_success_rate: float
    adjusted_success_rate: float
    attrition_risk: str  # "Low", "Moderate", "High", "Very High"
    attrition_risk_category: Dict  # Full category info from config
    key_barriers: List[str]
    barrier_details: List[Dict]  # Full barrier info from config
    recommended_interventions: List[InterventionRecommendation]
    estimated_bridge_duration_days: Tuple[int, int]  # (min, max)
    estimated_success_with_interventions: float
    clinical_notes: List[str]
    population_info: Dict  # Full population info from config
    attrition_factors: Dict = field(default_factory=dict)  # NEW: Explanation
    delay_factors: List[str] = field(default_factory=list)  # NEW: Bridge delays
    
    def to_json(self, profile: PatientProfile, tool_version: str = "2.1.0") -> Dict:
        """Export assessment as machine-readable JSON"""
        return {
            "patient_profile": {
                "population": profile.population,
                "population_name": self.population_info['name'],
                "age": profile.age,
                "prep_status": profile.current_prep_status,
                "barriers": profile.barriers,
                "barrier_names": [self.barrier_details[i]['name'] 
                                 for i in range(len(profile.barriers[:5]))],
                "healthcare_setting": profile.healthcare_setting,
                "insurance_status": profile.insurance_status
            },
            "risk_assessment": {
                "level": self.attrition_risk,
                "baseline_success": round(self.baseline_success_rate, 4),
                "adjusted_success": round(self.adjusted_success_rate, 4),
                "attrition_factors": self.attrition_factors,
                "evidence_base": {
                    "source": self.population_info.get('evidence_source', ''),
                    "level": self.population_info.get('evidence_level', '')
                }
            },
            "recommendations": [
                {
                    "intervention": rec.intervention,
                    "intervention_name": rec.intervention_name,
                    "priority": rec.priority,
                    "expected_improvement": round(rec.expected_improvement, 4),
                    "rationale": rec.rationale,
                    "evidence": rec.evidence_level,
                    "mechanisms": rec.mechanisms,
                    "cost_level": rec.cost_level,
                    "implementation_complexity": rec.implementation_complexity,
                    "confidence_interval": {
                        "lower": round(rec.confidence_interval[0], 4),
                        "upper": round(rec.confidence_interval[1], 4)
                    }
                }
                for rec in self.recommended_interventions
            ],
            "predictions": {
                "without_interventions": round(self.adjusted_success_rate, 4),
                "with_interventions": round(self.estimated_success_with_interventions, 4),
                "absolute_improvement": round(
                    self.estimated_success_with_interventions - self.adjusted_success_rate, 4
                ),
                "relative_improvement_pct": round(
                    (self.estimated_success_with_interventions / 
                     self.adjusted_success_rate - 1) * 100, 2
                ) if self.adjusted_success_rate > 0 else 0
            },
            "bridge_period_estimate": {
                "minimum_days": self.estimated_bridge_duration_days[0],
                "maximum_days": self.estimated_bridge_duration_days[1],
                "target_days": 14,
                "delay_factors": self.delay_factors
            },
            "metadata": {
                "tool_version": tool_version,
                "timestamp": datetime.now().isoformat(),
                "config_version": tool_version
            }
        }


class LAIPrEPDecisionTool:
    """Main decision support tool for LAI-PrEP implementation"""
    
    # Mechanism categories for diversity scoring
    MECHANISM_CATEGORIES = {
        'eliminate_bridge': ['ORAL_TO_INJECTABLE', 'SAME_DAY_SWITCHING'],
        'compress_bridge': ['ACCELERATED_TESTING', 'EXPEDITED_AUTHORIZATION'],
        'navigate_bridge': ['PATIENT_NAVIGATION', 'PEER_NAVIGATION', 'TEXT_MESSAGE_NAVIGATION'],
        'remove_barriers': ['TRANSPORTATION_SUPPORT', 'CHILDCARE_SUPPORT', 'MOBILE_DELIVERY'],
        'system_level': ['HARM_REDUCTION_INTEGRATION', 'BUNDLED_PAYMENT', 'TELEHEALTH_COUNSELING']
    }
    
    def __init__(self, config_path: Optional[str] = None, use_logit: bool = False):
        """
        Initialize decision tool with configuration
        
        Args:
            config_path: Path to configuration JSON file
            use_logit: Whether to use logit-space calculations (more mathematically sound)
        """
        self.config = Configuration(config_path)
        self.params = self.config.get_algorithm_params()
        self.risk_categories = self.config.get_risk_categories()
        self.use_logit = use_logit
    
    def assess_patient(self, profile: PatientProfile) -> BridgePeriodAssessment:
        """
        Perform complete bridge period assessment for a patient
        
        Args:
            profile: PatientProfile with patient characteristics
            
        Returns:
            BridgePeriodAssessment with predictions and recommendations
        """
        # Get population configuration
        pop_config = self.config.get_population_config(profile.population)
        baseline_attrition = pop_config['baseline_attrition']
        
        # Calculate adjusted success rate
        if self.use_logit:
            adjusted_success_rate, attrition_factors = self._calculate_adjusted_success_logit(
                profile, baseline_attrition
            )
        else:
            adjusted_success_rate, attrition_factors = self._calculate_adjusted_success_linear(
                profile, baseline_attrition
            )
        
        baseline_success_rate = 1 - baseline_attrition
        
        # Best-case success floor: oral PrEP + recent HIV test + no barriers
        # Ensures zero-barrier best-case scenarios reflect real-world high success when the bridge can be eliminated
        if (
            profile.current_prep_status == "oral_prep"
            and profile.recent_hiv_test
            and len(profile.barriers) == 0
        ):
            best_case_floor = self.params.get('best_case_success_floor', 0.85)
            adjusted_success_rate = max(adjusted_success_rate, best_case_floor)
        
        # Determine attrition risk category
        attrition_risk, risk_category = self._categorize_risk(1 - adjusted_success_rate)
        
        # Generate intervention recommendations with mechanism diversity
        recommendations = self._generate_recommendations_with_mechanisms(profile)
        
        # Calculate estimated success with interventions
        intervention_improvements = sum(
            rec.expected_improvement / 100  # Convert percentage points to decimal
            for rec in recommendations[:3]  # Top 3 interventions
        )
        
        # Apply diminishing returns factor
        estimated_success = min(
            self.params['max_success_rate_with_interventions'],
            adjusted_success_rate + (
                intervention_improvements * 
                self.params['intervention_diminishing_returns_factor']
            )
        )
        
        # Estimate bridge duration
        bridge_duration = self._estimate_bridge_duration(profile)
        
        # Identify delay factors
        delay_factors = self._identify_delay_factors(profile)
        
        # Generate clinical notes
        clinical_notes = self._generate_clinical_notes(
            profile, 1 - adjusted_success_rate, pop_config
        )
        
        # Get barrier details
        barrier_details = [
            self.config.get_barrier_config(b) for b in profile.barriers
        ]
        
        return BridgePeriodAssessment(
            baseline_success_rate=baseline_success_rate,
            adjusted_success_rate=adjusted_success_rate,
            attrition_risk=attrition_risk,
            attrition_risk_category=risk_category,
            key_barriers=profile.barriers[:5],  # Top 5 barriers
            barrier_details=barrier_details[:5],
            recommended_interventions=recommendations,
            estimated_bridge_duration_days=bridge_duration,
            estimated_success_with_interventions=estimated_success,
            clinical_notes=clinical_notes,
            population_info=pop_config,
            attrition_factors=attrition_factors,
            delay_factors=delay_factors
        )
    
    def _calculate_adjusted_success_linear(
        self, 
        profile: PatientProfile, 
        baseline_attrition: float
    ) -> Tuple[float, Dict]:
        """Calculate success rate using linear adjustment (original method)"""
        # Adjust for individual barriers
        barrier_adjustment = sum(
            self.config.get_barrier_config(barrier)['impact'] 
            for barrier in profile.barriers
        )
        
        # Apply barrier count adjustment
        barrier_count = len(profile.barriers)
        if barrier_count >= 3:
            barrier_adjustment += self.params['barrier_count_adjustment_factor']['3_plus_barriers']
        elif barrier_count == 2:
            barrier_adjustment += self.params['barrier_count_adjustment_factor']['2_barriers']
        elif barrier_count == 1:
            barrier_adjustment += self.params['barrier_count_adjustment_factor']['1_barrier']
        
        # Cap adjustment to prevent impossible values
        adjusted_attrition = min(
            self.params['max_attrition_ceiling'],
            baseline_attrition + barrier_adjustment
        )
        
        # Build explanation
        attrition_factors = {
            "baseline_attrition": round(baseline_attrition, 4),
            "barrier_impacts": {
                barrier: round(self.config.get_barrier_config(barrier)['impact'], 4)
                for barrier in profile.barriers
            },
            "barrier_count_penalty": round(
                barrier_adjustment - sum(
                    self.config.get_barrier_config(b)['impact'] for b in profile.barriers
                ), 4
            ),
            "total_adjustment": round(barrier_adjustment, 4),
            "adjusted_attrition": round(adjusted_attrition, 4)
        }
        
        return 1 - adjusted_attrition, attrition_factors
    
    def _calculate_adjusted_success_logit(
        self, 
        profile: PatientProfile, 
        baseline_attrition: float
    ) -> Tuple[float, Dict]:
        """Calculate success rate using logit space (more mathematically sound)"""
        
        def logit(p):
            """Convert probability to log-odds"""
            p = max(0.01, min(0.99, p))  # Bound to avoid infinity
            return np.log(p / (1 - p))
        
        def inv_logit(x):
            """Convert log-odds to probability"""
            return 1 / (1 + np.exp(-x))
        
        # Start with baseline in logit space
        base_logit = logit(baseline_attrition)
        
        # Add barrier effects (negative log-odds shifts)
        barrier_logits = {}
        for barrier in profile.barriers:
            barrier_impact = self.config.get_barrier_config(barrier)['impact']
            # Convert impact to log-odds shift
            # Larger impacts create larger shifts in log-odds
            barrier_logit_shift = logit(min(0.99, baseline_attrition + barrier_impact)) - base_logit
            base_logit += barrier_logit_shift
            barrier_logits[barrier] = round(float(barrier_logit_shift), 4)
        
        # Apply barrier count penalty in logit space
        barrier_count = len(profile.barriers)
        count_penalty = 0
        if barrier_count >= 3:
            count_penalty = self.params['barrier_count_adjustment_factor']['3_plus_barriers']
        elif barrier_count == 2:
            count_penalty = self.params['barrier_count_adjustment_factor']['2_barriers']
        elif barrier_count == 1:
            count_penalty = self.params['barrier_count_adjustment_factor']['1_barrier']
        
        if count_penalty > 0:
            base_logit += logit(min(0.99, baseline_attrition + count_penalty)) - logit(baseline_attrition)
        
        # Convert back to probability
        adjusted_attrition = float(inv_logit(base_logit))
        
        # Ensure bounds
        adjusted_attrition = max(0.05, min(0.95, adjusted_attrition))
        
        # Build explanation
        attrition_factors = {
            "method": "logit_space",
            "baseline_attrition": round(baseline_attrition, 4),
            "baseline_logit": round(float(logit(baseline_attrition)), 4),
            "barrier_logit_shifts": barrier_logits,
            "barrier_count_penalty": round(count_penalty, 4),
            "adjusted_attrition": round(adjusted_attrition, 4),
            "adjusted_logit": round(float(base_logit), 4)
        }
        
        return 1 - adjusted_attrition, attrition_factors
    
    def _categorize_risk(self, attrition_rate: float) -> Tuple[str, Dict]:
        """Categorize attrition risk level using configuration"""
        for category_name, category_info in self.risk_categories.items():
            threshold_min = category_info.get('threshold_min', 0)
            threshold_max = category_info.get('threshold_max', 1.0)
            
            if threshold_min <= attrition_rate < threshold_max:
                return category_info['label'], category_info
        
        # Default to VERY_HIGH if no match
        return self.risk_categories['VERY_HIGH']['label'], self.risk_categories['VERY_HIGH']
    
    def _generate_recommendations_with_mechanisms(
        self, 
        profile: PatientProfile
    ) -> List[InterventionRecommendation]:
        """
        Generate prioritized intervention recommendations with mechanism diversity
        
        This method prevents recommending multiple interventions that work through
        the same mechanism, applying overlap penalties.
        """
        # Generate all candidate recommendations
        candidates = self._generate_candidate_recommendations(profile)
        
        # Sort by priority and expected improvement
        priority_order = {"Critical": 0, "High": 1, "Moderate": 2}
        candidates.sort(
            key=lambda x: (priority_order.get(x.priority, 3), -x.expected_improvement)
        )
        
        # Select recommendations with mechanism diversity
        selected = []
        used_mechanisms = set()
        
        for candidate in candidates:
            if len(selected) >= 5:  # Limit to top 5 recommendations
                break
            
            # Calculate mechanism overlap
            overlap_count = len(set(candidate.mechanisms) & used_mechanisms)
            
            # Apply overlap penalty (10% reduction per overlapping mechanism)
            if overlap_count > 0:
                original_improvement = candidate.expected_improvement
                candidate.expected_improvement *= (0.9 ** overlap_count)
                
                # Add note about penalty
                if candidate.rationale:
                    candidate.rationale += f" (Note: {overlap_count} mechanism overlap, " \
                                          f"adjusted from {original_improvement:.1f}%)"
            
            selected.append(candidate)
            used_mechanisms.update(candidate.mechanisms)
        
        return selected
    
    def _generate_candidate_recommendations(
        self, 
        profile: PatientProfile
    ) -> List[InterventionRecommendation]:
        """Generate all candidate intervention recommendations"""
        recommendations = []
        
        # Strategy 1: Eliminate the bridge (oral-to-injectable transitions)
        if profile.current_prep_status == "oral_prep":
            if profile.recent_hiv_test:
                recommendations.append(self._create_recommendation(
                    'SAME_DAY_SWITCHING',
                    priority="Critical",
                    rationale="Patient on oral PrEP with recent HIV test - can eliminate "
                             "bridge period entirely with same-day switching protocol.",
                    mechanisms=['eliminate_bridge', 'reduce_appointments']
                ))
            else:
                recommendations.append(self._create_recommendation(
                    'ORAL_TO_INJECTABLE',
                    priority="Critical",
                    rationale="Patient on oral PrEP - oral-to-injectable transition has "
                             "1.5-fold higher success rate than PrEP-naive initiation.",
                    mechanisms=['eliminate_bridge', 'leverage_engagement']
                ))
        
        # Strategy 2: Compress the bridge (accelerated testing)
        if not profile.recent_hiv_test:
            recommendations.append(self._create_recommendation(
                'ACCELERATED_TESTING',
                priority="High",
                rationale="RNA testing reduces window period from 33-45 days to 10-14 days, "
                         "compressing bridge duration.",
                mechanisms=['compress_bridge', 'reduce_delays']
            ))
        
        # Strategy 3: Navigate the bridge (patient navigation)
        pop_config = self.config.get_population_config(profile.population)
        if pop_config['baseline_attrition'] > 0.50:  # High baseline risk
            if profile.population == 'PWID':
                recommendations.append(self._create_recommendation(
                    'PEER_NAVIGATION',
                    priority="High",
                    rationale=f"PWID population with high attrition risk ({pop_config['baseline_attrition']:.0%}) - "
                             "peer navigation particularly effective for building trust.",
                    mechanisms=['navigate_bridge', 'peer_support', 'reduce_stigma']
                ))
            else:
                recommendations.append(self._create_recommendation(
                    'PATIENT_NAVIGATION',
                    priority="High",
                    rationale=f"{pop_config['name']} with high attrition risk ({pop_config['baseline_attrition']:.0%}) - "
                             "navigation demonstrates 1.5-fold improvement in initiation.",
                    mechanisms=['navigate_bridge', 'coordination', 'barrier_identification']
                ))
        
        # Barrier-specific interventions
        for barrier in profile.barriers:
            barrier_config = self.config.get_barrier_config(barrier)
            
            # Find interventions that address this barrier
            for int_key, int_config in self.config.config['interventions'].items():
                if 'addresses_barriers' in int_config:
                    if barrier in int_config['addresses_barriers']:
                        # Check if intervention is already recommended
                        if int_key not in [r.intervention for r in recommendations]:
                            # Check if applicable to this population
                            if ('applicable_populations' not in int_config or
                                profile.population in int_config['applicable_populations']):
                                
                                mechanisms = self._determine_mechanisms(int_key)
                                recommendations.append(self._create_recommendation(
                                    int_key,
                                    priority="High",
                                    rationale=f"Addresses {barrier_config['name']} barrier "
                                             f"(+{barrier_config['impact']*100:.0f}% attrition impact).",
                                    mechanisms=mechanisms
                                ))
        
        # PWID-specific intervention
        if profile.population == 'PWID':
            if profile.healthcare_setting != 'HARM_REDUCTION':
                if 'HARM_REDUCTION_INTEGRATION' not in [r.intervention for r in recommendations]:
                    recommendations.append(self._create_recommendation(
                        'HARM_REDUCTION_INTEGRATION',
                        priority="Critical",
                        rationale="PWID population - harm reduction integration essential for "
                                 "trust-building and low-barrier access.",
                        mechanisms=['system_level', 'reduce_stigma', 'leverage_trust']
                    ))
        
        # Universal low-cost interventions
        if 'TEXT_MESSAGE_NAVIGATION' not in [r.intervention for r in recommendations]:
            recommendations.append(self._create_recommendation(
                'TEXT_MESSAGE_NAVIGATION',
                priority="Moderate",
                rationale="Low-cost universal intervention - SMS reminders improve appointment "
                         "attendance by 20-30%.",
                mechanisms=['navigate_bridge', 'reminder_system']
            ))
        
        # Setting-specific recommendations
        setting_config = self.config.get_setting_config(profile.healthcare_setting)
        if 'recommended_interventions' in setting_config:
            for int_key in setting_config['recommended_interventions']:
                if int_key not in [r.intervention for r in recommendations]:
                    int_config = self.config.get_intervention_config(int_key)
                    # Check applicability
                    if ('applicable_populations' not in int_config or
                        profile.population in int_config['applicable_populations']):
                        
                        mechanisms = self._determine_mechanisms(int_key)
                        recommendations.append(self._create_recommendation(
                            int_key,
                            priority="Moderate",
                            rationale=f"Optimized for {setting_config['name']} setting.",
                            mechanisms=mechanisms
                        ))
        
        return recommendations
    
    def _create_recommendation(
        self, 
        intervention_key: str, 
        priority: str,
        rationale: str,
        mechanisms: List[str]
    ) -> InterventionRecommendation:
        """Create an intervention recommendation with all metadata"""
        int_config = self.config.get_intervention_config(intervention_key)
        
        # Calculate confidence interval (±20% of point estimate)
        improvement = int_config['improvement'] * 100
        ci_width = improvement * 0.20
        confidence_interval = (
            max(0, improvement - ci_width),
            min(50, improvement + ci_width)
        )
        
        return InterventionRecommendation(
            intervention=intervention_key,
            intervention_name=int_config['name'],
            priority=priority,
            expected_improvement=improvement,
            implementation_notes=int_config['note'],
            evidence_level=int_config['evidence_level'],
            cost_level=int_config['cost_level'],
            implementation_complexity=int_config['implementation_complexity'],
            mechanisms=mechanisms,
            confidence_interval=confidence_interval,
            rationale=rationale
        )
    
    def _determine_mechanisms(self, intervention_key: str) -> List[str]:
        """Determine mechanism categories for an intervention"""
        mechanisms = []
        
        for category, interventions in self.MECHANISM_CATEGORIES.items():
            if intervention_key in interventions:
                mechanisms.append(category)
        
        # Add specific mechanism tags based on intervention type
        if 'NAVIGATION' in intervention_key:
            mechanisms.append('coordination')
        if 'SUPPORT' in intervention_key:
            mechanisms.append('remove_barriers')
        if 'TESTING' in intervention_key or 'AUTHORIZATION' in intervention_key:
            mechanisms.append('reduce_delays')
        if 'HARM_REDUCTION' in intervention_key or 'PEER' in intervention_key:
            mechanisms.append('reduce_stigma')
        if 'MOBILE' in intervention_key or 'TELEHEALTH' in intervention_key:
            mechanisms.append('increase_access')
        
        return mechanisms if mechanisms else ['general']
    
    def _estimate_bridge_duration(
        self, 
        profile: PatientProfile
    ) -> Tuple[int, int]:
        """Estimate bridge period duration in days"""
        if profile.current_prep_status == "oral_prep" and profile.recent_hiv_test:
            return tuple(self.params['bridge_duration_oral_prep_recent_test'])
        elif profile.current_prep_status == "oral_prep":
            return tuple(self.params['bridge_duration_oral_prep_no_recent_test'])
        else:
            # PrEP-naive: depends on testing strategy and barriers
            if profile.recent_hiv_test:
                min_days, max_days = self.params['bridge_duration_naive_recent_test']
            else:
                min_days, max_days = self.params['bridge_duration_naive_no_recent_test']
            
            # Adjust max based on barrier count
            if len(profile.barriers) > 2:
                max_days = self.params['maximum_bridge_duration_days']
            
            return (min_days, max_days)
    
    def _identify_delay_factors(self, profile: PatientProfile) -> List[str]:
        """Identify factors that may extend bridge period"""
        factors = []
        
        if not profile.recent_hiv_test:
            factors.append("HIV testing required (adds 3-7 days for results)")
        
        if profile.insurance_status in ["uninsured", "underinsured"]:
            factors.append("Insurance authorization may be complex")
        elif profile.insurance_status == "parental":
            factors.append("Parental insurance may raise privacy concerns")
        
        if not profile.transportation_access:
            factors.append("Transportation barriers may delay appointments")
        
        if profile.childcare_needs:
            factors.append("Childcare coordination needed for appointments")
        
        if len(profile.barriers) > 3:
            factors.append(f"{len(profile.barriers)} barriers present - multiple coordination challenges")
        
        if profile.healthcare_setting in ["ACADEMIC_MEDICAL_CENTER"]:
            factors.append("Complex healthcare system may extend navigation time")
        
        return factors
    
    def _generate_clinical_notes(
        self,
        profile: PatientProfile,
        attrition_rate: float,
        pop_config: Dict
    ) -> List[str]:
        """Generate clinical guidance notes"""
        notes = []
        guidance = self.config.get_clinical_guidance()
        
        # Risk level note
        _, risk_category = self._categorize_risk(attrition_rate)
        notes.append(
            f"{risk_category['icon']} {risk_category['label'].upper()}: "
            f"{risk_category['clinical_action']} ({attrition_rate:.0%} attrition risk)"
        )
        
        # Population-specific notes
        if 'clinical_notes' in pop_config:
            notes.append(f"📋 {pop_config['clinical_notes']}")
        
        # PrEP status notes
        if profile.current_prep_status == "oral_prep":
            if 'oral_prep_transition_priority' in guidance:
                notes.append(f"💊 {guidance['oral_prep_transition_priority']['message']}")
        elif profile.current_prep_status == "discontinued_oral":
            if 'discontinued_oral_prep' in guidance:
                notes.append(f"💊 {guidance['discontinued_oral_prep']['message']}")
        
        # High barrier count warning
        if len(profile.barriers) > 3:
            notes.append(f"⚠️  {len(profile.barriers)} barriers identified - "
                        "multiple intensive interventions will be required")
        
        # Evidence base
        if 'evidence_base' in guidance:
            notes.append(f"📊 {guidance['evidence_base']['message']}")
        
        return notes
    
    def generate_report(
        self, 
        profile: PatientProfile, 
        assessment: BridgePeriodAssessment
    ) -> str:
        """Generate formatted clinical report"""
        report = []
        report.append("=" * 80)
        report.append("LAI-PrEP BRIDGE PERIOD ASSESSMENT")
        report.append(f"Tool Version: {self.config.config.get('version', 'Unknown')} (Enhanced)")
        report.append(f"Calculation Method: {'Logit Space' if self.use_logit else 'Linear'}")
        report.append("=" * 80)
        report.append("")
        
        # Patient characteristics
        report.append("PATIENT PROFILE")
        report.append("-" * 80)
        report.append(f"Population: {assessment.population_info['name']}")
        report.append(f"  Evidence Level: {assessment.population_info['evidence_level']}")
        report.append(f"  Evidence Source: {assessment.population_info['evidence_source']}")
        report.append(f"Age: {profile.age} years")
        report.append(f"Current PrEP Status: {profile.current_prep_status}")
        
        # Healthcare setting
        setting_config = self.config.get_setting_config(profile.healthcare_setting)
        report.append(f"Healthcare Setting: {setting_config['name']}")
        
        report.append(f"Insurance: {profile.insurance_status}")
        
        if profile.barriers:
            report.append(f"\nIdentified Barriers ({len(profile.barriers)}):")
            for barrier_key, barrier_detail in zip(
                assessment.key_barriers, 
                assessment.barrier_details
            ):
                report.append(f"  • {barrier_detail['name']}")
                report.append(f"    Impact: +{barrier_detail['impact']*100:.1f} pts | "
                            f"Evidence: {barrier_detail['evidence_level']}")
        report.append("")
        
        # Risk assessment
        report.append("BRIDGE PERIOD SUCCESS PREDICTION")
        report.append("-" * 80)
        report.append(f"Population Baseline Success Rate: "
                     f"{assessment.baseline_success_rate:.1%}")
        report.append(f"Adjusted Success Rate (with barriers): "
                     f"{assessment.adjusted_success_rate:.1%}")
        report.append(f"Attrition Risk Level: {assessment.attrition_risk}")
        report.append(f"Estimated Bridge Duration: "
                     f"{assessment.estimated_bridge_duration_days[0]}-"
                     f"{assessment.estimated_bridge_duration_days[1]} days")
        
        if assessment.delay_factors:
            report.append(f"\nPotential Delay Factors:")
            for factor in assessment.delay_factors[:5]:
                report.append(f"  • {factor}")
        
        report.append("")
        report.append(f"💡 With recommended interventions: "
                     f"{assessment.estimated_success_with_interventions:.1%} success")
        improvement = (assessment.estimated_success_with_interventions - 
                      assessment.adjusted_success_rate) * 100
        report.append(f"   Potential improvement: +{improvement:.1f} percentage points "
                     f"({improvement/assessment.adjusted_success_rate*100:.0f}% relative)")
        report.append("")
        
        # Recommendations with mechanism tags
        report.append("RECOMMENDED INTERVENTIONS (With Mechanism Diversity)")
        report.append("-" * 80)
        for i, rec in enumerate(assessment.recommended_interventions[:5], 1):
            report.append(f"\n{i}. {rec.intervention_name}")
            report.append(f"   Priority: {rec.priority}")
            report.append(f"   Expected Improvement: +{rec.expected_improvement:.1f} percentage points")
            report.append(f"   Confidence Interval: [{rec.confidence_interval[0]:.1f}%, "
                         f"{rec.confidence_interval[1]:.1f}%]")
            report.append(f"   Evidence Level: {rec.evidence_level} | "
                         f"Cost: {rec.cost_level} | "
                         f"Complexity: {rec.implementation_complexity}")
            report.append(f"   Mechanisms: {', '.join(rec.mechanisms)}")
            report.append(f"   Rationale: {rec.rationale}")
        report.append("")
        
        # Clinical notes
        report.append("CLINICAL GUIDANCE")
        report.append("-" * 80)
        for note in assessment.clinical_notes:
            # Wrap long notes
            if len(note) > 76:
                words = note.split()
                lines = []
                current_line = words[0]
                for word in words[1:]:
                    if len(current_line + " " + word) <= 76:
                        current_line += " " + word
                    else:
                        lines.append(current_line)
                        current_line = "  " + word
                lines.append(current_line)
                report.extend(lines)
            else:
                report.append(note)
        report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append("Based on: Demidont & Backus (2025). Bridging the Gap: The PrEP")
        report.append("Cascade Paradigm Shift for Long-Acting Injectable HIV Prevention.")
        report.append("Enhanced with mechanism diversity scoring and explainability.")
        report.append(f"Configuration Version: {self.config.config.get('version', 'Unknown')}")
        report.append("=" * 80)
        
        return "\n".join(report)


def assess_patient_json(
    patient_data: Dict, 
    config_path: Optional[str] = None,
    use_logit: bool = False
) -> Dict:
    """
    Assess a patient and return JSON results (for CLI/API use)
    
    Args:
        patient_data: Dictionary with patient profile data
        config_path: Optional path to configuration file
        use_logit: Whether to use logit-space calculations
        
    Returns:
        Dictionary with assessment results
    """
    tool = LAIPrEPDecisionTool(config_path=config_path, use_logit=use_logit)
    profile = PatientProfile.from_dict(patient_data)
    assessment = tool.assess_patient(profile)
    return assessment.to_json(profile, tool_version="2.1.0")


def main():
    """Example usage and testing"""
    print("LAI-PrEP BRIDGE PERIOD DECISION SUPPORT TOOL v2.1")
    print("Enhanced with Mechanisms, JSON Export, and Explainability")
    print("=" * 80)
    print()
    
    try:
        # Test both linear and logit methods
        for use_logit in [False, True]:
            method = "Logit Space" if use_logit else "Linear"
            print(f"\n{'='*80}")
            print(f"TESTING WITH {method.upper()} METHOD")
            print(f"{'='*80}\n")
            
            tool = LAIPrEPDecisionTool(use_logit=use_logit)
            print(f"✓ Configuration loaded: {tool.config.config_path}")
            print(f"✓ Calculation method: {method}")
            print()
            
            # Example: PWID with multiple barriers
            print(f"EXAMPLE: Person Who Injects Drugs ({method})")
            print("-" * 80)
            profile = PatientProfile(
                population="PWID",
                age=35,
                current_prep_status="naive",
                recent_hiv_test=False,
                healthcare_setting="COMMUNITY_HEALTH_CENTER",
                barriers=[
                    "HOUSING_INSTABILITY",
                    "TRANSPORTATION",
                    "LEGAL_CONCERNS",
                    "HEALTHCARE_DISCRIMINATION"
                ],
                insurance_status="uninsured",
                transportation_access=False
            )
            
            assessment = tool.assess_patient(profile)
            print(tool.generate_report(profile, assessment))
            
            # Export to JSON
            json_output = assessment.to_json(profile)
            print("\n\nJSON OUTPUT (First 50 lines):")
            print("-" * 80)
            json_str = json.dumps(json_output, indent=2)
            print('\n'.join(json_str.split('\n')[:50]))
            print("...")
            
            if not use_logit:  # Only show comparison once
                print("\n\n")
    
    except ConfigurationError as e:
        print(f"❌ Configuration Error: {e}")
        return
    
    print("\n" + "=" * 80)
    print("✅ Enhanced tool with mechanism diversity and JSON export")
    print("=" * 80)


if __name__ == "__main__":
    main()
