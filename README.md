# Flutter Cleaner

A Python utility that automates running `flutter clean` on multiple Flutter projects within a directory tree.

## Features

- 🔍 **Recursive Discovery**: Automatically finds all Flutter projects (directories with `pubspec.yaml`) up to 5 levels deep
- ⚡ **Performance Optimized**: Skips common non-project directories (`.git`, `node_modules`, `build`, etc.)
- 📊 **Clear Reporting**: Shows a summary of successful and failed cleanups
- 🛡️ **Safe Navigation**: Always returns to the original directory after processing

## Requirements

- Python 3.6+
- Flutter SDK installed and available in PATH

## Usage

Run the script from a parent directory containing your Flutter projects:

```bash
python flutter_cleaner.py
```

The script will:
1. Scan all subdirectories for Flutter projects
2. Display found projects
3. Run `flutter clean` on each project
4. Report the results

### Example Output

```
Starting Flutter projects cleanup...

Scanning for Flutter projects (max depth: 5)...

Found 3 Flutter projects:
  - ./mobile_app
  - ./web_dashboard
  - ./tools/helper

Starting cleanup...

Processing ./mobile_app...
✅ Successfully cleaned ./mobile_app

Processing ./web_dashboard...
✅ Successfully cleaned ./web_dashboard

Processing ./tools/helper...
❌ Failed to clean ./tools/helper

=== CLEANUP SUMMARY ===

✅ Successfully cleaned projects:
  - ./mobile_app
  - ./web_dashboard

❌ Failed to clean projects:
  - ./tools/helper

Total: 2 succeeded, 1 failed
```

## Configuration

You can modify these constants in `flutter_cleaner.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `MAX_SEARCH_DEPTH` | `5` | Maximum directory depth to search |
| `SKIP_DIRS` | See code | Directories to skip during scan |

## What Gets Cleaned?

This script runs `flutter clean` on each found project, which removes:
- `build/` directory
- `.dart_tool/` directory
- Generated plugin registrants
- Other temporary build artifacts

## License

MIT
