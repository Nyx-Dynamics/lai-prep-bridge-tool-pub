# LAI-PrEP Bridge Period Decision Support Tool v2.1
# LAI-PrEP Bridge Period Decision Support Tool

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17727117.svg)](https://zenodo.org/uploads/17727117#:~:text=10.5281/zenodo.17727117)
[![License: Pharma-Restricted](https://img.shields.io/badge/License-Pharma--Restricted-blue.svg)](LICENSE.md)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Status: Validated](https://img.shields.io/badge/status-computationally%20validated-green.svg)]((https://zenodo.org/uploads/17727117#:~:text=10.5281/zenodo.17727117))

> Clinical decision support for LAI-PrEP bridge period navigation validated at UNAIDS global target scale (21.2M patients)

## Free for Healthcare Providers | Free for Researchers | Pharma: Permission Required

---

## Quick Links

- **Zenodo Archive**: 
- **Manuscript**: *Viruses* 2025 (under review)
- **Documentation**: [See https://zenodo.org/uploads/17727117#:~:text=10.5281/zenodo.17727117
- **Licenses**: DATA under CC 4.0 International[LICENSE.md], CODE under MIT[LICENSE.md], [Pharma-Restricted Open Healthcare v1.0](PHARMA_RESTRICTED_LICENSE.md)
        
- **Contact**: acdemidont@nyxdynamics.org

---

## Citation

If you use this tool in your work, please cite:

**Software:**
```bibtex
@software{demidont2025laiprep,
  author = {Demidont, Adrian C.} 
  title = {LAI-PrEP Bridge Period Decision Support Tool},
  version = {2.1.0},
  year = {2025},
  publisher = {Zenodo},
  doi = {(https://zenodo.org/uploads/17727117#:~:text=10.5281/zenodo.17727117)},
  
}
```

**Manuscript:**
```bibtex
@article{demidont2025validation,
  author = {Demidont, Adrian C. and Backus, Kandis V.},
  title = {Computational Validation of Clinical Decision Support Algorithm 
           for Long-Acting Injectable PrEP Bridge Period Navigation at 
           UNAIDS Global Target Scale},
  journal = {Viruses},
  year = {2025},
  note = {Under review}
}
```

**Plain text:**

## What's New in v2.1

### Enhanced Features

**1. Mechanism Diversity Scoring**
- Prevents recommending redundant interventions
- Applies overlap penalties for similar mechanisms
- Ensures diverse, synergistic recommendations

**2. JSON Export & Explainability**
- Machine-readable output format
- Detailed attrition factor explanations
- Confidence intervals for estimates
- Rationale for each recommendation

**3. Logit-Space Calculations (Optional)**
- More mathematically sound probability transformations
- Better handling of extreme values
- Maintains proper probability bounds

**4. Command-Line Interface**
- Assess single patients from JSON
- Batch process multiple patients from CSV
- Validate configuration files
- Generate templates

**5. Comprehensive Unit Tests**
- Edge case coverage
- Boundary condition testing
- Error handling validation
- Method comparison tests

---

## Quick Start

### Installation

```bash
# No external dependencies beyond Python 3.7+ stdlib
# Optional: Install pytest for running tests
pip install pytest --break-system-packages

# Download the files
# Ensure these files are in the same directory:
# - lai_prep_decision_tool_v2_1.py
# - lai_prep_config.json
# - cli.py (for CLI usage)
# - test_edge_cases.py (for testing)
```

### Basic Usage

#### Python API

```python
from SCR.lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool, PatientProfile

# Initialize tool
tool = LAIPrEPDecisionTool(use_logit=False)  # or use_logit=True for logit-space

# Create patient profile
profile = PatientProfile(
    population="CISGENDER_WOMEN",
    age=28,
    current_prep_status="naive",
    barriers=["TRANSPORTATION", "CHILDCARE"],
    healthcare_setting="COMMUNITY_HEALTH_CENTER",
    insurance_status="insured",
    childcare_needs=True,
    transportation_access=False
)

# Assess patient
assessment = tool.assess_patient(profile)

# Generate human-readable report
print(tool.generate_report(profile, assessment))

# Export as JSON
json_output = assessment.to_json(profile)
```

#### Command Line Interface

```bash
# Assess single patient
python cli.py assess -i example_patient.json -o results.json --pretty

# Batch process multiple patients
python cli.py batch -i example_patients.csv -o results/ --summary --verbose

# Validate configuration
python cli.py validate -c lai_prep_config.json

# Generate template
python cli.py template -o my_patient.json
```

---

## New Features Detailed

### 1. Mechanism Diversity Scoring

**Problem:** Original tool could recommend multiple interventions working through the same mechanism, leading to redundancy.

**Solution:** Track mechanism categories and apply overlap penalties.

**Mechanism Categories:**
- `eliminate_bridge` - Remove bridge period entirely
- `compress_bridge` - Shorten bridge duration
- `navigate_bridge` - Guide through bridge period
- `remove_barriers` - Address specific obstacles
- `system_level` - Healthcare system changes

**Example:**

```python
# Recommendations automatically diversified
recommendations = assessment.recommended_interventions

for rec in recommendations:
    print(f"{rec.intervention_name}")
    print(f"  Mechanisms: {', '.join(rec.mechanisms)}")
    print(f"  Improvement: +{rec.expected_improvement:.1f}%")
```

Output:
```
Same-day switching protocol
  Mechanisms: eliminate_bridge, reduce_appointments
  Improvement: +40.0%

Patient navigation program
  Mechanisms: navigate_bridge, coordination, barrier_identification
  Improvement: +15.0%

Transportation support
  Mechanisms: remove_barriers
  Improvement: +8.0%
```

**Overlap Penalty:** If a recommended intervention shares mechanisms with already-selected interventions, its improvement estimate is reduced by 10% per overlapping mechanism.

### 2. JSON Export & Explainability

**Machine-Readable Output:**

```python
json_output = assessment.to_json(profile)

# Structure:
{
  "patient_profile": {...},
  "risk_assessment": {
    "level": "High attrition risk",
    "baseline_success": 0.45,
    "adjusted_success": 0.33,
    "attrition_factors": {
      "baseline_attrition": 0.55,
      "barrier_impacts": {
        "TRANSPORTATION": 0.10,
        "CHILDCARE": 0.08
      },
      "barrier_count_penalty": 0.08,
      "total_adjustment": 0.26
    }
  },
  "recommendations": [...],
  "predictions": {
    "without_interventions": 0.33,
    "with_interventions": 0.514,
    "absolute_improvement": 0.184,
    "relative_improvement_pct": 55.76
  },
  "bridge_period_estimate": {
    "minimum_days": 21,
    "maximum_days": 56,
    "delay_factors": [
      "HIV testing required (adds 3-7 days)",
      "Transportation barriers may delay appointments",
      "Childcare coordination needed"
    ]
  }
}
```

**Attrition Factor Explanations:**

The `attrition_factors` field breaks down exactly why the adjusted success rate differs from baseline:

- **Baseline**: Population-specific starting point
- **Barrier impacts**: Individual contribution of each barrier
- **Barrier count penalty**: Compounding effect of multiple barriers
- **Total adjustment**: Sum of all adjustments

**Confidence Intervals:**

Each recommendation includes a confidence interval (±20% of point estimate):

```python
rec.confidence_interval  # (lower, upper)
# Example: (12.0, 18.0) for 15% point estimate
```

### 3. Logit-Space Calculations

**Why Logit Space?**

Linear probability adjustments can produce invalid probabilities (<0 or >1). Logit space ensures mathematically sound transformations.

**Logit Function:**
```
logit(p) = log(p / (1-p))
```

**Inverse Logit:**
```
inv_logit(x) = 1 / (1 + exp(-x))
```

**Usage:**

```python
# Linear method (default)
tool_linear = LAIPrEPDecisionTool(use_logit=False)

# Logit method (more mathematically sound)
tool_logit = LAIPrEPDecisionTool(use_logit=True)

# Both produce similar rankings but logit handles extremes better
```

**When to Use Logit:**
- Patients with extreme barrier loads (>4 barriers)
- Very low/high baseline attrition populations
- When mathematical rigor is prioritized

**Comparison Example:**

| Method | 4 Barriers | 7 Barriers |
|--------|-----------|-----------|
| Linear | 0.25 | 0.05 (floor) |
| Logit  | 0.28 | 0.12 |

Logit maintains realistic probabilities even with extreme inputs.

### 4. Command-Line Interface

#### Assess Command

```bash
python cli.py assess --input patient.json --output results.json [options]

Options:
  -i, --input PATH      Input JSON file (required)
  -o, --output PATH     Output JSON file (required)
  -c, --config PATH     Configuration file
  --logit               Use logit-space calculations
  --pretty              Pretty-print JSON output
  -v, --verbose         Verbose output
```

**Example:**

```bash
python cli.py assess \
  -i example_patient.json \
  -o results.json \
  --pretty \
  --verbose

# Output:
Loading patient data from: example_patient.json
Patient: PWID age 35
Running assessment (method: linear)...
✓ Assessment complete
✓ Results saved to: results.json

============================================================
ASSESSMENT SUMMARY
============================================================
Risk Level: Very high attrition risk
Baseline Success: 25.0%
Adjusted Success: 15.2%
With Interventions: 35.8%
Improvement: +20.6% (136% relative)

Top 3 Recommendations:
  1. SSP/harm reduction integration
     Priority: Critical | Improvement: +15.0%
  2. Peer navigation support
     Priority: High | Improvement: +12.0%
  3. Mobile/community-based delivery
     Priority: High | Improvement: +12.0%
============================================================
```

#### Batch Command

```bash
python cli.py batch --input patients.csv --output-dir results/ [options]

Options:
  -i, --input PATH      Input CSV file (required)
  -o, --output-dir PATH Output directory (required)
  -c, --config PATH     Configuration file
  --logit               Use logit-space calculations
  --summary             Generate summary CSV
  -v, --verbose         Verbose output
```

**CSV Format:**

```csv
patient_id,population,age,current_prep_status,barriers,healthcare_setting,insurance_status
pt001,MSM,28,oral_prep,SCHEDULING_CONFLICTS,LGBTQ_CENTER,insured
pt002,PWID,35,naive,"HOUSING_INSTABILITY,TRANSPORTATION",HARM_REDUCTION,uninsured
```

**Example:**

```bash
python cli.py batch \
  -i example_patients.csv \
  -o batch_results/ \
  --summary \
  --verbose

# Generates:
# batch_results/patient_001_assessment.json
# batch_results/patient_002_assessment.json
# ...
# batch_results/batch_summary.csv
```

**Summary CSV Output:**

```csv
patient_id,population,age,prep_status,barrier_count,risk_level,baseline_success,adjusted_success,estimated_success,improvement,top_intervention
pt001,MSM,28,oral_prep,1,Moderate,0.55,0.50,0.85,0.35,Same-day switching
pt002,PWID,35,naive,2,Very High,0.25,0.15,0.36,0.21,Harm reduction integration
```

#### Validate Command

```bash
python cli.py validate --config lai_prep_config.json

# Output:
Validating configuration: lai_prep_config.json
✓ JSON syntax valid
✓ Version: 2.0.0
✓ Section 'populations': 7 entries
✓ Section 'barriers': 13 entries
✓ Section 'interventions': 13 entries
✓ Section 'healthcare_settings': 8 entries
✓ Section 'risk_categories': 4 entries
✓ Section 'algorithm_parameters': 1 entries

============================================================
✅ CONFIGURATION VALID
============================================================
```

#### Template Command

```bash
python cli.py template --output my_patient.json

# Generates template with comments
```

### 5. Unit Tests

**Running Tests:**

```bash
# Install pytest (if not installed)
pip install pytest --break-system-packages

# Run all tests
python test_edge_cases.py

# Or use pytest directly
pytest test_edge_cases.py -v
```

**Test Categories:**

1. **Edge Cases**
   - Maximum barriers (>4)
   - Conflicting signals
   - Adolescent privacy concerns
   - Zero barriers (best case)
   - Discontinued oral PrEP re-engagement
   - Extreme ages

2. **Logit vs Linear**
   - Valid probability generation
   - Consistency in rankings
   - Extreme value handling

3. **Mechanism Diversity**
   - Redundancy prevention
   - Mechanism tag presence
   - Overlap penalty application

4. **JSON Export**
   - Valid structure
   - Explanation presence
   - Serializability

5. **Error Handling**
   - Invalid population
   - Invalid barrier
   - Invalid healthcare setting

**Example Test Output:**

```
======================== test session starts ========================
test_edge_cases.py::TestEdgeCases::test_maximum_barriers PASSED
test_edge_cases.py::TestEdgeCases::test_conflicting_signals_oral_prep_no_test PASSED
test_edge_cases.py::TestEdgeCases::test_adolescent_privacy_concerns PASSED
...
======================== 20 passed in 2.34s ========================
```

---

## Configuration Updates

The configuration file (`lai_prep_config.json`) can be extended with mechanism tags:

```json
{
  "interventions": {
    "PATIENT_NAVIGATION": {
      "name": "Patient navigation program",
      "improvement": 0.15,
      "mechanisms": ["navigate_bridge", "coordination"],
      ...
    }
  }
}
```

---

## API Reference

### LAIPrEPDecisionTool

```python
tool = LAIPrEPDecisionTool(
    config_path: Optional[str] = None,  # Path to config file
    use_logit: bool = False              # Use logit-space calculations
)
```

**Methods:**

- `assess_patient(profile: PatientProfile) -> BridgePeriodAssessment`
- `generate_report(profile, assessment) -> str`

### PatientProfile

```python
profile = PatientProfile(
    population: str,                     # Required
    age: int,                            # Required
    current_prep_status: str,            # Required
    barriers: List[str] = [],
    healthcare_setting: str = "COMMUNITY_HEALTH_CENTER",
    insurance_status: str = "insured",
    recent_hiv_test: bool = False,
    transportation_access: bool = True,
    childcare_needs: bool = False
)
```

**Class Methods:**

- `PatientProfile.from_dict(data: Dict) -> PatientProfile`
- `profile.to_dict() -> Dict`

### BridgePeriodAssessment

**Attributes:**

- `baseline_success_rate: float`
- `adjusted_success_rate: float`
- `attrition_risk: str`
- `recommended_interventions: List[InterventionRecommendation]`
- `estimated_success_with_interventions: float`
- `attrition_factors: Dict` *(new in v2.1)*
- `delay_factors: List[str]` *(new in v2.1)*

**Methods:**

- `to_json(profile: PatientProfile, tool_version: str) -> Dict` *(new in v2.1)*

### InterventionRecommendation

**Attributes:**

- `intervention: str`
- `intervention_name: str`
- `priority: str`
- `expected_improvement: float`
- `evidence_level: str`
- `cost_level: str`
- `implementation_complexity: str`
- `mechanisms: List[str]` *(new in v2.1)*
- `confidence_interval: Tuple[float, float]` *(new in v2.1)*
- `rationale: str` *(new in v2.1)*

**Methods:**

- `to_dict() -> Dict` *(new in v2.1)*

### Utility Functions

```python
# For CLI/API use
assess_patient_json(
    patient_data: Dict,
    config_path: Optional[str] = None,
    use_logit: bool = False
) -> Dict
```

---

## Examples

### Example 1: Single Patient Assessment with JSON Export

```python
from SCR.lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool, PatientProfile
import json

# Initialize
tool = LAIPrEPDecisionTool()

# Patient profile
profile = PatientProfile(
    population="PWID",
    age=35,
    current_prep_status="naive",
    barriers=["HOUSING_INSTABILITY", "TRANSPORTATION", "SUBSTANCE_USE"],
    healthcare_setting="HARM_REDUCTION",
    insurance_status="uninsured"
)

# Assess
assessment = tool.assess_patient(profile)

# Human-readable report
print(tool.generate_report(profile, assessment))

# JSON export
json_output = assessment.to_json(profile)
with open('assessment.json', 'w') as f:
    json.dump(json_output, f, indent=2)

# Access specific fields
print(f"\nRisk Level: {assessment.attrition_risk}")
print(f"Success Rate: {assessment.adjusted_success_rate:.1%}")
print(f"With Interventions: {assessment.estimated_success_with_interventions:.1%}")

print("\nTop 3 Interventions:")
for i, rec in enumerate(assessment.recommended_interventions[:3], 1):
    print(f"{i}. {rec.intervention_name}")
    print(f"   Improvement: +{rec.expected_improvement:.1f}%")
    print(f"   Mechanisms: {', '.join(rec.mechanisms)}")
    print(f"   Rationale: {rec.rationale}")
```

### Example 2: Comparing Linear vs Logit Methods

```python
from SCR.lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool, PatientProfile

# Extreme case: many barriers
profile = PatientProfile(
    population="PWID",
    age=35,
    current_prep_status="naive",
    barriers=[
        "HOUSING_INSTABILITY", "TRANSPORTATION", "LEGAL_CONCERNS",
        "HEALTHCARE_DISCRIMINATION", "COMPETING_PRIORITIES",
        "LACK_IDENTIFICATION", "SUBSTANCE_USE"
    ],
    healthcare_setting="COMMUNITY_HEALTH_CENTER",
    insurance_status="uninsured"
)

# Compare methods
tool_linear = LAIPrEPDecisionTool(use_logit=False)
tool_logit = LAIPrEPDecisionTool(use_logit=True)

assessment_linear = tool_linear.assess_patient(profile)
assessment_logit = tool_logit.assess_patient(profile)

print("Comparison with 7 Barriers:")
print(f"Linear Method:  {assessment_linear.adjusted_success_rate:.3f}")
print(f"Logit Method:   {assessment_logit.adjusted_success_rate:.3f}")

# Logit typically produces slightly higher (more realistic) estimates
# for extreme cases
```

### Example 3: Batch Processing via Python API

```python
import csv
from SCR.lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool, PatientProfile

tool = LAIPrEPDecisionTool()

# Read patients from CSV
patients = []
with open('patients.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['barriers'] = row['barriers'].split(',') if row['barriers'] else []
        row['age'] = int(row['age'])
        patients.append(row)

# Process each patient
results = []
for patient_data in patients:
    profile = PatientProfile.from_dict(patient_data)
    assessment = tool.assess_patient(profile)

    results.append({
        'patient_id': patient_data.get('patient_id', 'unknown'),
        'risk_level': assessment.attrition_risk,
        'adjusted_success': assessment.adjusted_success_rate,
        'estimated_success': assessment.estimated_success_with_interventions,
        'top_intervention': assessment.recommended_interventions[0].intervention_name
    })

# Save summary
with open('results_summary.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
```

---

## Version History

### v2.1.0 (Current)
- Mechanism diversity scoring
- JSON export with explainability
- Logit-space calculations (optional)
- Command-line interface
- Comprehensive unit tests
- Confidence intervals
- Rationale for recommendations

### v2.0.0
- Configuration-driven architecture
- External JSON configuration
- Evidence level tagging
- Cost and complexity ratings
- Improved clinical guidance

### v1.0.0
- Initial release
- Hard-coded parameters
- Basic functionality

---

## Citation

If you use this tool in research or clinical practice, please cite:

```
Demidont, A.C (2025). Computational Validation of a Clinical 
Decision Support Algorithm for Long-Acting Injectable PrEP Bridge Period 
Navigation at UNAIDS Global Target Scale. Viruses, 17(1), XX.

Demidont, A.C (2025). Bridging the Gap: The PrEP Cascade 
Paradigm Shift for Long-Acting Injectable HIV Prevention. Viruses, 1(1), XX.
```

---

## Contact

**Primary Author**: A.C Demidont, DO  
**Email**: acdemidont@nyxdynamics.org  
**Organization**: Nyx Dynamics, LLC



---

## License

Open source under MIT License.

---

**Tool Version**: 2.1.0  
**Last Updated**: November 29, 2025  
**Configuration Version**: 2.1.0
