#!/bin/bash
# Master script to run all DFR automated test suites

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
# Default environment, can be overridden by the first command-line argument
TARGET_ENV=${1:-dev}

# Optional markers for each suite, can be overridden by subsequent arguments
# Example: "./run_all_tests.sh dev smoke 'web and not performance' 'mobile and not offline_sync' 'integration'"
MARKERS_API=${2:-''}
MARKERS_WEB=${3:-''}
MARKERS_MOBILE=${4:-''}
MARKERS_INTEGRATION=${5:-''}


echo "--- Starting DFR Full Test Suite ---"
echo "Target Environment: $TARGET_ENV"
echo "API Markers: '$MARKERS_API'"
echo "Web Markers: '$MARKERS_WEB'"
echo "Mobile Markers: '$MARKERS_MOBILE'"
echo "Integration Markers: '$MARKERS_INTEGRATION'"


# --- Setup ---
# Determine the absolute path to the root of the test suite
TEST_SUITE_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
echo "Test suite root directory: $TEST_SUITE_ROOT_DIR"

# Change to the test suite root directory
cd "$TEST_SUITE_ROOT_DIR"

# Activate virtual environment if used
# Example: source .venv/bin/activate
# if [ -d ".venv" ]; then
#     echo "Activating virtual environment..."
#     source .venv/bin/activate
# else
#     echo "No virtual environment found at .venv. Running tests with system Python."
# fi

# Set environment variable for config loading (used by utils/config_loader.py)
export DFR_TARGET_ENV=$TARGET_ENV
echo "Set DFR_TARGET_ENV=$DFR_TARGET_ENV"

# Ensure the reports directory exists
mkdir -p reports
echo "Ensured reports directory exists: reports"

# --- Execute Test Suites ---
OVERALL_EXIT_CODE=0

echo "----------------------------------------"
echo "Running API Tests..."
echo "----------------------------------------"
# Pass environment and markers to the specific runner script
./runners/run_api_tests.sh "$TARGET_ENV" "$MARKERS_API"
API_EXIT_CODE=$?
if [ $API_EXIT_CODE -ne 0 ]; then
    echo "API tests failed with exit code $API_EXIT_CODE."
    OVERALL_EXIT_CODE=1
fi
echo "----------------------------------------"


# echo "----------------------------------------"
# echo "Running Web E2E Tests..."
# echo "----------------------------------------"
# # Assuming run_web_e2e_tests.sh exists and handles browser/headless options internally or via env vars
# # Example: Pass env and markers
# # Note: Selenium/WebDriver setup typically needs browser installed and driver available (via webdriver-manager or PATH)
# ./runners/run_web_e2e_tests.sh "$TARGET_ENV" "$MARKERS_WEB"
# WEB_EXIT_CODE=$?
# if [ $WEB_EXIT_CODE -ne 0 ]; then
#      echo "Web E2E tests failed with exit code $WEB_EXIT_CODE."
#      OVERALL_EXIT_CODE=1
# fi
# echo "----------------------------------------"


# echo "----------------------------------------"
# echo "Running Mobile E2E Tests (Android - Appium/Python)..."
# echo "----------------------------------------"
# # Ensure Appium server is running and accessible for these tests before running the script
# # Example: Pass env and markers
# ./runners/run_mobile_android_appium_tests.sh "$TARGET_ENV" "$MARKERS_MOBILE"
# MOBILE_ANDROID_EXIT_CODE=$?
# if [ $MOBILE_ANDROID_EXIT_CODE -ne 0 ]; then
#       echo "Mobile Android Appium tests failed with exit code $MOBILE_ANDROID_EXIT_CODE."
#       OVERALL_EXIT_CODE=1
# fi
# echo "----------------------------------------"

# # Note: Flutter Driver tests are typically run using the `flutter drive` command,
# # not directly by `pytest`. A runner script would execute this command.
# echo "----------------------------------------"
# echo "Running Mobile E2E Tests (Flutter Driver)..."
# echo "----------------------------------------"
# ./runners/run_mobile_flutter_driver_tests.sh "$TARGET_ENV" "$MARKERS_MOBILE"
# MOBILE_FLUTTER_EXIT_CODE=$?
# if [ $MOBILE_FLUTTER_EXIT_CODE -ne 0 ]; then
#       echo "Mobile Flutter Driver tests failed with exit code $MOBILE_FLUTTER_EXIT_CODE."
#       OVERALL_EXIT_CODE=1
# fi
# echo "----------------------------------------"


# echo "----------------------------------------"
# echo "Running Odoo Integration Tests..."
# echo "----------------------------------------"
# # Ensure Odoo test environment/DB is accessible
# ./runners/run_odoo_integration_tests.sh "$TARGET_ENV" "$MARKERS_INTEGRATION"
# ODOO_EXIT_CODE=$?
# if [ $ODOO_EXIT_CODE -ne 0 ]; then
#      echo "Odoo Integration tests failed with exit code $ODOO_EXIT_CODE."
#      OVERALL_EXIT_CODE=1
# fi
# echo "----------------------------------------"


echo "----------------------------------------"
if [ $OVERALL_EXIT_CODE -eq 0 ]; then
    echo "All executed test suites completed successfully for $TARGET_ENV."
else
    echo "One or more test suites failed for $TARGET_ENV. Overall Exit code: $OVERALL_EXIT_CODE"
fi
echo "----------------------------------------"

# Deactivate virtual environment if used
# if [ -d ".venv" ]; then
#     deactivate
#     echo "Deactivated virtual environment."
# fi

exit $OVERALL_EXIT_CODE