#!/usr/bin/env python3
"""
Manuscript Organization Tool for BTG and LAI Papers
====================================================
Scans directories for manuscript versions, categorizes them, and helps
organize by archiving intermediate versions and cleaning up early drafts.

Usage:
    python organize_manuscripts.py [directory] [--dry-run] [--archive-dir PATH]

Examples:
    python organize_manuscripts.py ~/Documents --dry-run
    python organize_manuscripts.py /path/to/manuscripts --archive-dir ~/Archives/Viruses
"""

import os
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse
import json

# =============================================================================
# CONFIGURATION - Customize these patterns for your manuscripts
# =============================================================================

MANUSCRIPT_PATTERNS = {
    'BTG': {
        'name': 'Bridge-to-Gap Conceptual Framework',
        'patterns': [
            # Direct BTG matches
            r'btg.*\.(tex|pdf|docx?|md|txt)$',
            r'BTG.*\.(tex|pdf|docx?|md|txt)$',
            # Conceptual variations
            r'bridge.*gap.*\.(tex|pdf|docx?|md)$',
            r'bridge.*period.*\.(tex|pdf|docx?|md)$',
            r'cascade.*reconceptuali.*\.(tex|pdf|docx?|md)$',
            r'prep.*cascade.*\.(tex|pdf|docx?|md)$',
            # Viruses journal specific
            r'viruses.*4064402.*\.(tex|pdf|docx?)$',
            r'viruses.*manuscript.*1.*\.(tex|pdf|docx?)$',
            r'manuscript.*1.*viruses.*\.(tex|pdf|docx?)$',
            # Common naming patterns
            r'.*conceptual.*framework.*prep.*\.(tex|pdf|docx?)$',
            r'.*framework.*paper.*\.(tex|pdf|docx?)$',
        ],
        'final_indicators': ['final', 'submitted', 'submission', 'revised', 'r1', 'r2', 'accepted', 'proof', 'galley'],
        'draft_indicators': ['draft', 'wip', 'working', 'temp', 'old', 'v0', 'v1', 'initial', 'rough', 'notes',
                             'outline', 'scratch'],
    },
    'LAI': {
        'name': 'LAI-PrEP Decision Tool Validation',
        'patterns': [
            # Direct LAI matches
            r'lai.*\.(tex|pdf|docx?|md|txt)$',
            r'LAI.*\.(tex|pdf|docx?|md|txt)$',
            # Validation paper variations
            r'decision.*tool.*validation.*\.(tex|pdf|docx?|md)$',
            r'validation.*paper.*\.(tex|pdf|docx?|md)$',
            r'prep.*bridge.*tool.*\.(tex|pdf|docx?|md)$',
            r'algorithm.*validation.*\.(tex|pdf|docx?|md)$',
            # Viruses journal specific
            r'viruses.*manuscript.*2.*\.(tex|pdf|docx?)$',
            r'manuscript.*2.*viruses.*\.(tex|pdf|docx?)$',
            # UNAIDS related
            r'.*unaids.*validation.*\.(tex|pdf|docx?|md)$',
            r'.*21.*million.*\.(tex|pdf|docx?)$',
        ],
        'final_indicators': ['final', 'submitted', 'submission', 'revised', 'r1', 'r2', 'accepted', 'proof', 'galley',
                             'v2_1', 'v2.1'],
        'draft_indicators': ['draft', 'wip', 'working', 'temp', 'old', 'v0', 'v1', 'initial', 'rough', 'notes',
                             'outline', 'scratch'],
    },
    'SUPPLEMENTARY': {
        'name': 'Supplementary Materials',
        'patterns': [
            r'.*_S\d+\.(pdf|docx?|xlsx?|png|jpg)$',  # S1, S2, etc.
            r'.*S\d+_.*\.(pdf|docx?|xlsx?|png|jpg)$',  # S1_, S2_, etc.
            r'.*supplement.*\.(pdf|docx?|xlsx?)$',
            r'.*appendix.*\.(pdf|docx?|xlsx?)$',
            r'.*supporting.*info.*\.(pdf|docx?)$',
            r'.*table_?S?\d+.*\.(pdf|docx?|xlsx?)$',
            r'.*figure_?S?\d+.*\.(pdf|png|jpg|tiff?)$',
            r'.*supp.*material.*\.(pdf|docx?|zip)$',
        ],
        'final_indicators': ['final', 'submitted', 'submission'],
        'draft_indicators': ['draft', 'wip', 'old', 'temp'],
    },
    'FIGURES': {
        'name': 'Manuscript Figures',
        'patterns': [
            r'figure_?\d+.*\.(png|pdf|jpg|jpeg|tiff?|eps|svg)$',
            r'fig_?\d+.*\.(png|pdf|jpg|jpeg|tiff?|eps|svg)$',
            r'Figure_?\d+.*\.(png|pdf|jpg|jpeg|tiff?|eps|svg)$',
            r'Fig_?\d+.*\.(png|pdf|jpg|jpeg|tiff?|eps|svg)$',
            # Specific figure types from your papers
            r'.*cascade.*\.(png|pdf|svg)$',
            r'.*workflow.*\.(png|pdf|svg)$',
            r'.*convergence.*\.(png|pdf|svg)$',
            r'.*paradox.*\.(png|pdf|svg)$',
            r'.*barrier.*\.(png|pdf|svg)$',
            r'.*population.*\.(png|pdf|svg)$',
            r'.*intervention.*\.(png|pdf|svg)$',
            r'.*regional.*\.(png|pdf|svg)$',
            r'.*impact.*\.(png|pdf|svg)$',
            r'.*flowchart.*\.(png|pdf|svg)$',
            r'.*diagram.*\.(png|pdf|svg)$',
            # Graphical abstract
            r'.*graphical.*abstract.*\.(png|pdf|jpg|tiff?)$',
            r'.*toc.*graphic.*\.(png|pdf|jpg|tiff?)$',
        ],
        'final_indicators': ['final', 'submitted', 'trim', 'clean', 'print', 'high_?res', '300dpi', 'production'],
        'draft_indicators': ['draft', 'wip', 'old', 'test', 'rough', 'sketch', 'lowres', 'preview'],
    },
    'VALIDATION': {
        'name': 'Validation Results',
        'patterns': [
            r'validation.*\.(json|csv|xlsx?)$',
            r'.*results.*\.(json|csv)$',
            r'test.*results.*\.(json|csv)$',
            r'.*output.*\.(json|csv)$',
            r'.*simulation.*results.*\.(json|csv|xlsx?)$',
            r'.*unaids.*\.(json|csv)$',
            r'.*\d+[mMkK]_?results.*\.(json|csv)$',  # 1M_results, 10M_results, etc.
        ],
        'final_indicators': ['final', 'UNAIDS', '21_2M', '21.2M', '10M', '1M', 'official'],
        'draft_indicators': ['test', 'temp', 'debug', 'scratch', 'trial'],
    },
    'CODE': {
        'name': 'Decision Tool Code',
        'patterns': [
            r'lai_prep.*\.py$',
            r'.*decision.*tool.*\.py$',
            r'test_.*\.py$',
            r'validate.*\.py$',
            r'.*config.*\.json$',
            r'run_.*\.py$',
            r'.*_tool\.py$',
            r'cli\.py$',
        ],
        'final_indicators': ['v2', 'v2_1', 'FIXED', 'final', 'release', 'stable'],
        'draft_indicators': ['old', 'backup', 'temp', 'test_old', 'deprecated', 'archive'],
    },
    'LATEX': {
        'name': 'LaTeX Source Files',
        'patterns': [
            r'.*\.tex$',
            r'.*\.bib$',
            r'.*\.bst$',
            r'.*\.cls$',
            r'.*\.sty$',
        ],
        'final_indicators': ['final', 'submitted', 'main', 'revised'],
        'draft_indicators': ['draft', 'old', 'backup', 'temp', 'working'],
    },
    'OVERLEAF': {
        'name': 'Overleaf Exports/Backups',
        'patterns': [
            r'.*overleaf.*\.(zip|tar\.gz)$',
            r'.*backup.*\d{4}.*\.(zip|tar\.gz)$',
            r'.*export.*\d{4}.*\.(zip|tar\.gz)$',
            r'.*viruses.*\.(zip|tar\.gz)$',
        ],
        'final_indicators': ['final', 'submitted'],
        'draft_indicators': ['backup', 'old', 'archive'],
    },
    'CORRESPONDENCE': {
        'name': 'Journal Correspondence',
        'patterns': [
            r'.*cover.*letter.*\.(pdf|docx?)$',
            r'.*response.*reviewer.*\.(pdf|docx?)$',
            r'.*rebuttal.*\.(pdf|docx?)$',
            r'.*revision.*notes.*\.(pdf|docx?)$',
            r'.*author.*response.*\.(pdf|docx?)$',
            r'.*peer.*review.*\.(pdf|docx?)$',
            r'.*editor.*letter.*\.(pdf|docx?)$',
            r'.*decision.*letter.*\.(pdf|docx?)$',
        ],
        'final_indicators': ['final', 'submitted', 'sent'],
        'draft_indicators': ['draft', 'wip', 'working'],
    },
}

