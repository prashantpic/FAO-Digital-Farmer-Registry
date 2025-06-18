#!/bin/bash
set -e
set -o pipefail

# Script to restore PostgreSQL database and Odoo filestore for DFR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
UTILS_SCRIPT_PATH="${SCRIPT_DIR}/../../shared/scripts/utils.sh"

if [ ! -f "$UTILS_SCRIPT_PATH" ]; then
    echo "Error: utils.sh not found at $UTILS_SCRIPT_PATH"
    exit 1
fi
# shellcheck source=../../shared/scripts/utils.sh
source "$UTILS_SCRIPT_PATH"

if [ -z "$ENV" ]; then
    log_error "Environment variable ENV is not set. Please set ENV (e.g., development, staging, production)."
    exit 1
fi

CONFIG_FILE_PATH="${SCRIPT_DIR}/../config/backup_vars.sh.${ENV}"
if [ ! -f "$CONFIG_FILE_PATH" ]; then
    log_error "Restore configuration file $CONFIG_FILE_PATH not found for environment '$ENV'."
    exit 1
fi
# shellcheck source=../config/backup_vars.sh.template
source "$CONFIG_FILE_PATH"
log_info "Loaded restore configuration from $CONFIG_FILE_PATH for environment '$ENV'."

# Script arguments
DB_BACKUP_FILE_ARG="$1"
FILESTORE_BACKUP_FILE_ARG="$2" # Optional

if [ -z "$DB_BACKUP_FILE_ARG" ]; then
    log_error "Usage: $0 <path_to_db_backup_file> [path_to_filestore_backup_file]"
    log_error "Example: $0 /backups/dfr_db_20230101_120000.dump /backups/dfr_filestore_20230101_120000.tar.gz"
    exit 1
fi

if [ ! -f "$DB_BACKUP_FILE_ARG" ]; then
    log_error "Database backup file '$DB_BACKUP_FILE_ARG' not found."
    exit 1
fi

if [ -n "$FILESTORE_BACKUP_FILE_ARG" ] && [ ! -f "$FILESTORE_BACKUP_FILE_ARG" ]; then
    log_error "Filestore backup file '$FILESTORE_BACKUP_FILE_ARG' specified but not found."
    exit 1
fi

# Validate required variables from config
REQUIRED_VARS=("DFR_DB_HOST" "DFR_DB_PORT" "DFR_DB_USER" "DFR_DB_NAME" "ODOO_SERVICE_NAME")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        log_error "Required configuration variable $var is not set in $CONFIG_FILE_PATH."
        exit 1
    fi
done

if [ -z "$DFR_DB_PASSWORD" ] && [ -z "$DFR_DB_PASSWORD_FILE" ]; then
    log_error "Either DFR_DB_PASSWORD or DFR_DB_PASSWORD_FILE must be set for database authentication."
    exit 1
fi

if [ -n "$DFR_DB_PASSWORD_FILE" ] && [ ! -f "$DFR_DB_PASSWORD_FILE" ]; then
    log_error "Password file $DFR_DB_PASSWORD_FILE specified but not found."
    exit 1
fi

export PGPASSWORD
if [ -n "$DFR_DB_PASSWORD_FILE" ]; then
    PGPASSWORD=$(cat "$DFR_DB_PASSWORD_FILE")
elif [ -n "$DFR_DB_PASSWORD" ]; then
    PGPASSWORD="$DFR_DB_PASSWORD"
fi

# Path to the docker-compose file for the environment
# Assuming this script is run from where docker-compose commands make sense,
# or DOCKER_COMPOSE_DIR is set in backup_vars.sh.ENV
# Defaulting to standard structure.
DOCKER_COMPOSE_BASE_DIR="${SCRIPT_DIR}/../../../environments" # Adjust if structure differs
DOCKER_COMPOSE_FILE="${DOCKER_COMPOSE_BASE_DIR}/${ENV}/docker-compose.yml"
COMMON_DOCKER_COMPOSE_FILE="${DOCKER_COMPOSE_BASE_DIR}/common/docker-compose.common.yml"

COMPOSE_FILES_OPTS="-f ${DOCKER_COMPOSE_FILE}"
if [ -f "$COMMON_DOCKER_COMPOSE_FILE" ]; then
    COMPOSE_FILES_OPTS="${COMPOSE_FILES_OPTS} -f ${COMMON_DOCKER_COMPOSE_FILE}"
fi
# Also consider .env file for the specific environment
ENV_FILE_PATH="${DOCKER_COMPOSE_BASE_DIR}/${ENV}/.env"
if [ -f "$ENV_FILE_PATH" ]; then
    # Docker Compose automatically loads .env from the directory of the primary compose file.
    # If running from script dir, may need --env-file option or cd.
    # For simplicity, assume docker-compose handles it or is run from correct context.
    log_info "Using .env file: $ENV_FILE_PATH (if applicable for docker-compose context)"
