#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status.

# This script is executed by the official postgres container entrypoint
# when the container starts for the first time and the data directory is empty.
# Environment variables like POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
# are available and the database/user specified by them would have been created
# by the main entrypoint script already.

# DFR_APP_DB: The database Odoo will connect to.
# DFR_APP_USER: The user Odoo will use to connect.
# If these are not set, they default to POSTGRES_DB and POSTGRES_USER respectively.
DFR_APP_DB="${DFR_APP_DB:-${POSTGRES_DB}}"
DFR_APP_USER="${DFR_APP_USER:-${POSTGRES_USER}}"
# DFR_APP_PASSWORD is not explicitly used here as the user should already exist.

echo "Running custom initialization script: 01_init_user_db.sh"
echo "Target database for extensions: ${DFR_APP_DB}"
echo "Operating as PostgreSQL user: ${POSTGRES_USER}"

# Enable required extensions in the DFR application database.
# The database DFR_APP_DB should already exist (created by postgres main entrypoint
# if it matches POSTGRES_DB, or needs to be created if DFR_APP_DB is different
# and POSTGRES_DB was something else like 'postgres').
# Assuming DFR_APP_DB is the one Odoo will use and is targeted by POSTGRES_DB.

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DFR_APP_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    COMMENT ON EXTENSION "uuid-ossp" IS 'Standard UUID functions';

    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    COMMENT ON EXTENSION "pgcrypto" IS 'Cryptographic functions (e.g., for password hashing if Odoo uses it, or field encryption)';

    -- Example for PostGIS if geospatial features are needed for DFR:
    -- CREATE EXTENSION IF NOT EXISTS postgis;
    -- CREATE EXTENSION IF NOT EXISTS postgis_topology;
    -- COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';

    -- You can add other database setup tasks here, like:
    -- ALTER DATABASE ${DFR_APP_DB} OWNER TO ${DFR_APP_USER}; -- If DFR_APP_USER is different and needs ownership
    -- GRANT ALL PRIVILEGES ON DATABASE ${DFR_APP_DB} TO ${DFR_APP_USER}; -- If needed
EOSQL

echo "Successfully enabled required PostgreSQL extensions (uuid-ossp, pgcrypto) in database '${DFR_APP_DB}'."

# If DFR_APP_USER and DFR_APP_DB are different from POSTGRES_USER and POSTGRES_DB,
# and they need to be created by this script:
#
# if [ "$DFR_APP_USER" != "$POSTGRES_USER" ] || [ "$DFR_APP_DB" != "$POSTGRES_DB" ]; then
#   echo "Attempting to create DFR-specific user and/or database."
#   DFR_APP_PASSWORD_TO_USE="${DFR_APP_PASSWORD:-${POSTGRES_PASSWORD}}" # Fallback, but DFR_APP_PASSWORD should be set
#
#   psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
#     DO \$\$
#     BEGIN
#       IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '${DFR_APP_USER}') THEN
#         CREATE USER ${DFR_APP_USER} WITH PASSWORD '${DFR_APP_PASSWORD_TO_USE}';
#         RAISE NOTICE 'User ${DFR_APP_USER} created.';
#       ELSE
#         RAISE NOTICE 'User ${DFR_APP_USER} already exists.';
#       END IF;
#     END
#     \$\$;
#
#     SELECT 'CREATE DATABASE ${DFR_APP_DB} OWNER ${DFR_APP_USER}'
#     WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DFR_APP_DB}');
#     -- The actual CREATE DATABASE needs to be run outside a transaction block if it might fail an `EXISTS` check in the same command.
#     -- Or connect to 'template1' to create DB.
#     -- A simpler approach if POSTGRES_DB is 'postgres':
#     -- CREATE DATABASE ${DFR_APP_DB} OWNER ${DFR_APP_USER}; -- This might fail if it exists.
#     -- GRANT ALL PRIVILEGES ON DATABASE ${DFR_APP_DB} TO ${DFR_APP_USER};
#   EOSQL
#   echo "DFR specific user/db setup attempted. Check logs for details."
# fi

echo "Custom initialization script 01_init_user_db.sh finished."