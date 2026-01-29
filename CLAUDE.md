# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility script that automates running `flutter clean` on multiple Flutter projects within a directory tree. It recursively scans the current directory and all subdirectories (up to 5 levels deep) for Flutter projects containing `pubspec.yaml` files and runs `flutter clean` on each Flutter project found.

## Running the Script

```bash
python flutter_cleaner.py
```

The script should be run from a parent directory containing Flutter projects. It will:
1. Recursively scan all subdirectories (up to 5 levels deep) for Flutter projects (identified by `pubspec.yaml`)
2. Display a list of all found Flutter projects before cleaning
3. Run `flutter clean` on each Flutter project found
4. Report success/failure for each project

**Performance Optimizations**: The script automatically skips common non-project directories during the scan (`.git`, `node_modules`, `build`, `.dart_tool`, `.idea`, `.vscode`, `.android`, `.ios`) to improve search speed.

## Code Architecture

**Single-file utility**: The entire functionality is contained in `flutter_cleaner.py` with four main functions:

- `find_flutter_projects(base_dir: str, max_depth: int = 5)`: Recursively discovers all Flutter projects in the directory tree using `os.walk()`. Tracks directory depth to limit recursion and filters out skip directories for performance. Returns a list of absolute paths to Flutter projects.

- `run_flutter_clean(project_path: str, base_dir: str)`: Executes `flutter clean` in a specific project directory using absolute paths. Handles directory navigation and error recovery by always storing and returning to the original directory.

- `clean_flutter_projects()`: Main orchestration function that uses `find_flutter_projects()` to discover all Flutter projects, displays them to the user, then processes each one. Returns a tuple of (successful_cleanups, failed_cleanups) lists with relative paths.

- `main()`: Entry point that calls the cleanup process and displays formatted results.

**Configuration Constants**:
- `SKIP_DIRS`: Set of directory names to skip during recursive search for performance optimization
- `MAX_SEARCH_DEPTH`: Maximum directory depth for recursive search (default: 5 levels)

**Error Handling Pattern**: The script uses defensive directory navigation - `run_flutter_clean()` stores the original directory before navigation and always attempts to return to it in both success and error cases to prevent the working directory from getting stuck in a subdirectory.

## Requirements

- Python 3.6+ (uses type hints)
- Flutter SDK must be installed and available in PATH
- Script can be run in any directory; it will recursively find all Flutter projects within the directory tree (up to 5 levels deep)