fi


# Confirmation
CONFIRM_MSG="WARNING: This will restore database '$DFR_DB_NAME' on '$DFR_DB_HOST' from '$DB_BACKUP_FILE_ARG'."
if [ -n "$FILESTORE_BACKUP_FILE_ARG" ]; then
    CONFIRM_MSG="$CONFIRM_MSG \nAnd filestore from '$FILESTORE_BACKUP_FILE_ARG' to '$ODOO_FILESTORE_PATH'."
fi
CONFIRM_MSG="$CONFIRM_MSG \nThis will overwrite existing data and stop/start service '$ODOO_SERVICE_NAME'. Are you sure?"

if ! confirm_action "$CONFIRM_MSG"; then
    log_warning "Restore operation cancelled by user."
    exit 0
fi

# Stop Odoo service
log_info "Stopping Odoo service: $ODOO_SERVICE_NAME..."
# shellcheck disable=SC2086 # We want word splitting for COMPOSE_FILES_OPTS
if docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" stop "$ODOO_SERVICE_NAME"; then
    log_success "Odoo service '$ODOO_SERVICE_NAME' stopped."
else
    log_error "Failed to stop Odoo service '$ODOO_SERVICE_NAME'. Check Docker Compose logs."
    # Ask user if they want to proceed with DB restore anyway
    if ! confirm_action "Failed to stop Odoo. Proceed with database restore anyway?"; then
        log_warning "Restore aborted due to Odoo service stop failure."
        exit 1
    fi
fi

# Restore database
# This assumes pg_dump backup. pg_basebackup restore is significantly different and more complex.
log_info "Starting database restore for '$DFR_DB_NAME' from '$DB_BACKUP_FILE_ARG'..."

TEMP_DB_BACKUP_FILE="$DB_BACKUP_FILE_ARG"
# Decompress if it's a .gz file
if [[ "$DB_BACKUP_FILE_ARG" == *.gz ]]; then
    log_info "Decompressing database backup file..."
    TEMP_DB_BACKUP_FILE_DECOMPRESSED="${DB_BACKUP_FILE_ARG%.gz}"
    if gunzip -k -f "$DB_BACKUP_FILE_ARG"; then # -k to keep original, -f to overwrite if .dump exists
        TEMP_DB_BACKUP_FILE="$TEMP_DB_BACKUP_FILE_DECOMPRESSED"
        log_success "Decompression successful: $TEMP_DB_BACKUP_FILE"
    else
        log_error "Decompression failed for $DB_BACKUP_FILE_ARG."
        # Attempt to start Odoo service back if it was stopped
        # shellcheck disable=SC2086
        docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" start "$ODOO_SERVICE_NAME" || log_warning "Failed to restart Odoo service."
        exit 1
    fi
fi


# Drop/Recreate database (common for pg_dump restores)
log_info "Dropping existing database '$DFR_DB_NAME' (if it exists)..."
if psql -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d postgres -c "DROP DATABASE IF EXISTS \"$DFR_DB_NAME\";"; then
    log_success "Database '$DFR_DB_NAME' dropped (or did not exist)."
else
    log_error "Failed to drop database '$DFR_DB_NAME'."
    # Attempt to start Odoo service back
    # shellcheck disable=SC2086
    docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" start "$ODOO_SERVICE_NAME" || log_warning "Failed to restart Odoo service."
    if [[ "$TEMP_DB_BACKUP_FILE" != "$DB_BACKUP_FILE_ARG" ]]; then rm -f "$TEMP_DB_BACKUP_FILE"; fi # Clean up decompressed file
    exit 1
fi

log_info "Creating new database '$DFR_DB_NAME' with owner '$DFR_DB_USER'..."
if psql -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d postgres -c "CREATE DATABASE \"$DFR_DB_NAME\" OWNER \"$DFR_DB_USER\";"; then
    log_success "Database '$DFR_DB_NAME' created."
else
    log_error "Failed to create database '$DFR_DB_NAME'."
    # Attempt to start Odoo service back
    # shellcheck disable=SC2086
    docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" start "$ODOO_SERVICE_NAME" || log_warning "Failed to restart Odoo service."
    if [[ "$TEMP_DB_BACKUP_FILE" != "$DB_BACKUP_FILE_ARG" ]]; then rm -f "$TEMP_DB_BACKUP_FILE"; fi
    exit 1
fi

# Determine restore command based on file type (simple check)
RESTORE_SUCCESS=false
if file "$TEMP_DB_BACKUP_FILE" | grep -q 'PostgreSQL custom database dump'; then
    log_info "Restoring using pg_restore (custom format)..."
    if pg_restore -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" --no-owner --no-privileges --clean --if-exists "$TEMP_DB_BACKUP_FILE"; then
        RESTORE_SUCCESS=true
    fi
