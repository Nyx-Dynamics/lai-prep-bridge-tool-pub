# LAI-PrEP Bridge Period Decision Support Tool

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17429833.svg)](https://doi.org/10.5281/zenodo.17429833)
[![License: Pharma-Restricted](https://img.shields.io/badge/License-Pharma--Restricted%20Open%20Healthcare-blue.svg)](LICENSE.md)
[![Python 3.9.6](https://img.shields.io/badge/python-3.9.6-blue.svg)](https://www.python.org/downloads/)
[![Validation: 21.2M patients](https://img.shields.io/badge/Validation-21.2M%20patients-green.svg)](#validation)
[![Tests: 18/18 passing](https://img.shields.io/badge/Tests-18%2F18%20passing-brightgreen.svg)](#testing)

**Clinical decision support tool for navigating the LAI-PrEP bridge period—the critical gap between prescription and first injection where 47% of patients are lost to follow-up.**

---

## The LAI-PrEP Bridge Period Paradox

Long-acting injectable PrEP (LAI-PrEP) offers **superior efficacy** compared to daily oral PrEP:
- **89% relative risk reduction** vs. oral PrEP in clinical trials (HPTN 083, HPTN 084)
- **Zero adherence burden** after injection
- **Preferred by patients** who struggle with daily pills

Yet **47% of patients prescribed LAI-PrEP never receive their first injection** (CAN Community Health Network, 2024).

This "bridge period paradox" means the most effective HIV prevention tool fails nearly half the time—not due to the medication, but due to **structural barriers** in healthcare delivery.

---

## The Evidence-Based Decision Support Tool

This tool synthesizes evidence from **15,000+ clinical trial participants** and **real-world implementation studies** to:

1. **Predict** individual patient bridge period success probability
2. **Identify** the specific barriers putting each patient at risk
3. **Recommend** evidence-based interventions prioritized by expected impact
4. **Quantify** expected improvement with recommended interventions

### Key Features

- **7 population categories** with evidence-based baseline rates
- **13 structural barriers** with quantified attrition impacts
- **21 evidence-based interventions** with expected improvements
- **Mechanism diversity scoring** to prevent redundant recommendations
- **Confidence intervals** for all estimates
- **JSON export** for EHR integration
- **Configuration-driven architecture** for easy evidence updates

---

## Validation

### Progressive Scale Testing
| Scale | Patients | Result | Use Case |
|-------|----------|--------|----------|
| 1,000 | 1K | ✅ Converged | Development |
| 1,000,000 | 1M | ✅ Converged | Regional planning |
| 10,000,000 | 10M | ✅ Converged | National scale |
| **21,200,000** | **21.2M** | ✅ Converged | **UNAIDS global target** |

### Unit Testing
- **18 edge case tests**: 100% pass rate
- **Mathematical validation**: Both logit and linear methods
- **Clinical scenarios**: Maximum barriers, extreme ages, all populations

### External Validation
Predictions align with published data:
- HPTN 083/084 trial outcomes
- CAN Community Health Network (47.1% attrition)
- San Francisco PrEP Navigation studies

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub.git
cd lai-prep-bridge-tool-pub

# No additional dependencies required (uses Python standard library + numpy)
pip install numpy
```

### Basic Usage

```python
from lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool, PatientProfile

# Initialize tool
tool = LAIPrEPDecisionTool(config_path="lai_prep_bridge_tool_v2_1_0.json")

# Create patient profile
patient = PatientProfile(
    population="MSM",
    age=28,
    current_prep_status="naive",
    barriers=["TRANSPORTATION", "INSURANCE_DELAYS"],
    healthcare_setting="COMMUNITY_HEALTH_CENTER",
    insurance_status="insured"
)

# Get assessment
assessment = tool.assess_patient(patient)

# Generate clinical report
print(tool.generate_report(patient, assessment))
```

### Command Line Interface

```bash
# Assess a patient from JSON file
python cli.py --patient example_patient.json --config lai_prep_bridge_tool_v2_1_0.json

# Output as JSON (for EHR integration)
python cli.py --patient example_patient.json --output json
```

---

## Repository Structure

```
lai-prep-bridge-tool-pub/
├── lai_prep_decision_tool_v2_1.py    # Main decision support tool
├── lai_prep_bridge_tool_v2_1_0.json  # Configuration file
├── cli.py                             # Command line interface
├── example_patient.json               # Example patient profile
│
├── Clinical Implementation Guides/    # Guides for specific populations
│   ├── PWID_Implementation_Guide.md
│   └── Adolescent_Implementation_Guide.md
│
├── Project Docs/                      # Project documentation
│   ├── VALIDATION_RESULTS.md
│   └── EVIDENCE_TIERS.md
│
├── Validation_progressive/            # Validation at multiple scales
│   ├── validation_1M_results.json
│   ├── validation_10M_results.json
│   └── validation_UNAIDS_21_2M_results.json
│
├── manuscripts/                       # Published/submitted manuscripts
│   └── viruses4063895final_proof.pdf
│
├── config/                            # Configuration files
│   └── global_params.json
│
├── zenodo_database/                   # Zenodo archive data
│
├── LICENSE.md                         # Pharma-Restricted Open Healthcare License
├── CITATION.cff                       # Citation file
└── .zenodo.json                       # Zenodo metadata
```

---

## Population-Specific Outcomes

| Population | Baseline Success | With Interventions | Improvement |
|------------|------------------|--------------------| ------------|
| MSM | 55.0% | 78.3% | +23.3 pp |
| Cisgender Women | 45.0% | 69.1% | +24.1 pp |
| Transgender Women | 50.0% | 73.7% | +23.7 pp |
| Adolescents | 35.0% | 58.4% | +23.4 pp |
| **PWID** | **25.0%** | **51.6%** | **+26.6 pp** |
| Pregnant/Lactating | 45.0% | 68.9% | +23.9 pp |
| General | 53.0% | 76.2% | +23.2 pp |

**Key finding**: Populations with lowest baseline success show **greatest relative improvement** with evidence-based interventions.

---

## Configuration

The tool uses an external JSON configuration file that can be updated as new evidence becomes available:

```json
{
  "version": "2.1.0",
  "populations": {
    "MSM": {
      "name": "Men who have sex with men",
      "baseline_success_rate": 0.55,
      "evidence_level": "Strong",
      "evidence_source": "HPTN 083"
    }
  },
  "interventions": {
    "PATIENT_NAVIGATION": {
      "name": "Patient navigation program",
      "improvement": 0.15,
      "evidence_level": "Strong",
      "mechanisms": ["COORDINATION", "BARRIER_REMOVAL"]
    }
  }
}
```

---

## Testing

Run the test suite:

```bash
python -m pytest test_edge_cases.py -v
```

Or run directly:

```bash
python test_edge_cases.py
```

Expected output:
```
==================== test session starts ====================
collected 18 items

test_edge_cases.py::test_pwid_maximum_barriers PASSED
test_edge_cases.py::test_adolescent_young PASSED
test_edge_cases.py::test_pregnant_comprehensive PASSED
... (18 tests total)

==================== 18 passed in 2.34s ====================
```

---

## Publications

### Computational Validation Manuscript
> Demidont, A.C. Computational Validation of Clinical Decision Support Algorithm for Long-Acting Injectable PrEP Bridge Period Navigation at UNAIDS Global Target Scale. *Viruses* in press.

### Clinical Implementation Manuscript  
>  Demidont,  A. Bridging the Gap: The Prep Cascade Paradign Shift for Long-Acting Injectable HIV Prevention. Preprints 2025, 2025122354. https://doi.org/10.20944/preprints202512.2354.v1
---

## License

**Pharma-Restricted Open Healthcare License v1.0**

| User Type | Access | Requirements |
|-----------|--------|--------------|
| Healthcare Providers | | Attribution only |
| Researchers |  | Attribution only |
| Non-Profits |  | Attribution only |
| Government |  Attribution only |
| Pharma/Biotech |  Written permission required |

See [LICENSE.md](LICENSE.md) for full details.

---

## Citation

### Software
```bibtex
@software{demidont2025laiprep,
  author = {Demidont, Adrian C.},
  title = {LAI-PrEP Bridge Period Decision Support Tool},
  version = {2.1.0},
  year = {2025},
  url = {https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub},
  doi = {10.5281/zenodo.17429833}
}
```

### Manuscript
```bibtex
@article{demidont2025validation,
  author = {Demidont, Adrian C.},
  title = {Computational Validation of Clinical Decision Support Algorithm for Long-Acting Injectable PrEP Bridge Period Navigation at UNAIDS Global Target Scale, 21.2 M Individuals},
  journal = {Viruses},
  year = {2025}
}
```

---

## Contributing

We welcome contributions! Please see our contributing guidelines.

**Priority areas:**
- Real-world validation data
- Additional population-specific evidence
- EHR integration examples
- Translations of clinical guides

---

## Contact

**Adrian C. Demidont, DO**  
Founder & CEO, Nyx Dynamics LLC  
Email: acdemidont@nyxdynamics.org

**Repository Issues**: [GitHub Issues](https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub/issues)

---

## Clinical Disclaimer

This tool is intended to **ASSIST** healthcare providers in clinical decision-making. It does not replace clinical judgment. All treatment decisions remain the responsibility of the treating healthcare provider.

This tool has been **computationally validated** and requires **prospective clinical validation** before widespread deployment.

---

## Acknowledgments

- HPTN 083/084 study teams
- CAN Community Health Network
- PURPOSE trial investigators
- All patients and communities contributing to HIV prevention research

---
