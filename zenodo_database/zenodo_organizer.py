#!/usr/bin/env python3
"""
LAI-PrEP Bridge Tool Zenodo Package Organizer

This script organizes project files into a structured package for Zenodo upload.
It creates appropriate subdirectories, generates a README, computes checksums,
and prepares all materials for DOI assignment and archival.

Author: A.C. Demidont, DO
Organization: Nyx Dynamics, LLC
Created: 2025
"""

import os
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import argparse


@dataclass
class FileCategory:
    """Represents a category of files for organization"""
    name: str
    description: str
    subdirectory: str
    patterns: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


class ZenodoPackageOrganizer:
    """
    Organizes LAI-PrEP Bridge Tool files for Zenodo upload.

    Creates a structured package with:
    - Core algorithm code
    - Configuration files
    - Test suites
    - Validation results
    - Documentation
    - Figures
    - Supplementary materials
    - Manuscript PDFs
    """

    def __init__(self, source_dir: str, output_dir: str, profile: Optional[str] = None):
        """
        Initialize the organizer.

        Args:
            source_dir: Path to source project files
            output_dir: Path for organized Zenodo package
        """
        # Fixed source directory per user request
        self.source_dir = Path("/")
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
        # Package profile selection (for splitting into BTG vs LAI)
        self.profile: Optional[str] = (profile or "").lower() or None

        # Fixed output directory per user request (adjusted by profile when provided)
        if self.profile == "btg":
            self.output_dir = Path("/Users/acdmbpmax/Desktop/btg_bridge_tool_zenodo_package")
        elif self.profile == "lai":
            self.output_dir = Path("/Users/acdmbpmax/Desktop/lai_bridge_tool_zenodo_package")
        else:
            self.output_dir = Path("/Users/acdmbpmax/Desktop/lai_bridge_tool_zenodo_package")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest: Dict[str, dict] = {}
        self.stats = {
            'files_copied': 0,
            'total_size': 0,
            'categories': {}
        }

        # Define file categories with organization rules
        self.categories = self._define_categories()

        # Define profile-specific inclusion rules (currently applied to Figures only)
        self.profiles: Dict[str, Dict[str, List[str]]] = {
            "btg": {
                # BTG (bridge tool general) — emphasize general workflow/equity/interventions/populations/impact/barriers
                "figures_include_patterns": [
                    "figures/figure1_critical_insights*.*",
                    "figures/figure2_workflow*.*",
                    "figures/figure3_convergence*.*",
                    "figures/figure4_*.*",
                    "figures/figure5_*.*",
                    "figures/figure7_*.*",
                    "figures/figure8_impact*.*",
                    "figures/figure_equity_pathways*.*",
                    "figures/RWE_PrEP_DC.png",
                ]
            },
            "lai": {
                # LAI-specific — oral vs LAI comparisons and major trial figures
                "figures_include_patterns": [
                    "figures/HPTN*.png",
                    "figures/PURPOSE*.png",
                    "figures/figure_oral_vs_lai_MDPI.*",
                    "figures/figure_1A_*.*",
                    "figures/figure_1B_*.*",
                ]
            },
        }

    def _define_categories(self) -> List[FileCategory]:
        """Define file categories and their organization rules"""
        return [
            # Code
            FileCategory(
                name="Core Algorithm",
                description="Main decision support algorithm implementation",
                subdirectory="code/algorithm",
                patterns=[
                    "SCR/lai_prep_decision_tool*.py",
                    "SCR/LAI_DMT_v*.py"
                ]
            ),
            FileCategory(
                name="Command Line Interface",
                description="CLI for tool interaction and batch processing",
                subdirectory="code/cli",
                files=[
                    "SCR/cli.py",
                    "SCR/code/cli/cli.py"
                ]
            ),
            FileCategory(
                name="Test Suites",
                description="Comprehensive testing for validation",
                subdirectory="code/tests",
                patterns=[
                    "SCR/test_*.py",
                    "SCR/code/tests/*.py"
                ]
            ),
            # Config and machine-readable data
            FileCategory(
                name="Configuration",
                description="External JSON configuration and machine-readable data",
                subdirectory="config",
                patterns=[
                    "*.json",
                    "SCR/*.json",
                    "lai_prep_config*.json",
                    "lai_prep_bridge_tool_*.json"
                ],
                files=["SCR/lai_prep_config_FIXED.json"]
            ),
            # Validation artifacts
            FileCategory(
                name="Validation Results",
                description="Progressive validation datasets (1M to 21.2M scale)",
                subdirectory="validation",
                patterns=[
                    "Validation_progressive/validation_*.json",
                    "Validation_progressive/*.md"
                ]
            ),
            # Figures
            FileCategory(
                name="Figures",
                description="Publication figures and visualizations",
                subdirectory="figures",
                patterns=[
                    "figures/*.png",
                    "figures/figure*.png",
                    "figures/M*.png",
                    "figures/*MDPI.pdf",
                    "figures/figure*.pdf"
                ]
            ),
            # Supplementary sources
            FileCategory(
                name="Supplementary LaTeX",
                description="Supplementary material LaTeX source files",
                subdirectory="supplementary/latex",
                patterns=["Supplementary_File_*.tex"]
            ),
            FileCategory(
                name="Word Documents",
                description="Supplementary Word documents",
                subdirectory="supplementary/docx",
                patterns=["*.docx"]
            ),
            # Documentation and project docs
            FileCategory(
                name="Documentation Markdown",
                description="Project documentation and guides",
                subdirectory="documentation",
                patterns=[
                    "Project Docs/*.md",
                    "Clinical Implementation Guides/*.md",
                    "README*.md"
                ]
            ),
            # Manuscripts (PDFs)
            FileCategory(
                name="Manuscript PDFs",
                description="Main manuscript and supplementary PDFs",
                subdirectory="manuscripts",
                patterns=["*.pdf"]
            ),
            # Data examples
            FileCategory(
                name="Data Examples",
                description="Example patient JSON/CSV files",
                subdirectory="data_examples",
                patterns=[
                    "Clinical Implementation Guides/*.csv",
                    "Clinical Implementation Guides/*.json"
                ]
            ),
            # Repo metadata
            FileCategory(
                name="Repository Metadata",
                description="Citation and archival metadata",
                subdirectory="repo",
                files=[
                    "CITATION.cff",
                    ".zenodo.json",
                    "Project Docs/LICENSE",
                    "Project Docs/LICENSE.md",
                    "Project Docs/PHARMA_RESTRICTED_LICENSE.md"
                ]
            ),
            # HTML visualizations
            FileCategory(
                name="HTML Visualizations",
                description="Interactive HTML visualizations",
                subdirectory="visualizations",
                patterns=["*.html"]
            )
        ]

    def compute_checksum(self, filepath: Path) -> str:
        """Compute SHA-256 checksum for a file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def get_file_size_human(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def matches_pattern(self, relpath: str, patterns: List[str]) -> bool:
        """Check if relative path or basename matches any of the glob patterns"""
        from fnmatch import fnmatch
        basename = os.path.basename(relpath)
        return any(
            fnmatch(relpath, pattern) or fnmatch(basename, pattern)
            for pattern in patterns
        )

    def categorize_files(self) -> Dict[str, List[Path]]:
        """
        Recursively categorize all source files into their appropriate categories.

        Returns:
            Dictionary mapping category names to list of file paths
        """
        categorized: Dict[str, List[Path]] = {cat.name: [] for cat in self.categories}
        uncategorized: List[Path] = []

        # Get all files in source directory
        if not self.source_dir.exists():
            print(f"Warning: Source directory {self.source_dir} does not exist")
            return categorized

        exclude_dirs = {".git", "__pycache__", "githooks", ".venv", "venv", ".idea", ".pytest_cache", ".mypy_cache", ".ipynb_checkpoints"}
        exclude_name_patterns = {".DS_Store"}

        for item in self.source_dir.rglob("*"):
            if item.is_dir():
                # Skip excluded directories quickly
                if item.name in exclude_dirs:
                    # prevent descending further by skipping children is not trivial with rglob
                    # rely on name checks for files below
                    continue
                continue
            # Files only below
            if item.name in exclude_name_patterns or item.suffix == ".pyc":
                continue
            # Skip anything under excluded dirs by checking parts
            parts = set(p.name for p in item.parents)
            if parts & exclude_dirs:
                continue

            relpath = item.relative_to(self.source_dir).as_posix()
            placed = False

            for category in self.categories:
                # Check explicit file list first (support both exact relpath and basename entries)
                if relpath in category.files or item.name in category.files:
                    categorized[category.name].append(item)
                    placed = True
                    break
                # Then check patterns (which may include directory-aware globs)
                if self.matches_pattern(relpath, category.patterns):
                    categorized[category.name].append(item)
                    placed = True
                    break

            if not placed:
                uncategorized.append(item)

        if uncategorized:
            print(f"\nUncategorized files ({len(uncategorized)}), showing first 200:")
            for f in sorted(uncategorized)[:200]:
                print(f"  - {f.relative_to(self.source_dir).as_posix()}")
            if len(uncategorized) > 200:
                print(f"  ... and {len(uncategorized) - 200} more (suppressed)")

        return categorized

    def create_directory_structure(self):
        """Create the output directory structure"""
        # Clean and create base output directory
        if self.output_dir.exists():
            print(f"Removing existing directory: {self.output_dir}")
            shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each category
        for category in self.categories:
            subdir = self.output_dir / category.subdirectory
            subdir.mkdir(parents=True, exist_ok=True)
            print(f"Created: {subdir}")

    def copy_files(self, categorized: Dict[str, List[Path]]):
        """Copy files to their designated locations"""
        print("\nCopying files...")

        for category in self.categories:
            files = categorized.get(category.name, [])
            if not files:
                continue

            dest_dir = self.output_dir / category.subdirectory

            # Apply profile-specific filtering for figures to keep packages parallel but targeted
            if self.profile in self.profiles and category.name == "Figures":
                inc_patterns = self.profiles[self.profile].get("figures_include_patterns", [])
                if inc_patterns:
                    files = [
                        f for f in files
                        if self.matches_pattern(f.relative_to(self.source_dir).as_posix(), inc_patterns)
                    ]
                    if not files:
                        # Skip category if nothing matches after filtering
                        continue
            category_size = 0

            print(f"\n{category.name} ({len(files)} files):")

            for src_file in files:
                dest_file = dest_dir / src_file.name
                shutil.copy2(src_file, dest_file)

                # Compute checksum and record metadata
                file_size = dest_file.stat().st_size
                checksum = self.compute_checksum(dest_file)

                relative_path = str(dest_file.relative_to(self.output_dir))
                self.manifest[relative_path] = {
                    'original_name': src_file.name,
                    'category': category.name,
                    'size_bytes': file_size,
                    'size_human': self.get_file_size_human(file_size),
                    'sha256': checksum,
                    'copied_at': datetime.now().isoformat()
                }

                category_size += file_size
                self.stats['files_copied'] += 1
                self.stats['total_size'] += file_size

                print(f"  ✓ {src_file.name} ({self.get_file_size_human(file_size)})")

            self.stats['categories'][category.name] = {
                'files': len(files),
                'size': category_size,
                'size_human': self.get_file_size_human(category_size)
            }

    def generate_readme(self) -> str:
        """Generate comprehensive README for Zenodo package"""
        readme = f"""# LAI-PrEP Bridge Period Decision Support Tool

