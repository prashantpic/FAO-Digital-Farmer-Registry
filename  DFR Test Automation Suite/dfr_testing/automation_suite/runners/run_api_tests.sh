```bash
#!/bin/bash
# Script to run DFR API tests using PyTest

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
# Default environment is 'dev', can be overridden by the first command-line argument
TARGET_ENV=${1:-dev}
# Optional PyTest markers, overridden by the second command-line argument
# Example: "smoke" or "regression and not performance"
MARKERS=${2:-""} # Default to empty string if not provided

echo "--- Running DFR API Tests ---"
echo "Target Environment: $TARGET_ENV"
if [ -n "$MARKERS" ]; then
    echo "Applying Markers: $MARKERS"
else
    echo "No specific markers applied (running all API tests found by pytest in 'api_tests' path)."
fi

# --- Setup ---
# Determine the absolute path to the root of the test suite
# This script is in runners/, so go up one level
TEST_SUITE_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
echo "Test suite root directory: $TEST_SUITE_ROOT_DIR"

# Change to the test suite root directory
cd "$TEST_SUITE_ROOT_DIR"

# Activate virtual environment if used (example)
# if [ -f ".venv/bin/activate" ]; then
#     echo "Activating virtual environment..."
#     source .venv/bin/activate
# elif [ -f "venv/bin/activate" ]; then
#     echo "Activating virtual environment..."
#     source venv/bin/activate
# else
#     echo "No common virtual environment (.venv or venv) found. Running tests with system Python or globally installed packages."
# fi

# Set environment variable for config loading (used by utils/config_loader.py and global_config.py)
export DFR_TARGET_ENV=$TARGET_ENV
echo "Set DFR_TARGET_ENV=$DFR_TARGET_ENV"

# Ensure the reports directory exists (PyTest might also create it based on log_file path)
REPORTS_DIR="reports" # Relative to TEST_SUITE_ROOT_DIR
mkdir -p "$REPORTS_DIR"
echo "Ensured reports directory exists: $REPORTS_DIR"

# --- Build PyTest Arguments ---
# Standard arguments from pytest.ini are usually sufficient (testpaths, html report, log settings)
# This script can add or override specific options for this run.
PYTEST_COMMAND="pytest" # Use 'python -m pytest' if pytest is not directly on PATH
PYTEST_TARGET_PATH="api_tests" # Specify the directory to run tests from

# Basic options
PYTEST_ARGS="-v" # Verbose output
PYTEST_ARGS="$PYTEST_ARGS --durations=10" # Show top 10 slowest tests
# HTML report name specific to this runner
PYTEST_ARGS="$PYTEST_ARGS --html=$REPORTS_DIR/api_test_report_${TARGET_ENV}.html --self-contained-html"

# Add environment option for PyTest fixtures (e.g., if conftest.py uses --env)
PYTEST_ARGS="$PYTEST_ARGS --env=$TARGET_ENV"

if [ -n "$MARKERS" ]; then
    # Ensure markers with spaces or operators are correctly quoted for eval
    # Example: MARKERS="smoke and not performance"
    PYTEST_ARGS="$PYTEST_ARGS -m \"$MARKERS\""
fi

# --- Execute Tests ---
echo "Executing pytest for API tests..."
# The pytest.ini defines `testpaths`; running `pytest` from root should pick up `api_tests`
# However, explicitly stating `api_tests` can be clearer.
FULL_COMMAND="$PYTEST_COMMAND $PYTEST_TARGET_PATH $PYTEST_ARGS"
echo "Full command: $FULL_COMMAND"

# Use eval to correctly interpret quoted markers if they contain spaces or logical operators
eval $FULL_COMMAND
PYTEST_EXIT_CODE=$?

# --- Teardown and Reporting ---
# PyTest exit code indicates test outcome (0 = success, non-zero = failure or error)

if [ $PYTEST_EXIT_CODE -eq 0 ]; then
    echo "--- DFR API tests completed successfully for $TARGET_ENV. ---"
elif [ $PYTEST_EXIT_CODE -eq 5 ]; then
    echo "--- DFR API tests: No tests were collected for $TARGET_ENV with markers '$MARKERS'. Exit code: $PYTEST_EXIT_CODE ---"
else
    echo "--- DFR API tests failed for $TARGET_ENV. Exit code: $PYTEST_EXIT_CODE ---"
fi

# Deactivate virtual environment if used
# if type deactivate &>/dev/null; then
#     deactivate
#     echo "Deactivated virtual environment."
# fi

exit $PYTEST_EXIT_CODE # Exit the script with the PyTest execution exit code

```