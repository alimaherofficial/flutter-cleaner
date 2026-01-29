import os
import subprocess
from typing import List, Tuple

# Directories to skip during recursive search (performance optimization)
SKIP_DIRS = {
    '.git',           # Git repository data
    'node_modules',   # Node.js dependencies
    'build',          # Build artifacts
    '.dart_tool',     # Dart tooling cache
    '.idea',          # IntelliJ IDEA settings
    '.vscode',        # VS Code settings
    '.android',       # Android build artifacts
    '.ios'            # iOS build artifacts
}

# Maximum depth for recursive search
MAX_SEARCH_DEPTH = 5

def find_flutter_projects(base_dir: str, max_depth: int = MAX_SEARCH_DEPTH) -> List[str]:
    """
    Recursively find all Flutter projects in the directory tree
    Returns a list of absolute paths to Flutter projects (directories containing pubspec.yaml)
    """
    flutter_projects = []
    base_depth = base_dir.count(os.sep)

    for dirpath, dirnames, filenames in os.walk(base_dir):
        # Calculate current depth relative to base directory
        current_depth = dirpath.count(os.sep) - base_depth

        # Skip if we've exceeded max depth
        if current_depth >= max_depth:
            # Clear dirnames to prevent os.walk from descending further
            dirnames[:] = []
            continue

        # Skip directories in SKIP_DIRS (modify dirnames in-place to affect os.walk behavior)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        # Check if this directory is a Flutter project
        if 'pubspec.yaml' in filenames:
            flutter_projects.append(dirpath)

    return flutter_projects

def run_flutter_clean(project_path: str, base_dir: str) -> bool:
    """
    Run flutter clean in the specified project directory
    Args:
        project_path: Absolute path to the Flutter project
        base_dir: Base directory to return to after cleaning
    Returns:
        True if successful, False if there was an error
    """
    original_dir = os.getcwd()

    try:
        # Change to the project directory
        os.chdir(project_path)

        # Run flutter clean and capture output
        process = subprocess.run(['flutter', 'clean'],
                               capture_output=True,
                               text=True,
                               check=True)

        # Change back to original directory
        os.chdir(original_dir)
        return True

    except subprocess.CalledProcessError:
        # If flutter clean fails, change back to original directory and return False
        os.chdir(original_dir)
        return False
    except Exception:
        # For any other error, try to change back to original directory and return False
        try:
            os.chdir(original_dir)
        except:
            pass
        return False

def clean_flutter_projects() -> Tuple[List[str], List[str]]:
    """
    Recursively clean all Flutter projects in the directory tree
    Returns tuple of (successful_cleanups, failed_cleanups)
    """
    # Get the current working directory
    base_dir = os.getcwd()

    # Lists to track results
    successful_cleanups = []
    failed_cleanups = []

    # Find all Flutter projects recursively
    print(f"Scanning for Flutter projects (max depth: {MAX_SEARCH_DEPTH})...\n")
    flutter_projects = find_flutter_projects(base_dir)

    # Check if any projects were found
    if not flutter_projects:
        print("No Flutter projects found in directory tree")
        return successful_cleanups, failed_cleanups

    # Display all found projects
    print(f"Found {len(flutter_projects)} Flutter project{'s' if len(flutter_projects) != 1 else ''}:")
    for project_path in flutter_projects:
        relative_path = os.path.relpath(project_path, base_dir)
        print(f"  - {relative_path}")

    # Start cleanup process
    print("\nStarting cleanup...\n")

    # Process each Flutter project
    for project_path in flutter_projects:
        relative_path = os.path.relpath(project_path, base_dir)
        print(f"Processing {relative_path}...")

        # Run flutter clean
        if run_flutter_clean(project_path, base_dir):
            successful_cleanups.append(relative_path)
            print(f"✅ Successfully cleaned {relative_path}")
        else:
            failed_cleanups.append(relative_path)
            print(f"❌ Failed to clean {relative_path}")
        print()  # Add blank line between projects

    return successful_cleanups, failed_cleanups

def main():
    print("Starting Flutter projects cleanup...\n")
    
    successful, failed = clean_flutter_projects()
    
    print("\n=== CLEANUP SUMMARY ===")
    
    print("\n✅ Successfully cleaned projects:")
    if successful:
        for project in successful:
            print(f"  - {project}")
    else:
        print("  None")
    
    print("\n❌ Failed to clean projects:")
    if failed:
        for project in failed:
            print(f"  - {project}")
    else:
        print("  None")
    
    print(f"\nTotal: {len(successful)} succeeded, {len(failed)} failed")

if __name__ == "__main__":
    main()

