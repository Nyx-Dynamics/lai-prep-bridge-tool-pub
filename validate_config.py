#!/usr/bin/env python3
"""
Configuration Validation Script for LAI-PrEP Bridge Decision Support Tool

This script validates the configuration JSON file to ensure:
1. Valid JSON syntax
2. Required sections present
3. Valid parameter ranges
4. Consistent cross-references
5. Evidence documentation complete
"""

import json
import sys


class ConfigValidator:
    """Validates LAI-PrEP configuration files"""
    
    REQUIRED_SECTIONS = [
        'version', 'populations', 'barriers', 'interventions',
        'healthcare_settings', 'risk_categories', 'algorithm_parameters'
    ]
    
    REQUIRED_POPULATION_FIELDS = [
        'name', 'baseline_attrition', 'evidence_level', 'evidence_source'
    ]
    
    REQUIRED_BARRIER_FIELDS = [
        'name', 'impact', 'evidence_level'
    ]
    
    REQUIRED_INTERVENTION_FIELDS = [
        'name', 'improvement', 'evidence_level', 'cost_level',
        'implementation_complexity'
    ]
    
    VALID_EVIDENCE_LEVELS = ['strong', 'moderate', 'emerging']
    VALID_COST_LEVELS = ['low', 'medium', 'high']
    VALID_COMPLEXITY_LEVELS = ['low', 'medium', 'high']
    
    def __init__(self, config_path: str):
        """Initialize validator with configuration file path"""
        self.config_path = config_path
        self.config = None
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate(self) -> bool:
        """
        Validate configuration file
        
        Returns:
            bool: True if valid, False if errors found
        """
        print(f"Validating configuration: {self.config_path}")
        print("=" * 80)
        
        # Load and parse JSON
        if not self._load_json():
            return False
        
        # Validate structure
        self._validate_required_sections()
        self._validate_populations()
        self._validate_barriers()
        self._validate_interventions()
        self._validate_healthcare_settings()
        self._validate_risk_categories()
        self._validate_algorithm_parameters()
        
        # Validate cross-references
        self._validate_cross_references()
        
        # Validate ranges
        self._validate_ranges()
        
        # Report results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _load_json(self) -> bool:
        """Load and parse JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            self.info.append(f"✓ JSON syntax valid")
            return True
        except FileNotFoundError:
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading configuration: {e}")
            return False
    
    def _validate_required_sections(self):
        """Validate that all required sections are present"""
        for section in self.REQUIRED_SECTIONS:
            if section not in self.config:
                self.errors.append(f"Missing required section: '{section}'")
            else:
                self.info.append(f"✓ Section '{section}' present")
    
    def _validate_populations(self):
        """Validate populations section"""
        if 'populations' not in self.config:
            return
        
        pops = self.config['populations']
        self.info.append(f"✓ Found {len(pops)} populations")
        
        for pop_key, pop_data in pops.items():
            # Check required fields
            for field in self.REQUIRED_POPULATION_FIELDS:
                if field not in pop_data:
                    self.errors.append(
                        f"Population '{pop_key}' missing required field: '{field}'"
                    )
            
            # Validate attrition range
            if 'baseline_attrition' in pop_data:
                attrition = pop_data['baseline_attrition']
                if not (0 <= attrition <= 1):
                    self.errors.append(
                        f"Population '{pop_key}' baseline_attrition must be 0-1, "
                        f"got {attrition}"
                    )
            
            # Validate evidence level
            if 'evidence_level' in pop_data:
                if pop_data['evidence_level'] not in self.VALID_EVIDENCE_LEVELS:
                    self.warnings.append(
                        f"Population '{pop_key}' has non-standard evidence_level: "
                        f"'{pop_data['evidence_level']}'"
                    )
            
            # Check attrition range
            if 'attrition_range' in pop_data:
                if len(pop_data['attrition_range']) != 2:
                    self.errors.append(
                        f"Population '{pop_key}' attrition_range must have 2 values"
                    )
                else:
                    min_atr, max_atr = pop_data['attrition_range']
                    if min_atr > max_atr:
                        self.errors.append(
                            f"Population '{pop_key}' attrition_range min > max"
                        )
    
    def _validate_barriers(self):
        """Validate barriers section"""
        if 'barriers' not in self.config:
            return
        
        barriers = self.config['barriers']
        self.info.append(f"✓ Found {len(barriers)} barriers")
        
        for barrier_key, barrier_data in barriers.items():
            # Check required fields
            for field in self.REQUIRED_BARRIER_FIELDS:
                if field not in barrier_data:
                    self.errors.append(
                        f"Barrier '{barrier_key}' missing required field: '{field}'"
                    )
            
            # Validate impact range
            if 'impact' in barrier_data:
                impact = barrier_data['impact']
                if not (0 <= impact <= 0.5):
                    self.warnings.append(
                        f"Barrier '{barrier_key}' impact unusually high: {impact} "
                        f"(typical: 0.05-0.15)"
                    )
            
            # Validate evidence level
            if 'evidence_level' in barrier_data:
                if barrier_data['evidence_level'] not in self.VALID_EVIDENCE_LEVELS:
                    self.warnings.append(
                        f"Barrier '{barrier_key}' has non-standard evidence_level"
                    )
    
    def _validate_interventions(self):
        """Validate interventions section"""
        if 'interventions' not in self.config:
            return
        
        interventions = self.config['interventions']
        self.info.append(f"✓ Found {len(interventions)} interventions")
        
        for int_key, int_data in interventions.items():
            # Check required fields
            for field in self.REQUIRED_INTERVENTION_FIELDS:
                if field not in int_data:
                    self.errors.append(
                        f"Intervention '{int_key}' missing required field: '{field}'"
                    )
            
            # Validate improvement range
            if 'improvement' in int_data:
                improvement = int_data['improvement']
                if not (0 <= improvement <= 0.5):
                    self.warnings.append(
                        f"Intervention '{int_key}' improvement unusually high: "
                        f"{improvement} (typical: 0.05-0.20)"
                    )
            
            # Validate evidence level
            if 'evidence_level' in int_data:
                if int_data['evidence_level'] not in self.VALID_EVIDENCE_LEVELS:
                    self.warnings.append(
                        f"Intervention '{int_key}' has non-standard evidence_level"
                    )
            
            # Validate cost level
            if 'cost_level' in int_data:
                if int_data['cost_level'] not in self.VALID_COST_LEVELS:
                    self.warnings.append(
                        f"Intervention '{int_key}' has non-standard cost_level"
                    )
            
            # Validate complexity level
            if 'implementation_complexity' in int_data:
                if int_data['implementation_complexity'] not in self.VALID_COMPLEXITY_LEVELS:
                    self.warnings.append(
                        f"Intervention '{int_key}' has non-standard complexity"
                    )
    
    def _validate_healthcare_settings(self):
        """Validate healthcare_settings section"""
        if 'healthcare_settings' not in self.config:
            return
        
        settings = self.config['healthcare_settings']
        self.info.append(f"✓ Found {len(settings)} healthcare settings")
        
        for setting_key, setting_data in settings.items():
            # Check name field
            if 'name' not in setting_data:
                self.errors.append(
                    f"Healthcare setting '{setting_key}' missing 'name' field"
                )
    
    def _validate_risk_categories(self):
        """Validate risk_categories section"""
        if 'risk_categories' not in self.config:
            return
        
        categories = self.config['risk_categories']
        self.info.append(f"✓ Found {len(categories)} risk categories")
        
        # Check that thresholds don't overlap
        thresholds = []
        for cat_key, cat_data in categories.items():
            if 'threshold_min' in cat_data and 'threshold_max' in cat_data:
                thresholds.append((
                    cat_key,
                    cat_data['threshold_min'],
                    cat_data['threshold_max']
                ))
        
        # Sort by min threshold
        thresholds.sort(key=lambda x: x[1])
        
        # Check for gaps or overlaps
        for i in range(len(thresholds) - 1):
            current = thresholds[i]
            next_cat = thresholds[i + 1]
            
            if current[2] != next_cat[1]:
                self.warnings.append(
                    f"Risk category threshold gap/overlap between '{current[0]}' "
                    f"and '{next_cat[0]}'"
                )
    
    def _validate_algorithm_parameters(self):
        """Validate algorithm_parameters section"""
        if 'algorithm_parameters' not in self.config:
            return
        
        params = self.config['algorithm_parameters']
        self.info.append(f"✓ Algorithm parameters present")
        
        # Check ceiling
        if 'max_attrition_ceiling' in params:
            ceiling = params['max_attrition_ceiling']
            if ceiling != 0.95:
                self.warnings.append(
                    f"max_attrition_ceiling is {ceiling}, standard is 0.95"
                )
        
        # Check diminishing returns factor
        if 'intervention_diminishing_returns_factor' in params:
            factor = params['intervention_diminishing_returns_factor']
            if not (0.5 <= factor <= 1.0):
                self.warnings.append(
                    f"intervention_diminishing_returns_factor is {factor}, "
                    f"typical range: 0.5-1.0"
                )
    
    def _validate_cross_references(self):
        """Validate cross-references between sections"""
        if not all(k in self.config for k in ['populations', 'barriers', 'interventions']):
            return
        
        # Check population references in barrier affected_populations
        pop_keys = set(self.config['populations'].keys())
        
        for barrier_key, barrier_data in self.config['barriers'].items():
            if 'affected_populations' in barrier_data:
                for pop in barrier_data['affected_populations']:
                    if pop not in pop_keys:
                        self.errors.append(
                            f"Barrier '{barrier_key}' references unknown population: '{pop}'"
                        )
        
        # Check population references in intervention applicable_populations
        for int_key, int_data in self.config['interventions'].items():
            if 'applicable_populations' in int_data:
                for pop in int_data['applicable_populations']:
                    if pop not in pop_keys:
                        self.errors.append(
                            f"Intervention '{int_key}' references unknown population: '{pop}'"
                        )
        
        # Check barrier references in intervention addresses_barriers
        barrier_keys = set(self.config['barriers'].keys())
        
        for int_key, int_data in self.config['interventions'].items():
            if 'addresses_barriers' in int_data:
                for barrier in int_data['addresses_barriers']:
                    if barrier not in barrier_keys:
                        self.errors.append(
                            f"Intervention '{int_key}' references unknown barrier: '{barrier}'"
                        )
    
    def _validate_ranges(self):
        """Validate that parameter values are within reasonable ranges"""
        if 'populations' not in self.config:
            return
        
        # Check that sum of baseline attritions is reasonable
        attritions = [
            pop['baseline_attrition'] 
            for pop in self.config['populations'].values()
            if 'baseline_attrition' in pop
        ]
        
        if attritions:
            avg_attrition = sum(attritions) / len(attritions)
            if not (0.3 <= avg_attrition <= 0.7):
                self.warnings.append(
                    f"Average population attrition is {avg_attrition:.2f}, "
                    f"expected range: 0.30-0.70"
                )
    
    def _print_results(self):
        """Print validation results"""
        print()
        
        # Print info messages
        if self.info:
            print("INFO:")
            print("-" * 80)
            for msg in self.info:
                print(f"  {msg}")
            print()
        
        # Print warnings
        if self.warnings:
            print("WARNINGS:")
            print("-" * 80)
            for msg in self.warnings:
                print(f"  ⚠️  {msg}")
            print()
        
        # Print errors
        if self.errors:
            print("ERRORS:")
            print("-" * 80)
            for msg in self.errors:
                print(f"  ❌ {msg}")
            print()
        
        # Print summary
        print("=" * 80)
        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} error(s), "
                  f"{len(self.warnings)} warning(s)")
        elif self.warnings:
            print(f"⚠️  VALIDATION PASSED WITH WARNINGS: {len(self.warnings)} warning(s)")
        else:
            print(f"✅ VALIDATION PASSED: No errors or warnings")
        print("=" * 80)


def main():
    """Main validation function"""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python validate_config.py <config_file.json>")
        print()
        print("Example:")
        print("  python validate_config.py lai_prep_config.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    # Validate
    validator = ConfigValidator(config_path)
    is_valid = validator.validate()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
