# LAI-PrEP Bridge Period Decision Support Tool

## Zenodo Archive Package

**Version:** 2.1.0  
**DOI:** [To be assigned upon upload]  
**Date:** November 26, 2025  
**License:** Pharma-Restricted Open Healthcare License v1.0

---

## Overview

This archive contains the complete LAI-PrEP Bridge Period Decision Support Tool, 
a computational tool designed to help clinicians and healthcare systems navigate 
the critical "bridge period" between LAI-PrEP prescription and first injection.

### Key Features

- **Patient Risk Stratification:** Assesses individual patient risk based on 
  population, barriers, and healthcare setting
- **Evidence-Based Interventions:** Recommends from 21 validated interventions
- **Outcome Prediction:** Estimates success probability with and without interventions
- **Mechanism Diversity:** Prevents redundant recommendations using diversity scoring
- **Progressive Validation:** Tested at scales from 1,000 to 21.2 million patients

### Clinical Impact Potential

- 47% of patients currently fail to receive first LAI-PrEP injection
- Systematic interventions could improve success from 24% to 44%
- Potential to prevent ~100,000 HIV infections annually
- Estimated $40 billion in lifetime treatment costs saved (11:1 ROI)

---

## Package Contents

### Core Algorithm
**Directory:** `code/algorithm/`  
**Files:** 2  
**Size:** 59.7 KB

Main decision support algorithm implementation

### Command Line Interface
**Directory:** `code/cli/`  
**Files:** 1  
**Size:** 15.0 KB

CLI for tool interaction and batch processing

### Test Suites
**Directory:** `code/tests/`  
**Files:** 5  
**Size:** 113.1 KB

Comprehensive testing for validation

### Configuration
**Directory:** `config/`  
**Files:** 4  
**Size:** 45.5 KB

External JSON configuration for parameters

### Figures
**Directory:** `figures/`  
**Files:** 10  
**Size:** 949.2 KB

Publication figures and visualizations

### Supplementary LaTeX
**Directory:** `supplementary/latex/`  
**Files:** 9  
**Size:** 180.9 KB

Supplementary material LaTeX source files

### Documentation Markdown
**Directory:** `documentation/`  
**Files:** 14  
**Size:** 196.6 KB

Project documentation and guides

### Manuscript PDFs
**Directory:** `manuscripts/`  
**Files:** 5  
**Size:** 19.8 MB

Main manuscript and supplementary PDFs

### Word Documents
**Directory:** `supplementary/docx/`  
**Files:** 2  
**Size:** 32.8 KB

Supplementary Word documents

### HTML Visualizations
**Directory:** `visualizations/`  
**Files:** 1  
**Size:** 24.3 KB

Interactive HTML visualizations

---

## Directory Structure

```
lai_bridge_tool_zenodo_package/
├── code/
│   ├── algorithm/          # Core decision support algorithm
│   ├── cli/                # Command-line interface
│   └── tests/              # Comprehensive test suites
├── config/                 # External JSON configuration
├── validation/             # Validation results (1M-21.2M scale)
├── figures/                # Publication figures
├── documentation/          # Markdown documentation
├── manuscripts/            # PDF manuscripts
├── supplementary/
│   ├── latex/              # LaTeX source files
│   └── docx/               # Word documents
├── visualizations/         # Interactive HTML visualizations
├── README.md               # This file
├── MANIFEST.json           # File checksums and metadata
└── CHECKSUMS.sha256        # SHA-256 checksums
```

---

## Quick Start

### Requirements

- Python 3.8+
- No external dependencies for core algorithm
- Optional: NumPy for enhanced performance

### Basic Usage

```python
from code.algorithm.lai_prep_decision_tool import LAIPrEPDecisionTool, PatientProfile, Population, Barrier

# Initialize tool
tool = LAIPrEPDecisionTool()

# Create patient profile
patient = PatientProfile(
    population=Population.MSM,
    age=28,
    current_prep_status="oral_prep",
    barriers=[Barrier.SCHEDULING_CONFLICTS],
    recent_hiv_test=True
)

# Get assessment
assessment = tool.assess_patient(patient)

# View report
print(tool.generate_report(patient, assessment))
```

### Command Line Interface