## Zenodo Archive Package

**Version:** 2.1.0  
**DOI:** [To be assigned upon upload]  
**Date:** {datetime.now().strftime('%B %d, %Y')}  
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

"""
        # Add category descriptions
        for category in self.categories:
            stats = self.stats['categories'].get(category.name, {'files': 0, 'size_human': '0 B'})
            if stats['files'] > 0:
                readme += f"""### {category.name}
**Directory:** `{category.subdirectory}/`  
**Files:** {stats['files']}  
**Size:** {stats['size_human']}

{category.description}

"""

        readme += """---

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
"""
        return readme

    def generate_manifest(self) -> str:
        """Generate JSON manifest with file metadata"""
        manifest_data = {
            'package_info': {
                'name': 'LAI-PrEP Bridge Period Decision Support Tool',
                'version': '2.1.0',
                'created': datetime.now().isoformat(),
                'total_files': self.stats['files_copied'],
                'total_size_bytes': self.stats['total_size'],
                'total_size_human': self.get_file_size_human(self.stats['total_size'])
            },
            'categories': self.stats['categories'],
            'files': self.manifest
        }
        return json.dumps(manifest_data, indent=2)

    def generate_checksums(self) -> str:
        """Generate SHA-256 checksum file"""
        lines = ["# SHA-256 Checksums for LAI-PrEP Bridge Tool Zenodo Package",
                 f"# Generated: {datetime.now().isoformat()}",
                 ""]

        for filepath, metadata in sorted(self.manifest.items()):
            lines.append(f"{metadata['sha256']}  {filepath}")

        return "\n".join(lines)

    def create_zenodo_metadata(self) -> str:
        """Generate .zenodo.json metadata file"""
        if self.profile == "btg":
            title = "Bridge-to-Get (BTG) Manuscript Package: LAI-PrEP Bridge Decision Support Tool"
            description = (
                "Package for the BTG manuscript accompanying the LAI-PrEP Bridge Period Decision "
                "Support Tool. Includes code, configuration, documentation, and BTG-focused figures "
                "(workflow, equity pathways, populations, barriers, interventions, impact)."
            )
        elif self.profile == "lai":
            title = "LAI Manuscript Package: LAI-PrEP Bridge Period Decision Support Tool"
            description = (
                "Package for the LAI-focused manuscript accompanying the LAI-PrEP Bridge Period Decision "
                "Support Tool. Includes code, configuration, documentation, and LAI-specific figures "
                "(oral vs LAI comparisons and key trial visuals such as HPTN 083/084 and PURPOSE-1/2)."
            )
        else:
            title = "LAI-PrEP Bridge Period Decision Support Tool"
            description = (
                "Clinical decision support algorithm for Long-Acting Injectable PrEP (LAI-PrEP) bridge "
                "period navigation. Helps clinicians identify patient risk factors and recommend "
                "evidence-based interventions to improve the probability of successful transition "
                "from prescription to first injection. Validated at UNAIDS global target scale "
                "(21.2 million patients)."
            )

        metadata = {
            "title": title,
            "description": description,
            "creators": [
                {
                    "name": "Demidont, Adrian C.",
                    "affiliation": "Nyx Dynamics, LLC",
                    "orcid": "0000-0000-0000-0000"  # Placeholder - update with real ORCID
                },
                {
                    "name": "Backus, Kandis V.",
                    "affiliation": "Gilead Sciences"
                }
            ],
            "keywords": [
                "HIV prevention",
                "PrEP",
                "long-acting injectable",
                "cabotegravir",
                "lenacapavir",
                "clinical decision support",
                "implementation science",
                "health equity",
                "patient navigation"
            ],
            "license": {
                "id": "other-open"
            },
            "upload_type": "software",
            "publication_date": datetime.now().strftime("%Y-%m-%d"),
            "access_right": "open",
            "related_identifiers": [
                {
                    "identifier": "https://github.com/Nyx-Dynamics/lai-prep-bridge-decision-tool",
                    "relation": "isSupplementTo",
                    "resource_type": "software"
                }
            ],
            "communities": [
                {"identifier": "hiv-prevention"},
                {"identifier": "clinical-decision-support"}
            ],
            "grants": [],
            "version": "2.1.0"
        }
        return json.dumps(metadata, indent=2)

    def organize(self) -> bool:
        """
        Main method to organize all files for Zenodo upload.

        Returns:
            True if successful, False otherwise
        """
        print("=" * 70)
        print("LAI-PrEP Bridge Tool Zenodo Package Organizer")
        print("=" * 70)
        print(f"\nSource: {self.source_dir}")
        print(f"Output: {self.output_dir}")

        # Step 1: Categorize files
        print("\n[1/5] Categorizing source files...")
        categorized = self.categorize_files()

        # Step 2: Create directory structure
        print("\n[2/5] Creating directory structure...")
        self.create_directory_structure()

        # Step 3: Copy files
        print("\n[3/5] Copying and checksumming files...")
        self.copy_files(categorized)

        # Step 4: Generate documentation files
        print("\n[4/5] Generating documentation...")

        # README
        readme_path = self.output_dir / "README.md"
        readme_content = self.generate_readme()
        readme_path.write_text(readme_content)
        print(f"  ✓ README.md ({self.get_file_size_human(len(readme_content))})")

        # Manifest
        manifest_path = self.output_dir / "MANIFEST.json"
        manifest_content = self.generate_manifest()
        manifest_path.write_text(manifest_content)
        print(f"  ✓ MANIFEST.json ({self.get_file_size_human(len(manifest_content))})")

        # Checksums
        checksums_path = self.output_dir / "CHECKSUMS.sha256"
        checksums_content = self.generate_checksums()
        checksums_path.write_text(checksums_content)
        print(f"  ✓ CHECKSUMS.sha256 ({self.get_file_size_human(len(checksums_content))})")

        # Zenodo metadata
        zenodo_meta_path = self.output_dir / ".zenodo.json"
        zenodo_meta_content = self.create_zenodo_metadata()
        zenodo_meta_path.write_text(zenodo_meta_content)
        print(f"  ✓ .zenodo.json ({self.get_file_size_human(len(zenodo_meta_content))})")

        # Step 5: Summary
        print("\n[5/5] Package Summary")
        print("=" * 70)
        print(f"\nTotal files copied: {self.stats['files_copied']}")
        print(f"Total size: {self.get_file_size_human(self.stats['total_size'])}")
        print("\nFiles by category:")
        for cat_name, cat_stats in self.stats['categories'].items():
            if cat_stats['files'] > 0:
                print(f"  • {cat_name}: {cat_stats['files']} files ({cat_stats['size_human']})")

        print(f"\n✅ Package ready at: {self.output_dir}")
        print("\nNext steps for Zenodo upload:")
        print("  1. Review package contents")
        print("  2. Update .zenodo.json with your ORCID")
        print("  3. Create new upload at zenodo.org")
        print("  4. Upload entire directory as ZIP or individual files")
        print("  5. Reserve DOI and publish")

        return True


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Organize LAI-PrEP Bridge Tool files for Zenodo upload",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Organize files from project directory to output directory
  python zenodo_organizer.py /path/to/project /path/to/output

  # Use default paths
  python zenodo_organizer.py

  # Build only BTG package
  python zenodo_organizer.py --profile btg

  # Build only LAI package
  python zenodo_organizer.py --profile lai

  # Build both BTG and LAI packages
  python zenodo_organizer.py --both
        """
    )

    parser.add_argument(
        'source',
        nargs='?',
        default='/mnt/project',
        help='Source directory containing project files (default: /mnt/project)'
    )

    parser.add_argument(
        'output',
        nargs='?',
        default='/mnt/user-data/outputs/lai_bridge_tool_zenodo_package',
        help='Output directory for Zenodo package (default: /mnt/user-data/outputs/lai_bridge_tool_zenodo_package)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without copying files'
    )

    parser.add_argument(
        '--profile', choices=['btg', 'lai'],
        help='Select which package profile to build (btg or lai). If omitted and --both is not set, defaults to LAI.'
    )

    parser.add_argument(
        '--both', action='store_true',
        help='Build both BTG and LAI packages in parallel output directories.'
    )

    args = parser.parse_args()

    # Determine profiles to build
    profiles: List[Optional[str]]
    if args.both:
        profiles = ['btg', 'lai']
    else:
        profiles = [args.profile or 'lai']

    exit_code = 0
    for prof in profiles:
        # Create organizer and run per profile
        organizer = ZenodoPackageOrganizer(args.source, args.output, profile=prof)

        if args.dry_run:
            print(f"DRY RUN - No files will be copied (profile={prof})")
            categorized = organizer.categorize_files()
            print("\nWould organize the following files:")
            for cat_name, files in categorized.items():
                if files:
                    print(f"\n{cat_name}:")
                    for f in files:
                        print(f"  - {f.name}")
        else:
            success = organizer.organize()
            if not success:
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    exit(main())