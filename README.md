# LAI-PrEP Bridge Period Decision Support Tool

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17873201.svg)](https://doi.org/10.5281/zenodo.17873201) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![License: CC-BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/) [![GitHub](https://img.shields.io/badge/GitHub-Nyx--Dynamics-blue)](https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub)

**Computational validation of a clinical decision support algorithm for long-acting injectable pre-exposure prophylaxis (LAI-PrEP) bridge period navigation at UNAIDS global target scale (21.2 million patients)**

---

## 📋 Overview

This repository contains the complete source code, configuration files, test suites, and validation datasets for a clinical decision support tool designed to address the LAI-PrEP bridge period paradox: 47% of patients prescribed LAI-PrEP fail to receive their first injection despite superior clinical efficacy (>96%) compared to daily oral PrEP.

### The Bridge Period Challenge

Long-acting injectable antiretroviral agents represent a paradigm shift in HIV prevention, but implementation reveals a critical structural barrier: the "bridge period" between prescription and first injection. During this 2-8 week window, patients must navigate:
- HIV testing requirements (mandatory 7-day window)
- Insurance authorization delays
- Clinical appointment scheduling
- Multiple access barriers

Current implementation data show only 52.9% bridge period success, with significant disparities across populations:
- **MSM:** 30-40% success
- **Cisgender women:** 25-30% success  
- **Adolescents:** 15-25% success
- **People who inject drugs (PWID):** 10-20% success

This tool synthesizes evidence from >15,000 clinical trial participants to predict bridge period outcomes and recommend evidence-based interventions.

---

## 🔬 Key Findings

### Computational Validation Results

| Scale | Patients | Test Pass Rate | Key Metric |
|-------|----------|----------------|------------|
| Development | 1,000 | 100% | Initial validation |
| Intermediate | 1,000,000 | 100% | Scale stability |
| Large-scale | 10,000,000 | 100% | Population convergence |
| **UNAIDS Target** | **21,200,000** | **100%** | **Policy-grade precision** |

### Population Disparities Confirmed
- Baseline success rates range from 15% (PWID) to 40% (MSM)
- Evidence-based interventions improve outcomes by 83-265% depending on population
- Greatest improvement potential in historically underserved populations

### Edge Case Testing
- **18/18 edge cases passed** (100%)
- Covers maximum barriers, extreme ages, all populations
- Mathematical validation of logit and linear combination methods
- Mechanism diversity prevents redundant interventions

---

## 📁 Repository Structure

```
lai-prep-bridge-tool-pub/
├── src/
│   ├── lai_prep_decision_tool_v2_1.py    # Core algorithm
│   ├── lai_prep_config.json              # Evidence-based parameters
│   └── validate_config.py                # Configuration validator
├── tests/
│   ├── test_edge_cases.py                # Comprehensive edge case suite
│   └── run_tests.py                      # Test runner
├── validation/
│   ├── validation_1M_results.json        # 1M patient results
│   ├── validation_10M_results.json       # 10M patient results
│   └── validation_UNAIDS_21_2M_results.json  # UNAIDS scale results
├── docs/
│   └── VALIDATION_METHODOLOGY.md         # Methods documentation
├── LICENSE.md                            # MIT License (code)
├── LICENSE_DATA_CC_BY_4_0.md            # CC-BY 4.0 (data/docs)
├── CITATION.cff                          # Citation metadata
└── README.md                             # This file
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub.git
cd lai-prep-bridge-tool-pub

# Install dependencies
pip install numpy

# Run validation
python tests/run_tests.py
```

### Basic Usage

```python
from src.lai_prep_decision_tool_v2_1 import LAIPrEPBridgeTool

# Initialize tool
tool = LAIPrEPBridgeTool()

# Create patient profile
patient = {
    "population": "msm",
    "age": 28,
    "barriers": ["insurance_delay", "transportation"],
    "healthcare_setting": "community_health_center"
}

# Get recommendation
result = tool.assess_patient(patient)

print(f"Baseline success probability: {result['baseline_probability']:.1%}")
print(f"Predicted success with interventions: {result['predicted_probability']:.1%}")
print(f"Recommended interventions: {result['interventions']}")
```

---

## 📊 Validation Methodology

### Progressive Scale Testing
1. **Development (n=1,000):** Algorithm debugging and refinement
2. **Intermediate (n=1M):** Population distribution stability
3. **Large-scale (n=10M):** Convergence verification
4. **UNAIDS (n=21.2M):** Policy-grade validation at global target scale

### Edge Case Categories
- Maximum barrier combinations (7+ simultaneous barriers)
- Extreme ages (16-year-old adolescent, 65-year-old adult)
- All population categories with population-specific barriers
- Mathematical method validation (logit vs linear)
- Mechanism diversity (no redundant intervention recommendations)

### Precision Metrics
- Population proportion variance: ±0.018 percentage points
- Mean baseline probability: 0.244 (95% CI: 0.243-0.245)
- Convergence achieved at 10M patients

---

## 📚 Configuration System

The tool uses an external JSON configuration (`lai_prep_config.json`) enabling:
- **Rapid evidence updates** as new data emerges
- **Local adaptation** to different healthcare contexts
- **Transparency** for clinical audit and review
- **Version control** for parameter changes

### Configuration Categories
- **7 populations** with baseline success rates
- **13 structural barriers** with quantified impacts
- **21 evidence-based interventions** with effect sizes
- **8 healthcare settings** with setting-specific recommendations

---

## 📖 Citation

If you use this tool in your work, please cite:

**Software:**
```bibtex
@software{demidont2025laiprep,
  author = {Demidont, Adrian C.},
  title = {LAI-PrEP Bridge Period Decision Support Tool: Computational 
           validation at UNAIDS global target scale},
  version = {4.1.0},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17873201},
  url = {https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub}
}
```

**Plain text:**
```
Demidont, A.C. (2025). LAI-PrEP Bridge Period Decision Support Tool: 
Computational validation at UNAIDS global target scale (v4.1.0). 
Zenodo. https://doi.org/10.5281/zenodo.17873201
```

---

## 📄 License

- **Source code:** MIT License ([LICENSE.md](LICENSE.md))
- **Data and documentation:** CC-BY 4.0 ([LICENSE_DATA_CC_BY_4_0.md](LICENSE_DATA_CC_BY_4_0.md))

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional population-specific barrier data
- Healthcare setting adaptations
- Language translations
- Integration with EHR systems

---

## ⚠️ Clinical Disclaimer

This tool is intended to support, not replace, clinical judgment. All treatment decisions should be made in consultation with qualified healthcare providers. The algorithm has been computationally validated but requires prospective clinical validation before deployment in clinical care settings.

---

## 📞 Contact

**Author:** Adrian C. Demidont, DO  
**Organization:** Nyx Dynamics LLC  
**Email:** acdemidont@nyxdynamics.org  
**ORCID:** [0000-0002-9216-8569](https://orcid.org/0000-0002-9216-8569)

---

## 🙏 Acknowledgments

This work builds on evidence from major clinical trials including HPTN 083, HPTN 084, PURPOSE-1, and PURPOSE-2, representing contributions from >15,000 clinical trial participants worldwide. Special thanks to the implementation scientists and community partners working to translate prevention research into equitable, effective HIV prevention services.

---

**Version:** 4.1.0 | **Last Updated:** December 2025 | **Status:** Computationally validated, pending prospective clinical validation
