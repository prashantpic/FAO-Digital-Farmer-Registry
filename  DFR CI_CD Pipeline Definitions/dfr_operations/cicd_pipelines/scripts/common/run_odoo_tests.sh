#!/bin/bash
# Shell script to execute Odoo unit and/or integration tests.
#
# Purpose: Standardizes the execution of Odoo tests within CI/CD pipelines.
# Assumes `odoo-bin` is in the PATH or accessible within the execution environment.
#
# Inputs/Parameters (Environment Variables or Arguments):
#   ODOO_DATABASE_NAME: (Required) Name of the test database (e.g., test_dfr_cicd).
#   ODOO_MODULES_TO_TEST: (Required) Comma-separated list of Odoo modules to test (e.g., dfr_farmer_registry,dfr_dynamic_forms).
#                         Can be 'all' to test all DFR custom modules (requires further logic to determine these modules if 'all' is used).
#                         For simplicity, this script expects an explicit list if not 'all'.
#                         If 'all' is provided, it might imply that the Odoo instance is configured to run all its available tests.
#   TEST_TYPE: (Required, 'unit' or 'integration') Specifies the type of tests to run. This script uses it for logging and potential future conditional logic
#              (e.g., if Odoo test tags are used like --test-tags /module_name,:test_type).
#              Currently, Odoo's test runner itself might not differentiate test types by a simple flag; it depends on how tests are written and tagged.
#   ODOO_ADDONS_PATH: (Required) Path to Odoo addons, including custom DFR modules and Odoo core addons.
#                     (e.g., "/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons").
#   ODOO_CONFIG_FILE: (Optional) Path to an Odoo configuration file if needed.
#   DB_HOST: (Optional, default: localhost or Docker service name if run in CI with services) Database host.
#   DB_PORT: (Optional, default: 5432) Database port.
#   DB_USER: (Optional, default: odoo) Database user for Odoo.
#   DB_PASSWORD: (Optional, secret, default: odoo) Database password for Odoo user.

set -e
set -o pipefail

# --- Parameter Validation & Defaults ---
if [ -z "$ODOO_DATABASE_NAME" ]; then
    echo "Error: ODOO_DATABASE_NAME is required." >&2
    exit 1
fi
if [ -z "$ODOO_MODULES_TO_TEST" ]; then
    echo "Error: ODOO_MODULES_TO_TEST is required." >&2
    exit 1
fi
if [ -z "$TEST_TYPE" ]; then
    echo "Error: TEST_TYPE is required (e.g., 'unit', 'integration')." >&2
    exit 1
fi
if [ "$TEST_TYPE" != "unit" ] && [ "$TEST_TYPE" != "integration" ]; then
    echo "Error: TEST_TYPE must be 'unit' or 'integration'." >&2
    exit 1
fi
if [ -z "$ODOO_ADDONS_PATH" ]; then
    echo "Error: ODOO_ADDONS_PATH is required." >&2
    exit 1
fi

DB_HOST_PARAM=""
if [ -n "$DB_HOST" ]; then
    DB_HOST_PARAM="--db_host=${DB_HOST}"
fi

DB_PORT_PARAM=""
if [ -n "$DB_PORT" ]; then
    DB_PORT_PARAM="--db_port=${DB_PORT}"
fi

DB_USER_PARAM=""
if [ -n "$DB_USER" ]; then
    DB_USER_PARAM="--db_user=${DB_USER}"
fi

DB_PASSWORD_PARAM=""
if [ -n "$DB_PASSWORD" ]; then
    DB_PASSWORD_PARAM="--db_password=${DB_PASSWORD}"
fi

ODOO_CONFIG_PARAM=""
if [ -n "$ODOO_CONFIG_FILE" ]; then
    if [ ! -f "$ODOO_CONFIG_FILE" ]; then
        echo "Error: ODOO_CONFIG_FILE '$ODOO_CONFIG_FILE' not found." >&2
        exit 1
    fi
    ODOO_CONFIG_PARAM="--config=${ODOO_CONFIG_FILE}"
    echo "Using Odoo config file: ${ODOO_CONFIG_FILE}"
fi

