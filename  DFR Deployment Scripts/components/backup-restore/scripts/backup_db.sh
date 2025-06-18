#!/bin/bash
set -e
set -o pipefail

# Script to perform PostgreSQL database backup for DFR
# Sources configuration from backup_vars.sh.ENV

# Determine script's directory to source utils.sh reliably
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
UTILS_SCRIPT_PATH="${SCRIPT_DIR}/../../shared/scripts/utils.sh"
DOCKER_HELPERS_SCRIPT_PATH="${SCRIPT_DIR}/../../shared/scripts/docker_helpers.sh" # Not strictly needed for backup, but good practice

if [ ! -f "$UTILS_SCRIPT_PATH" ]; then
    echo "Error: utils.sh not found at $UTILS_SCRIPT_PATH"
    exit 1
fi
# shellcheck source=../../shared/scripts/utils.sh
source "$UTILS_SCRIPT_PATH"

# Expect ENV to be set externally (e.g., by Makefile or cron job environment)
if [ -z "$ENV" ]; then
    log_error "Environment variable ENV is not set. Please set ENV (e.g., development, staging, production)."
    exit 1
fi

CONFIG_FILE_PATH="${SCRIPT_DIR}/../config/backup_vars.sh.${ENV}"
if [ ! -f "$CONFIG_FILE_PATH" ]; then
    log_error "Backup configuration file $CONFIG_FILE_PATH not found for environment '$ENV'."
    exit 1
fi
# shellcheck source=../config/backup_vars.sh.template
source "$CONFIG_FILE_PATH"
log_info "Loaded backup configuration from $CONFIG_FILE_PATH for environment '$ENV'."

# Validate required variables
REQUIRED_VARS=("DFR_DB_HOST" "DFR_DB_PORT" "DFR_DB_USER" "DFR_DB_NAME" "BACKUP_DIR" "BACKUP_METHOD")
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


# Prepare backup directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TARGET_BACKUP_SUBDIR="${BACKUP_DIR}/${TIMESTAMP}"
mkdir -p "$TARGET_BACKUP_SUBDIR"
log_info "Created backup directory: $TARGET_BACKUP_SUBDIR"

# Perform database backup
BACKUP_FILENAME_DB="dfr_db_${TIMESTAMP}"
BACKUP_FILE_DB_FULL_PATH=""

log_info "Starting database backup using method: $BACKUP_METHOD"
case "$BACKUP_METHOD" in
    pg_dump)
        FORMAT_OPT=""
        FORMAT_EXT="dump" # Default for custom format
        PG_DUMP_FORMAT_EFFECTIVE="${PG_DUMP_FORMAT:-c}" # Default to custom if not set

        case "$PG_DUMP_FORMAT_EFFECTIVE" in
            c|custom)
                FORMAT_OPT="-Fc"
                FORMAT_EXT="dump"
                ;;
            p|plain)
                FORMAT_OPT="-Fp"
                FORMAT_EXT="sql"
                ;;
            t|tar)
                FORMAT_OPT="-Ft"
                FORMAT_EXT="tar"
                ;;
            *)
                log_warning "Invalid PG_DUMP_FORMAT '$PG_DUMP_FORMAT_EFFECTIVE'. Defaulting to custom format."
                FORMAT_OPT="-Fc"
                FORMAT_EXT="dump"
                ;;
        esac
        BACKUP_FILENAME_DB="${BACKUP_FILENAME_DB}.${FORMAT_EXT}"
        BACKUP_FILE_DB_FULL_PATH="${TARGET_BACKUP_SUBDIR}/${BACKUP_FILENAME_DB}"

        log_info "Running pg_dump: Host=${DFR_DB_HOST}, Port=${DFR_DB_PORT}, User=${DFR_DB_USER}, DB=${DFR_DB_NAME}, Format=${PG_DUMP_FORMAT_EFFECTIVE}"
        if pg_dump -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -d "$DFR_DB_NAME" "$FORMAT_OPT" -f "$BACKUP_FILE_DB_FULL_PATH"; then
            log_success "Database dump successful: $BACKUP_FILE_DB_FULL_PATH"
        else
            log_error "pg_dump failed. Check logs."
            # Clean up partial backup directory
            rm -rf "$TARGET_BACKUP_SUBDIR" 
            exit 1
        fi

        # Optional compression for plain or tar format if COMPRESS_BACKUP is true
        if [[ "$COMPRESS_BACKUP" == "true" ]] && ([[ "$PG_DUMP_FORMAT_EFFECTIVE" == "p" ]] || [[ "$PG_DUMP_FORMAT_EFFECTIVE" == "t" ]]); then
            log_info "Compressing database dump $BACKUP_FILE_DB_FULL_PATH..."
            if gzip "$BACKUP_FILE_DB_FULL_PATH"; then
                BACKUP_FILE_DB_FULL_PATH="${BACKUP_FILE_DB_FULL_PATH}.gz"
                log_success "Compression successful: $BACKUP_FILE_DB_FULL_PATH"
            else
                log_error "Compression failed for $BACKUP_FILE_DB_FULL_PATH."
                # Proceed with uncompressed backup
            fi
        elif [[ "$COMPRESS_BACKUP" == "true" ]] && [[ "$PG_DUMP_FORMAT_EFFECTIVE" == "c" ]]; then
            log_info "pg_dump custom format is already compressed. Skipping explicit gzip."
        fi
        ;;
    pg_basebackup)
        # pg_basebackup is more complex for simple backups, often used for PITR setups.
        # Requires specific PostgreSQL configuration (e.g., archive_mode, wal_level).
        log_info "Running pg_basebackup: Host=${DFR_DB_HOST}, Port=${DFR_DB_PORT}, User=${DFR_DB_USER}"
        BACKUP_FILE_DB_FULL_PATH="${TARGET_BACKUP_SUBDIR}/db_basebackup" # This will be a directory
        # -Ft: tar format, -X stream: stream WAL files, -P: progress, -R: create recovery files
        if pg_basebackup -h "$DFR_DB_HOST" -p "$DFR_DB_PORT" -U "$DFR_DB_USER" -D "$BACKUP_FILE_DB_FULL_PATH" -Ft -X stream -P -R; then
            log_success "pg_basebackup successful: $BACKUP_FILE_DB_FULL_PATH"
            if [[ "$COMPRESS_BACKUP" == "true" ]]; then
                 log_info "Compressing base backup directory..."
                 # pg_basebackup output for -Ft is multiple tar files (base.tar, pg_wal.tar)
                 # Compressing the whole directory might be better or compress individual tars
                 if tar -czf "${BACKUP_FILE_DB_FULL_PATH}.tar.gz" -C "$(dirname "$BACKUP_FILE_DB_FULL_PATH")" "$(basename "$BACKUP_FILE_DB_FULL_PATH")"; then
                    log_success "Base backup directory compressed to ${BACKUP_FILE_DB_FULL_PATH}.tar.gz"
                    rm -rf "$BACKUP_FILE_DB_FULL_PATH" # Remove original directory
                    BACKUP_FILE_DB_FULL_PATH="${BACKUP_FILE_DB_FULL_PATH}.tar.gz"
                 else
                    log_error "Compression of base backup directory failed."
                 fi
            fi
        else
            log_error "pg_basebackup failed. Check logs."
            rm -rf "$TARGET_BACKUP_SUBDIR"
            exit 1
        fi
        ;;
    *)
        log_error "Unsupported BACKUP_METHOD: $BACKUP_METHOD. Supported methods are 'pg_dump', 'pg_basebackup'."
        rm -rf "$TARGET_BACKUP_SUBDIR"
        exit 1
        ;;