elif file "$TEMP_DB_BACKUP_FILE" | grep -q 'PostgreSQL tar database dump'; then
    log_info "Restoring using pg_restore (tar format)..."
    if pg_restore -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" --no-owner --no-privileges --clean --if-exists "$TEMP_DB_BACKUP_FILE"; then
        RESTORE_SUCCESS=true
    fi
elif file "$TEMP_DB_BACKUP_FILE" | grep -qE 'ASCII text|SQL'; then # Simple check for plain SQL
    log_info "Restoring using psql (plain SQL format)..."
    if psql -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" -f "$TEMP_DB_BACKUP_FILE"; then
        RESTORE_SUCCESS=true
    fi
else
    log_warning "Could not determine backup file type from content. Attempting pg_restore..."
    if pg_restore -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" --no-owner --no-privileges --clean --if-exists "$TEMP_DB_BACKUP_FILE"; then
        RESTORE_SUCCESS=true
    else
      log_warning "pg_restore failed. Trying psql..."
      if psql -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" -f "$TEMP_DB_BACKUP_FILE"; then
          RESTORE_SUCCESS=true
      fi
    fi
fi

if [[ "$TEMP_DB_BACKUP_FILE" != "$DB_BACKUP_FILE_ARG" ]]; then
    rm -f "$TEMP_DB_BACKUP_FILE" # Clean up decompressed file
fi

if $RESTORE_SUCCESS; then
    log_success "Database restore successful for '$DFR_DB_NAME'."
else
    log_error "Database restore failed for '$DFR_DB_NAME'."
    # Attempt to start Odoo service back
    # shellcheck disable=SC2086
    docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" start "$ODOO_SERVICE_NAME" || log_warning "Failed to restart Odoo service."
    exit 1
fi

# Restore filestore
if [ -n "$FILESTORE_BACKUP_FILE_ARG" ]; then
    if [ -z "$ODOO_FILESTORE_PATH" ]; then
        log_warning "FILESTORE_BACKUP_FILE provided, but ODOO_FILESTORE_PATH is not set in config. Skipping filestore restore."
    else
        log_info "Restoring filestore from '$FILESTORE_BACKUP_FILE_ARG' to '$ODOO_FILESTORE_PATH'..."
        # Ensure filestore parent directory exists
        FILESTORE_PARENT_DIR=$(dirname "$ODOO_FILESTORE_PATH")
        mkdir -p "$FILESTORE_PARENT_DIR"

        # Remove existing filestore content (if any)
        if [ -d "$ODOO_FILESTORE_PATH" ]; then
            log_info "Removing existing filestore content at $ODOO_FILESTORE_PATH..."
            rm -rf "${ODOO_FILESTORE_PATH:?}"/* # Protect against empty ODOO_FILESTORE_PATH
        else
            mkdir -p "$ODOO_FILESTORE_PATH"
        fi
        
        # Extract filestore backup
        # Assuming tar.gz. Adjust if other formats are used.
        # -C changes directory for extraction to target path.
        # Tar archives created with -C during backup should restore correctly.
        # If backup was `tar -czf backup.tar.gz /path/to/filestore/DB_NAME`, then extract to parent of `DB_NAME` dir.
        # If backup was `tar -czf backup.tar.gz -C /path/to/filestore DB_NAME`, then extract to `/path/to/filestore`.
        # The backup script uses `tar -czf target_path -C PARENT_DIR_FILESTORE DIR_TO_BACKUP_FILESTORE`
        # So, we should extract to PARENT_DIR_FILESTORE
        
        if tar -xzf "$FILESTORE_BACKUP_FILE_ARG" -C "$FILESTORE_PARENT_DIR"; then
            log_success "Filestore restore successful to $ODOO_FILESTORE_PATH."
        else
            log_error "Filestore restore failed from '$FILESTORE_BACKUP_FILE_ARG'."
            # This might leave system in inconsistent state. User should check.
        fi
    fi
fi

# Start Odoo service
log_info "Starting Odoo service: $ODOO_SERVICE_NAME..."
# shellcheck disable=SC2086
if docker-compose ${COMPOSE_FILES_OPTS} --project-directory "${DOCKER_COMPOSE_BASE_DIR}/${ENV}" start "$ODOO_SERVICE_NAME"; then
    log_success "Odoo service '$ODOO_SERVICE_NAME' started."
else
    log_error "Failed to start Odoo service '$ODOO_SERVICE_NAME'. Check Docker Compose logs."
    # The restore might be complete but service failed to start.
fi

# Unset PGPASSWORD
unset PGPASSWORD

log_success "DFR Restore process completed for environment '$ENV'."