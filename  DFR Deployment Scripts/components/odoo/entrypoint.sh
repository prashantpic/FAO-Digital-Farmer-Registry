#!/bin/bash
set -e

# Source utility functions
# Adjust the path if utils.sh is located elsewhere, assuming it's two levels up in shared/scripts
UTILS_PATH=$(dirname "$0")/../../shared/scripts/utils.sh
if [ -f "$UTILS_PATH" ]; then
    # shellcheck source=../../shared/scripts/utils.sh
    source "$UTILS_PATH"
else
    echo "Error: utils.sh not found at $UTILS_PATH"
    exit 1
fi

# Default values
: "${DB_HOST:=postgres}"
: "${DB_PORT:=5432}"
: "${DB_USER:=odoo}"
: "${DB_NAME:=odoo}"
: "${DB_TIMEOUT:=60}"
: "${ODOO_CONF_TEMPLATE:=/etc/odoo/odoo.conf.template}"
: "${ODOO_CONF:=/etc/odoo/odoo.conf}"
: "${ODOO_DEFAULT_ADDONS_PATH:=/usr/lib/python3/dist-packages/odoo/addons}" # May vary by Odoo installation
: "${ODOO_EXTRA_ADDONS_PATH:=/mnt/extra-addons}"

# Wait for PostgreSQL
log_info "Waiting for PostgreSQL server at ${DB_HOST}:${DB_PORT}..."
WAIT_START_TIME=$(date +%s)
while ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -q; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - WAIT_START_TIME))
    if [ "${ELAPSED_TIME}" -ge "${DB_TIMEOUT}" ]; then
        log_error "Timeout waiting for PostgreSQL server at ${DB_HOST}:${DB_PORT} after ${DB_TIMEOUT} seconds."
        exit 1
    fi
    log_info "PostgreSQL is unavailable - sleeping for 5 seconds..."
    sleep 5
done
log_success "PostgreSQL server is ready."

# Configuration Generation
log_info "Generating Odoo configuration file from template..."
if [ ! -f "${ODOO_CONF_TEMPLATE}" ]; then
    log_error "Odoo configuration template ${ODOO_CONF_TEMPLATE} not found."
    exit 1
fi

cp "${ODOO_CONF_TEMPLATE}" "${ODOO_CONF}"

# Substitute environment variables into odoo.conf
# Ensure all required ODOO_* and DB_* variables are set in the environment
# For variables with defaults in the template (e.g., {{VAR | default(value)}}),
# this simple envsubst won't handle them. The template should be designed for envsubst
# or a more sophisticated templating tool should be used.
# For now, assuming direct placeholder replacement.

# ODOO_ADDONS_PATH should combine default and extra addons
export ODOO_FINAL_ADDONS_PATH="${ODOO_DEFAULT_ADDONS_PATH},${ODOO_EXTRA_ADDONS_PATH}"
if [ -n "$CUSTOM_ADDONS_PATH" ]; then # Allow further customization if needed
    export ODOO_FINAL_ADDONS_PATH="${ODOO_FINAL_ADDONS_PATH},${CUSTOM_ADDONS_PATH}"
fi

# List of variables to substitute - ensure they are exported or use a different method
VARS_TO_SUBSTITUTE=$(env | grep -E '^ODOO_|^DB_' | awk -F= '{print "$"$1}')
# Add specific vars that might not follow the pattern or need defaults handled by shell
VARS_TO_SUBSTITUTE="$VARS_TO_SUBSTITUTE \$ODOO_FINAL_ADDONS_PATH"

# Create a temporary file for envsubst input to handle defaults gracefully if not set
TEMP_CONF_FOR_ENVBST=$(mktemp)
# shellcheck disable=SC2016 # We want literal $ expansion by envsubst
eval "echo \"$(cat ${ODOO_CONF})\"" > "$TEMP_CONF_FOR_ENVBST"

# Replace placeholders using envsubst
# Note: envsubst only substitutes variables that are set.
# This approach replaces {{VAR_NAME}} with the value of VAR_NAME.
# If a variable is not set, {{VAR_NAME}} will remain.
# The odoo.conf.template should use syntax like {{ODOO_DB_HOST}} not ${ODOO_DB_HOST} for this to work.
# A more robust solution might involve sed or awk for each placeholder.
# For simplicity, using sed for direct replacement based on SDS placeholders.

sed_expressions=""
add_sed_expr() {
    # $1: placeholder like {{VAR_NAME}}
    # $2: env var name like VAR_NAME
    # $3: default value (optional)
    placeholder="$1"
    var_name="$2"
    default_value="$3"
    env_var_value=$(printenv "$var_name")

    if [ -n "$env_var_value" ]; then
        val_to_sub="$env_var_value"
    elif [ -n "$default_value" ]; then
        val_to_sub="$default_value"
    else
        # If no env var and no default, placeholder might remain or be empty.
        # Depending on Odoo's tolerance, this could be an issue.
        # For required fields, ensure env vars are set.
        log_warning "Environment variable $var_name is not set and no default provided for $placeholder."
        val_to_sub="" # Or keep placeholder: val_to_sub="$placeholder"
    fi
    # Escape for sed: special characters like / & \
    val_to_sub_escaped=$(echo "$val_to_sub" | sed -e 's/[\/&]/\\&/g')
    sed_expressions="${sed_expressions} -e s|${placeholder}|${val_to_sub_escaped}|g"
}