# Files that should NEVER be deleted (even if they look like drafts)
PROTECTED_FILES = [
    'btg_final_submission_main',
    'btg_final_submission_S',
    'lai_final_submission_main',
    'lai_final_submission_S',
    'validation_UNAIDS',
    'validation_10M',
    'validation_1M',
    'lai_prep_decision_tool_v2',
    'lai_prep_config_FIXED',
    'BTG_final_viruses_main',
]

# Common directories where manuscript files accumulate
COMMON_SEARCH_DIRS = [
    '~/Documents',
    '~/Downloads',
    '~/Desktop',
    '~/Dropbox',
    '~/Google Drive',
    '~/OneDrive',
    '~/Box',
    '~/iCloud Drive',
    '~/Library/Mobile Documents',  # macOS iCloud
    '/tmp',
    '~/Projects',
    '~/Research',
    '~/Papers',
    '~/Manuscripts',
    '~/Viruses',
    '~/Work',
    '~/Overleaf',
]


# =============================================================================
# FILE CATEGORIZATION
# =============================================================================

class ManuscriptFile:
    """Represents a manuscript-related file with metadata."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.size = path.stat().st_size
        self.modified = datetime.fromtimestamp(path.stat().st_mtime)
        self.category = self._determine_category()
        self.manuscript_type = self._determine_manuscript_type()
        self.status = self._determine_status()
        self.is_protected = self._check_protected()
        self.hash = None  # Computed on demand

    def _determine_category(self) -> str:
        """Determine which category this file belongs to."""
        name_lower = self.name.lower()
        for cat_name, cat_info in MANUSCRIPT_PATTERNS.items():
            for pattern in cat_info['patterns']:
                if re.search(pattern, self.name, re.IGNORECASE):
                    return cat_name
        return 'OTHER'

    def _determine_manuscript_type(self) -> str:
        """Determine if this is BTG or LAI related."""
        name_lower = self.name.lower()
        if 'btg' in name_lower or 'bridge' in name_lower and 'gap' in name_lower:
            return 'BTG'
        elif 'lai' in name_lower or 'decision' in name_lower and 'tool' in name_lower:
            return 'LAI'
        elif '_s' in name_lower and self.name.endswith('.pdf'):
            # Supplementary files - check prefix
            if name_lower.startswith('btg'):
                return 'BTG'
            elif name_lower.startswith('lai'):
                return 'LAI'
        return 'SHARED'

    def _determine_status(self) -> str:
        """Determine file status: FINAL, WORKING, DRAFT, or UNKNOWN."""
        name_lower = self.name.lower()

        # Check for final indicators
        cat_info = MANUSCRIPT_PATTERNS.get(self.category, {})
        final_indicators = cat_info.get('final_indicators', [])
        draft_indicators = cat_info.get('draft_indicators', [])

        for indicator in final_indicators:
            if indicator.lower() in name_lower:
                return 'FINAL'

        for indicator in draft_indicators:
            if indicator.lower() in name_lower:
                return 'DRAFT'

        # Check version numbers - higher versions are likely more recent
        version_match = re.search(r'v(\d+)', name_lower)
        if version_match:
            version = int(version_match.group(1))
            if version >= 2:
                return 'FINAL'
            else:
                return 'DRAFT'

        return 'WORKING'

    def _check_protected(self) -> bool:
        """Check if this file is protected from deletion."""
        for protected in PROTECTED_FILES:
            if protected.lower() in self.name.lower():
                return True
        return False

    def compute_hash(self) -> str:
        """Compute MD5 hash for duplicate detection."""
        if self.hash is None:
            hasher = hashlib.md5()
            with open(self.path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hasher.update(chunk)
            self.hash = hasher.hexdigest()
        return self.hash

    def __repr__(self):
        return f"ManuscriptFile({self.name}, {self.category}, {self.status})"


# =============================================================================
# SCANNER
# =============================================================================

class ManuscriptScanner:
    """Scans directories for manuscript files."""

    def __init__(self, root_dirs: list):
        self.root_dirs = [Path(d) for d in root_dirs]
        self.files = []
        self.by_category = defaultdict(list)
        self.by_type = defaultdict(list)
        self.by_status = defaultdict(list)
        self.duplicates = []

    def scan(self, recursive: bool = True):
        """Scan directories for manuscript files."""
        print(f"\n📂 Scanning directories...")

        all_patterns = []
        for cat_info in MANUSCRIPT_PATTERNS.values():
            all_patterns.extend(cat_info['patterns'])

        for root_dir in self.root_dirs:
            if not root_dir.exists():
                print(f"  ⚠️  Directory not found: {root_dir}")
                continue

            print(f"  Scanning: {root_dir}")

            if recursive:
                file_iter = root_dir.rglob('*')
            else:
                file_iter = root_dir.glob('*')

            for file_path in file_iter:
                if not file_path.is_file():
                    continue

                # Skip hidden files and common non-manuscript locations
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                if any(skip in str(file_path) for skip in ['node_modules', '__pycache__', '.git', 'venv']):
                    continue

                # Check if file matches any pattern
                for pattern in all_patterns:
                    if re.search(pattern, file_path.name, re.IGNORECASE):
                        mf = ManuscriptFile(file_path)
                        self.files.append(mf)
                        self.by_category[mf.category].append(mf)
                        self.by_type[mf.manuscript_type].append(mf)
                        self.by_status[mf.status].append(mf)
                        break

        print(f"  Found {len(self.files)} manuscript-related files")
        return self

    def find_duplicates(self):
        """Find duplicate files by content hash."""
        print("\n🔍 Checking for duplicates...")
        hash_map = defaultdict(list)

        for mf in self.files:
            if mf.size > 0:  # Skip empty files
                file_hash = mf.compute_hash()
                hash_map[file_hash].append(mf)

        self.duplicates = [files for files in hash_map.values() if len(files) > 1]

        if self.duplicates:
            print(f"  Found {len(self.duplicates)} sets of duplicate files")
        else:
            print("  No duplicates found")

        return self.duplicates

    def generate_report(self) -> str:
        """Generate a summary report."""
        lines = [
            "=" * 70,
            "MANUSCRIPT ORGANIZATION REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 70,
            "",
            "SUMMARY BY MANUSCRIPT TYPE",
            "-" * 40,
        ]

        for mtype, files in sorted(self.by_type.items()):
            lines.append(f"  {mtype}: {len(files)} files")

        lines.extend([
            "",
            "SUMMARY BY STATUS",
            "-" * 40,
        ])

        for status, files in sorted(self.by_status.items()):
            lines.append(f"  {status}: {len(files)} files")

        lines.extend([
            "",
            "SUMMARY BY CATEGORY",
            "-" * 40,
        ])

        for category, files in sorted(self.by_category.items()):
            cat_name = MANUSCRIPT_PATTERNS.get(category, {}).get('name', category)
            lines.append(f"  {cat_name}: {len(files)} files")

        lines.extend([
            "",
            "DETAILED FILE LIST",
            "-" * 40,
        ])

        # Group by manuscript type and status
        for mtype in ['BTG', 'LAI', 'SHARED']:
            type_files = self.by_type.get(mtype, [])
            if not type_files:
                continue

            lines.append(f"\n### {mtype} ###")

            for status in ['FINAL', 'WORKING', 'DRAFT']:
                status_files = [f for f in type_files if f.status == status]
                if not status_files:
                    continue

                lines.append(f"\n  [{status}]")
                for mf in sorted(status_files, key=lambda x: x.modified, reverse=True):
                    protected = "🔒" if mf.is_protected else "  "
                    size_kb = mf.size / 1024
                    if size_kb > 1024:
                        size_str = f"{size_kb / 1024:.1f} MB"
                    else:
                        size_str = f"{size_kb:.0f} KB"
                    lines.append(f"    {protected} {mf.name}")
                    lines.append(f"         {mf.modified.strftime('%Y-%m-%d %H:%M')} | {size_str}")
                    lines.append(f"         {mf.path}")

        if self.duplicates:
            lines.extend([
                "",
                "DUPLICATE FILES",
                "-" * 40,
            ])
            for i, dup_set in enumerate(self.duplicates, 1):
                lines.append(f"\n  Duplicate Set #{i}:")
                for mf in dup_set:
                    lines.append(f"    - {mf.path}")

        return "\n".join(lines)


# =============================================================================
# ORGANIZER
# =============================================================================

class ManuscriptOrganizer:
    """Organizes manuscript files: archive, delete, and restructure."""

    def __init__(self, scanner: ManuscriptScanner, archive_dir: Path = None):
        self.scanner = scanner
        self.archive_dir = archive_dir or Path.home() / "Archives" / "Viruses_Manuscripts"
        self.actions = []

    def plan_organization(self) -> list:
        """Plan organization actions without executing them."""
        self.actions = []

        # 1. Identify files to keep (FINAL and protected)
        keep_files = []
        for mf in self.scanner.files:
            if mf.is_protected or mf.status == 'FINAL':
                keep_files.append(mf)
                self.actions.append({
                    'action': 'KEEP',
                    'file': mf,
                    'reason': 'Protected file' if mf.is_protected else 'Final version'
                })

        # 2. Identify files to archive (WORKING status)
        for mf in self.scanner.files:
            if mf.status == 'WORKING' and not mf.is_protected:
                self.actions.append({
                    'action': 'ARCHIVE',
                    'file': mf,
                    'destination': self.archive_dir / mf.manuscript_type / mf.name,
                    'reason': 'Working version - archiving'
                })

        # 3. Identify files to delete (DRAFT status and duplicates)
        for mf in self.scanner.files:
            if mf.status == 'DRAFT' and not mf.is_protected:
                self.actions.append({
                    'action': 'DELETE',
                    'file': mf,
                    'reason': 'Early draft version'
                })

        # 4. Handle duplicates - keep newest, archive/delete others
        for dup_set in self.scanner.duplicates:
            # Sort by modified time, newest first
            sorted_dups = sorted(dup_set, key=lambda x: x.modified, reverse=True)
            newest = sorted_dups[0]

            # Keep the newest if not already marked
            if not any(a['file'] == newest and a['action'] == 'KEEP' for a in self.actions):
                # Remove any existing action for this file
                self.actions = [a for a in self.actions if a['file'] != newest]
                self.actions.append({
                    'action': 'KEEP',
                    'file': newest,
                    'reason': 'Newest duplicate'
                })

            # Archive or delete older duplicates
            for older in sorted_dups[1:]:
                if older.is_protected:
                    continue
                # Remove existing action and add DELETE
                self.actions = [a for a in self.actions if a['file'] != older]
                self.actions.append({
                    'action': 'DELETE',
                    'file': older,
                    'reason': f'Duplicate of {newest.name}'
                })

        return self.actions

    def print_plan(self):
        """Print the organization plan."""
        print("\n" + "=" * 70)
        print("ORGANIZATION PLAN")
        print("=" * 70)

        by_action = defaultdict(list)
        for action in self.actions:
            by_action[action['action']].append(action)

        for action_type in ['KEEP', 'ARCHIVE', 'DELETE']:
            items = by_action.get(action_type, [])
            if not items:
                continue

            icon = {'KEEP': '✅', 'ARCHIVE': '📦', 'DELETE': '🗑️ '}[action_type]
            print(f"\n{icon} {action_type} ({len(items)} files)")
            print("-" * 40)

            for item in items:
                mf = item['file']
                print(f"  {mf.name}")
                print(f"     Reason: {item['reason']}")
                if 'destination' in item:
                    print(f"     → {item['destination']}")

    def execute(self, dry_run: bool = True):
        """Execute the organization plan."""
        if dry_run:
            print("\n⚠️  DRY RUN - No files will be modified")
        else:
            print("\n🚀 EXECUTING ORGANIZATION PLAN")

        archived = 0
        deleted = 0
        errors = []

        # Create archive directory structure
        if not dry_run:
            for mtype in ['BTG', 'LAI', 'SHARED']:
                (self.archive_dir / mtype).mkdir(parents=True, exist_ok=True)

        for action in self.actions:
            action_type = action['action']
            mf = action['file']

            if action_type == 'KEEP':
                print(f"  ✅ Keeping: {mf.name}")

            elif action_type == 'ARCHIVE':
                dest = action['destination']
                print(f"  📦 Archiving: {mf.name}")
                print(f"     → {dest}")

                if not dry_run:
                    try:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(mf.path, dest)
                        archived += 1
                    except Exception as e:
                        errors.append(f"Failed to archive {mf.name}: {e}")

            elif action_type == 'DELETE':
                print(f"  🗑️  Deleting: {mf.name}")

                if not dry_run:
                    try:
                        mf.path.unlink()
                        deleted += 1
                    except Exception as e:
                        errors.append(f"Failed to delete {mf.name}: {e}")

        print(f"\n{'DRY RUN ' if dry_run else ''}SUMMARY:")
        print(f"  Files archived: {archived}")
        print(f"  Files deleted: {deleted}")

        if errors:
            print(f"\n⚠️  ERRORS ({len(errors)}):")
            for err in errors:
                print(f"  - {err}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Organize BTG and LAI manuscript files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Documents --dry-run
  %(prog)s --find-all                    # Search all common locations
  %(prog)s --find-all --execute          # Search and clean up
  %(prog)s /path/to/manuscripts --archive-dir ~/Archives/Viruses

Actions:
  KEEP    - Files marked as final or protected (never modified)
  ARCHIVE - Working versions moved to archive directory  
  DELETE  - Early drafts removed (with confirmation)

Status indicators:
  🔒 Protected - will never be deleted
  ✅ FINAL    - submitted/accepted versions
  📦 WORKING  - intermediate versions (will be archived)
  🗑️  DRAFT    - early versions (will be deleted)
        """
    )

    parser.add_argument(
        'directories',
        nargs='*',
        default=[],
        help='Directories to scan (default: current directory)'
    )

    parser.add_argument(
        '--find-all', '-f',
        action='store_true',
        help='Search all common locations (Documents, Downloads, Desktop, Dropbox, etc.)'
    )

    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        default=True,
        help='Show what would be done without making changes (default: True)'
    )

    parser.add_argument(
        '--execute', '-x',
        action='store_true',
        help='Actually execute the organization (disables dry-run)'
    )

    parser.add_argument(
        '--archive-dir', '-a',
        type=Path,
        default=None,
        help='Directory for archived files (default: ~/Archives/Viruses_Manuscripts)'
    )

    parser.add_argument(
        '--no-recursive', '-R',
        action='store_true',
        help='Do not scan subdirectories'
    )

    parser.add_argument(
        '--report', '-r',
        type=Path,
        default=None,
        help='Save report to file'
    )

    parser.add_argument(
        '--delete-duplicates',
        action='store_true',
        help='Also delete duplicate files (keeps newest)'
    )

    args = parser.parse_args()

    # Determine directories to scan
    if args.find_all:
        search_dirs = []
        for dir_path in COMMON_SEARCH_DIRS:
            expanded = Path(dir_path).expanduser()
            if expanded.exists():
                search_dirs.append(str(expanded))
                print(f"  ✓ Found: {expanded}")
            else:
                pass  # Silently skip non-existent directories
        if not search_dirs:
            print("❌ No common directories found!")
            return
    elif args.directories:
        search_dirs = args.directories
    else:
        search_dirs = ['.']

    # Scan
    scanner = ManuscriptScanner(search_dirs)
    scanner.scan(recursive=not args.no_recursive)
    scanner.find_duplicates()

    # Generate and display report
    report = scanner.generate_report()
    print(report)

    if args.report:
        args.report.write_text(report)
        print(f"\n📄 Report saved to: {args.report}")

    # Plan and execute organization
    organizer = ManuscriptOrganizer(scanner, args.archive_dir)
    organizer.plan_organization()
    organizer.print_plan()

    dry_run = args.dry_run and not args.execute

    if not dry_run:
        print("\n" + "=" * 70)
        response = input("⚠️  Are you sure you want to proceed? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    organizer.execute(dry_run=dry_run)

    print("\n✨ Done!")


if __name__ == '__main__':
    main()