esac

# Backup filestore (if ODOO_FILESTORE_PATH is set)
FILESTORE_BACKUP_FILE_FULL_PATH=""
if [ -n "$ODOO_FILESTORE_PATH" ]; then
    if [ -d "$ODOO_FILESTORE_PATH" ]; then
        BACKUP_FILENAME_FS="dfr_filestore_${TIMESTAMP}.tar.gz"
        FILESTORE_BACKUP_FILE_FULL_PATH="${TARGET_BACKUP_SUBDIR}/${BACKUP_FILENAME_FS}"
        log_info "Backing up Odoo filestore from $ODOO_FILESTORE_PATH to $FILESTORE_BACKUP_FILE_FULL_PATH..."
        # Using -C to change directory to avoid leading paths in tar archive.
        # Example: tar -czf archive.tar.gz -C /path/to/filestore .
        PARENT_DIR_FILESTORE=$(dirname "$ODOO_FILESTORE_PATH")
        DIR_TO_BACKUP_FILESTORE=$(basename "$ODOO_FILESTORE_PATH")

        if tar -czf "$FILESTORE_BACKUP_FILE_FULL_PATH" -C "$PARENT_DIR_FILESTORE" "$DIR_TO_BACKUP_FILESTORE"; then
            log_success "Filestore backup successful: $FILESTORE_BACKUP_FILE_FULL_PATH"
        else
            log_error "Filestore backup failed for $ODOO_FILESTORE_PATH."
            # Decide if this is a critical failure. For now, continue but log error.
        fi
    else
        log_warning "ODOO_FILESTORE_PATH '$ODOO_FILESTORE_PATH' is set but is not a valid directory. Skipping filestore backup."
    fi
else
    log_info "ODOO_FILESTORE_PATH is not set. Skipping filestore backup."
fi

# Cleanup old backups
# Using RETENTION_DAYS which should be defined in backup_vars.sh.ENV
# The template has RETENTION_DAYS_DAILY etc. Using a generic one here as per SDS 4.5.1
# Assume RETENTION_DAYS is the primary one, e.g. RETENTION_DAYS="${RETENTION_DAYS_DAILY}"
RETENTION_POLICY_DAYS="${RETENTION_DAYS:-${RETENTION_DAYS_DAILY:-7}}" # Default to 7 days if not set

if [[ "$RETENTION_POLICY_DAYS" -gt 0 ]]; then
    log_info "Cleaning up backups older than $RETENTION_POLICY_DAYS days in $BACKUP_DIR..."
    # Use find to delete directories (each backup is in its own timestamped dir)
    # The -mindepth 1 and -maxdepth 1 ensure we only look at the timestamped subdirs
    # The -type d ensures we only delete directories
    # The -mtime +N means older than N days (N*24 hours ago)
    # Ensure BACKUP_DIR itself is not deleted if it matches name pattern by mistake
    find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d -mtime "+$((RETENTION_POLICY_DAYS - 1))" -exec rm -rf {} \;
    log_success "Old backup cleanup finished."
else
    log_info "Backup retention policy is not set or is zero. Skipping cleanup."
fi

# Unset PGPASSWORD
unset PGPASSWORD

log_success "DFR Backup process completed for environment '$ENV'."
if [ -n "$BACKUP_FILE_DB_FULL_PATH" ]; then
    log_info "Database backup stored at: $BACKUP_FILE_DB_FULL_PATH"
fi
if [ -n "$FILESTORE_BACKUP_FILE_FULL_PATH" ]; then
    log_info "Filestore backup stored at: $FILESTORE_BACKUP_FILE_FULL_PATH"
fi