# Add substitutions based on odoo.conf.template placeholders
add_sed_expr "{{ODOO_ADMIN_PASSWD}}" "ODOO_ADMIN_PASSWD" "admin" # Default for safety, should be overridden
add_sed_expr "{{ODOO_DB_HOST}}" "DB_HOST" "${DB_HOST}"
add_sed_expr "{{ODOO_DB_PORT}}" "DB_PORT" "${DB_PORT}"
add_sed_expr "{{ODOO_DB_USER}}" "DB_USER" "${DB_USER}"
add_sed_expr "{{ODOO_DB_PASSWORD}}" "DB_PASSWORD" "" # No default for password
# addons_path is handled differently due to concatenation
# add_sed_expr "{{ODOO_ADDONS_PATH}}" "ODOO_FINAL_ADDONS_PATH" # This placeholder is not in SDS example
add_sed_expr "{{ODOO_WORKERS}}" "ODOO_WORKERS" "0"
add_sed_expr "{{ODOO_LIMIT_TIME_CPU}}" "ODOO_LIMIT_TIME_CPU" "600"
add_sed_expr "{{ODOO_LIMIT_TIME_REAL}}" "ODOO_LIMIT_TIME_REAL" "1200"
# proxy_mode is True by default in template
add_sed_expr "{{ODOO_LOG_LEVEL}}" "ODOO_LOG_LEVEL" "info"
add_sed_expr "{{ODOO_LIST_DB}}" "ODOO_LIST_DB" "True"
# data_dir is /var/lib/odoo by default in template

# Manual substitution for addons_path as it's complex
addons_path_escaped=$(echo "$ODOO_FINAL_ADDONS_PATH" | sed -e 's/[\/&]/\\&/g')
sed_expressions="${sed_expressions} -e s|^addons_path = .*|addons_path = ${addons_path_escaped}|g"


# Apply sed substitutions
# shellcheck disable=SC2086 # We want word splitting for sed_expressions
sed ${sed_expressions} "$TEMP_CONF_FOR_ENVBST" > "${ODOO_CONF}"
rm "$TEMP_CONF_FOR_ENVBST"

log_success "Odoo configuration file ${ODOO_CONF} generated."
log_info "Generated odoo.conf content:"
cat "${ODOO_CONF}" # For debugging

# Database Initialization/Update (Optional)
# This part is complex and depends on specific project needs (e.g., which modules to init/update)
# For a generic entrypoint, it's often better to handle DB init/update as a separate step
# or via a CI/CD pipeline job after deployment.
# ODOO_AUTO_INIT_DB and ODOO_AUTO_UPDATE_MODULES can be used as flags.

if [[ "${ODOO_AUTO_INIT_DB}" == "true" || "${ODOO_AUTO_UPDATE_MODULES}" == "true" ]]; then
    log_info "Attempting automatic database initialization/update..."
    # Check if DB exists. This is a basic check.
    # psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -lqt | cut -d \| -f 1 | grep -qw "${DB_NAME}"
    # If DB does not exist and ODOO_AUTO_INIT_DB is true:
    #   odoo -c "${ODOO_CONF}" -d "${DB_NAME}" --init="${ODOO_MODULES_TO_INIT:-all}" --stop-after-init
    # If ODOO_AUTO_UPDATE_MODULES is true (and DB exists):
    #   odoo -c "${ODOO_CONF}" -d "${DB_NAME}" --update="${ODOO_MODULES_TO_UPDATE:-all}" --stop-after-init
    # This requires ODOO_MODULES_TO_INIT and ODOO_MODULES_TO_UPDATE to be set.
    # Example:
    if [[ "${ODOO_AUTO_INIT_DB}" == "true" && -n "${ODOO_MODULES_TO_INIT}" ]]; then
        log_info "Running Odoo DB initialization for modules: ${ODOO_MODULES_TO_INIT}..."
        odoo -c "${ODOO_CONF}" -d "${DB_NAME}" --init="${ODOO_MODULES_TO_INIT}" --stop-after-init || log_warning "DB Init command failed. Continuing..."
        log_success "Odoo DB initialization finished."
    fi
    if [[ "${ODOO_AUTO_UPDATE_MODULES}" == "true" && -n "${ODOO_MODULES_TO_UPDATE}" ]]; then
        log_info "Running Odoo DB update for modules: ${ODOO_MODULES_TO_UPDATE}..."
        odoo -c "${ODOO_CONF}" -d "${DB_NAME}" --update="${ODOO_MODULES_TO_UPDATE}" --stop-after-init || log_warning "DB Update command failed. Continuing..."
        log_success "Odoo DB update finished."
    fi
else
    log_info "Automatic database initialization/update is disabled."
fi

# Start Odoo Server
log_info "Starting Odoo server..."
exec odoo -c "${ODOO_CONF}" "$@"