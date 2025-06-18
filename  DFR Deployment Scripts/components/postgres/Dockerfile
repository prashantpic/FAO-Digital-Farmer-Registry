FROM postgres:16-alpine

# Copy custom initialization scripts
# Scripts in /docker-entrypoint-initdb.d are run if /var/lib/postgresql/data is empty
COPY ./initdb.d/01_init_user_db.sh /docker-entrypoint-initdb.d/01_init_user_db.sh
RUN chmod +x /docker-entrypoint-initdb.d/01_init_user_db.sh

# No need to install pgcrypto or uuid-ossp via apk if they are part of postgresql package
# and can be enabled via CREATE EXTENSION by the init script.
# If other specific extensions like PostGIS were needed and not available by default,
# one might need to install packages like `postgresql-contrib` or `postgis`.
# For Alpine, this would be `apk add postgresql16-contrib` if such a package exists
# and provides the needed extensions. The 01_init_user_db.sh script handles enabling.

EXPOSE 5432