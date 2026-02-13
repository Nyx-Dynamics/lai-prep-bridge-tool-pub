import os
import subprocess
from pathlib import Path

def sync_projects():
    # Define the base directory for your projects
    base_dir = Path.home() / "PycharmProjects"
    
    if not base_dir.exists():
        print(f"Error: Directory {base_dir} not found.")
        return

    print(f"--- Starting Sync for projects in {base_dir} ---\n")

    # Find all directories that contain a .git folder
    projects = [p.parent for p in base_dir.rglob(".git") if p.is_dir()]

    summary = {"success": [], "up_to_date": [], "error": [], "manual": []}

    for project in projects:
        print(f"Updating: {project.name}...")
        try:
            # 1. Try to pull using rebase and autostash (handles local changes and divergent branches)
            # We use --rebase to keep history clean and --autostash to temporarily hide local changes
            result = subprocess.run(
                ["git", "pull", "--rebase", "--autostash"],
                cwd=project,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if "Already up to date" in result.stdout:
                    print(f"  ✅ Up to date.")
                    summary["up_to_date"].append(project.name)
                else:
                    print(f"  🚀 Updated successfully (rebased & autostashed).")
                    summary["success"].append(project.name)
            
            # 2. Handle specific common errors
            else:
                stderr = result.stderr.lower()
                if "no tracking information" in stderr:
                    print(f"  ⚠️  No tracking info. Trying to link to origin/main...")
                    # Attempt to fix tracking if on main
                    fix_result = subprocess.run(
                        ["git", "branch", "--set-upstream-to=origin/main"],
                        cwd=project, capture_output=True, text=True
                    )
                    if fix_result.returncode == 0:
                        print(f"  ✅ Linked to origin/main. Please run sync again.")
                        summary["success"].append(f"{project.name} (linked)")
                    else:
                        print(f"  ❌ Manual Action: Run 'git branch --set-upstream-to=origin/<branch>'")
                        summary["manual"].append(project.name)
                
                elif "conflict" in stderr or "merge" in stderr:
                    print(f"  ❌ Conflict detected. Please resolve manually.")
                    summary["error"].append(project.name)
                
                else:
                    print(f"  ❌ Error: {result.stderr.strip()[:100]}...")
                    summary["error"].append(project.name)

        except Exception as e:
            print(f"  ⚠️ Failed to run git: {e}")
            summary["error"].append(project.name)
        print("-" * 30)

    # Print Summary
    print("\n" + "="*40)
    print("           SYNC SUMMARY")
    print("="*40)
    print(f"✅ Up to Date: {len(summary['up_to_date'])}")
    print(f"🚀 Updated:    {len(summary['success'])}")
    print(f"⚠️  Manual Fix: {len(summary['manual'])}")
    print(f"❌ Errors:     {len(summary['error'])}")
    
    if summary['manual'] or summary['error']:
        print("\nProjects needing attention:")
        for p in summary['manual'] + summary['error']:
            print(f" - {p}")
    print("="*40)

    print("\n--- Sync Complete ---")

if __name__ == "__main__":
    sync_projects()