# --- Main Logic ---
echo "Starting Odoo ${TEST_TYPE} tests..."
echo "Database Name: ${ODOO_DATABASE_NAME}"
echo "Modules to Test: ${ODOO_MODULES_TO_TEST}"
echo "Addons Path: ${ODOO_ADDONS_PATH}"
[ -n "$DB_HOST" ] && echo "DB Host: ${DB_HOST}"
[ -n "$DB_PORT" ] && echo "DB Port: ${DB_PORT}"
[ -n "$DB_USER" ] && echo "DB User: ${DB_USER}"
[ -n "$DB_PASSWORD" ] && echo "DB Password: [REDACTED]"


# Constructing the odoo-bin command for running tests.
# The basic command structure for Odoo tests is:
# odoo-bin \
#   -d <database_name> \                # Initialize a new database or use an existing one for tests
#   -i <module1,module2,...> \         # Install/Update and test specified modules
#   --addons-path=<path1,path2> \      # Specify addons paths
#   --test-enable \                    # Enable test mode (critical for running tests)
#   --stop-after-init \                # Stop the server after modules are initialized (and tests are run)
#   --log-level=test \                 # Set log level appropriate for testing
#   [db connection params]             # --db_host, --db_port, --db_user, --db_password
#   [--config <config_file>]           # Optional Odoo server config file
#
#   For specific test types (unit/integration), Odoo often relies on:
#   1. Module structure: Tests in `tests/test_foo.py` are discovered.
#   2. Test tags: `--test-tags [module_name][:class_name][.test_method_name]`
#      If your tests are tagged like `tagged('unit')` or `tagged('integration')`
#      within the Python test files, you might use `--test-tags :unit` or `--test-tags :integration`.
#      However, this script will pass the module names to `-i` which runs all tests in those modules.
#      Further filtering by TEST_TYPE would require a more sophisticated test tagging strategy
#      and modification of this command. For now, TEST_TYPE is mainly for informational purposes
#      or if the test setup for a module inherently runs only one type.

TEST_COMMAND="odoo-bin"
TEST_COMMAND="${TEST_COMMAND} -d ${ODOO_DATABASE_NAME}"
TEST_COMMAND="${TEST_COMMAND} -i ${ODOO_MODULES_TO_TEST}" # For 'all', this might need to be `-u all` or specific modules
TEST_COMMAND="${TEST_COMMAND} --addons-path=${ODOO_ADDONS_PATH}"
TEST_COMMAND="${TEST_COMMAND} --test-enable"
TEST_COMMAND="${TEST_COMMAND} --stop-after-init"
TEST_COMMAND="${TEST_COMMAND} --log-level=test" # Or 'debug' for more verbose output

# Add optional parameters
if [ -n "$ODOO_CONFIG_PARAM" ]; then
    TEST_COMMAND="${TEST_COMMAND} ${ODOO_CONFIG_PARAM}"
fi
if [ -n "$DB_HOST_PARAM" ]; then
    TEST_COMMAND="${TEST_COMMAND} ${DB_HOST_PARAM}"
fi
if [ -n "$DB_PORT_PARAM" ]; then
    TEST_COMMAND="${TEST_COMMAND} ${DB_PORT_PARAM}"
fi
if [ -n "$DB_USER_PARAM" ]; then
    TEST_COMMAND="${TEST_COMMAND} ${DB_USER_PARAM}"
fi
if [ -n "$DB_PASSWORD_PARAM" ]; then
    TEST_COMMAND="${TEST_COMMAND} ${DB_PASSWORD_PARAM}"
fi

# If using test tags for unit/integration, you might add something like:
# if [ "$TEST_TYPE" == "unit" ]; then
#   TEST_COMMAND="${TEST_COMMAND} --test-tags /${ODOO_MODULES_TO_TEST},:unit" # Example syntax
# elif [ "$TEST_TYPE" == "integration" ]; then
#   TEST_COMMAND="${TEST_COMMAND} --test-tags /${ODOO_MODULES_TO_TEST},:integration" # Example syntax
# fi
# This requires tests to be appropriately tagged within Odoo modules.
# For simplicity, we are not implementing test-tag based filtering by default here.

echo "Executing Odoo test command:"
echo "${TEST_COMMAND}" # Consider redacting password if it were directly in the command. Here it's via env or config.

# Execute the test command
# shellcheck disable=SC2086
eval ${TEST_COMMAND}
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "Error: Odoo tests failed with exit code ${TEST_EXIT_CODE}." >&2
    exit $TEST_EXIT_CODE
else
    echo "Odoo tests completed successfully."
fi

exit 0