```bash
# Single patient assessment
python code/cli/cli.py assess -i patient.json -o results.json

# Batch processing
python code/cli/cli.py batch -i patients.csv -o results.csv

# Run validation
python code/cli/cli.py validate -n 1000000 -o validation.json
```

### Running Tests

```bash
# Run all tests
python -m pytest code/tests/ -v

# Run specific test suite
python -m pytest code/tests/test_edge_cases.py -v
```

---

## Validation Summary

### Progressive Scale Testing

| Scale | Patients | Mean Success | Margin of Error |
|-------|----------|--------------|-----------------|
| Tier 1 | 1,000 | 27.7% | ±2.8% |
| Tier 2 | 1,000,000 | 27.7% | ±0.09% |
| Tier 3 | 10,000,000 | 24.0% | ±0.03% |
| Tier 4 | 21,200,000 | 24.0% | ±0.018% |

### Unit Test Results

- **Test Pass Rate:** 100% (18/18 edge cases)
- **Categories Tested:**
  - Clinical edge cases (9 tests)
  - Mathematical validation (2 tests)
  - Mechanism diversity (2 tests)
  - JSON export (2 tests)
  - Error handling (3 tests)

---

## Evidence Base

### Clinical Trials

- **HPTN 083** (n=4,566): CAB-LA in MSM/TGW, 89% relative risk reduction
- **HPTN 084** (n=3,224): CAB-LA in cisgender women, 89% superior efficacy
- **PURPOSE-1** (n=5,338): Lenacapavir in cisgender women, zero infections
- **PURPOSE-2** (n=2,183): Lenacapavir across gender identities, 96% reduction

### Implementation Studies

- CAN Community Health Network Study (2021-2023): 47% bridge period attrition
- Patient navigation literature: 10-40% improvement in care completion

---

## Citation

### Software Citation

```bibtex
@software{{demidont2025laiprep,
  author = {{Demidont, Adrian C. and Backus, Kandis V.}},
  title = {{LAI-PrEP Bridge Period Decision Support Tool}},
  version = {{2.1.0}},
  year = {{2025}},
  publisher = {{Zenodo}},
  doi = {{10.5281/zenodo.XXXXXXX}},
  url = {{https://github.com/Nyx-Dynamics/lai-prep-bridge-decision-tool}}
}}
```

### Manuscript Citation

```bibtex
@article{{demidont2025bridging,
  author = {{Demidont, Adrian C. and Backus, Kandis V.}},
  title = {{Computational Validation of Clinical Decision Support Algorithm 
            for Long-Acting Injectable PrEP Bridge Period Navigation 
            at UNAIDS Global Target Scale}},
  journal = {{Viruses}},
  year = {{2025}},
  volume = {{XX}},
  number = {{XX}},
  pages = {{XXX--XXX}},
  doi = {{10.3390/vXXXXXXXX}}
}}
```

---

## License

This software is released under the **Pharma-Restricted Open Healthcare License v1.0**.

### Free for:
- Healthcare providers
- Researchers and academics
- Non-profit organizations
- Government agencies

### Requires permission for:
- Pharmaceutical companies (commercial use)
- Biotechnology companies (commercial use)

**Exception:** Patient care use by pharma-employed clinicians allowed with notification.

See `documentation/LICENSE.md` and `documentation/PHARMA_RESTRICTED_LICENSE.md` for full terms.

---

## Authors

**Adrian C. Demidont, DO**  
Infectious Diseases Physician  
Nyx Dynamics, LLC  
Email: acdemidont@nyxdynamics.org

**Kandis V. Backus, PharmD**  
Gilead Sciences

---

## Support

- **Issues:** https://github.com/Nyx-Dynamics/lai-prep-bridge-decision-tool/issues
- **Documentation:** https://github.com/Nyx-Dynamics/lai-prep-bridge-decision-tool/docs
- **Email:** acdemidont@nyxdynamics.org

---

## Acknowledgments

This work builds upon evidence from HPTN 083, HPTN 084, PURPOSE-1, PURPOSE-2, 
and real-world implementation studies. We acknowledge the trial participants, 
research teams, and the broader HIV prevention community.

---

*Generated by Zenodo Package Organizer on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
