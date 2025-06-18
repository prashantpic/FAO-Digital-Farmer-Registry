# Software Design Specification: DFR Deployment Scripts

## 1. Introduction

### 1.1 Purpose
This document outlines the design and specifications for the `DFR_DEPLOYMENT_SCRIPTS` repository. This repository is responsible for providing all necessary scripts, Dockerfiles, configuration templates, and orchestration files (e.g., Docker Compose) to build, deploy, manage, and maintain the Digital Farmer Registry (DFR) system across various environments (Development, Staging, Production). This includes containerizing application components, automating deployment processes, and facilitating operational tasks such as database backup and restore.

### 1.2 Scope
The scope of this repository covers:
*   Dockerization of DFR components: Odoo application server, PostgreSQL database server, and Nginx reverse proxy.
*   Orchestration of these components using Docker Compose for different environments.
*   Configuration templates for each component and environment.
*   Scripts for database backup and restore operations.
*   Utility scripts to support deployment and operational tasks.
*   A Makefile to orchestrate common build, deployment, and operational commands.
*   Versioning for the deployment scripts themselves.

Kubernetes manifests and Ansible playbooks are considered optional extensions and will be specified if and when a decision is made to adopt these technologies for more complex deployments.

### 1.3 Intended Audience
This document is intended for:
*   **DevOps Engineers/System Administrators:** Responsible for deploying, managing, and maintaining the DFR system.
*   **Developers:** To understand how the application is built, configured, and deployed, enabling them to set up local development environments.
*   **FAO and National IT Teams:** Who will eventually take ownership and manage the DFR instances in their respective countries.

## 2. Design Considerations

### 2.1 Environment Agnosticism
Scripts and configurations will be designed to be as environment-agnostic as possible, relying on environment variables and configuration templates to adapt to specific deployment targets (Development, Staging, Production, and different country instances).

### 2.2 Security
*   Sensitive information (passwords, API keys) will be managed through environment variables or secure configuration files, never hardcoded into scripts or Docker images. Templates will indicate where secrets are required.
*   Docker images will be built from official, trusted base images where possible.
*   Nginx will be configured for HTTPS termination, enforcing secure communication.
*   Backup files will be handled securely, with consideration for encryption and secure storage locations.

### 2.3 Configurability
*   Key parameters for Odoo, PostgreSQL, Nginx, and backup/restore operations will be configurable via environment variables or dedicated configuration files.
*   Templates will be used extensively to allow easy customization for each environment or country instance.

### 2.4 Reproducibility and Consistency
*   Dockerization ensures that the application runs in a consistent environment across all deployment stages.
*   Version control for all scripts and configuration templates ensures reproducibility and traceability of changes.

### 2.5 Simplicity and Maintainability
*   Scripts will be well-commented and structured for clarity.
*   A Makefile will provide a simple interface for common operations.
*   Shared utility scripts will promote code reuse and reduce redundancy.

### 2.6 Idempotency
Deployment and configuration scripts should aim for idempotency where practical, meaning they can be run multiple times with the same outcome without causing unintended side effects.

## 3. System Architecture Overview
The deployment architecture relies on containerization using Docker and orchestration using Docker Compose. The key components are:
*   **Odoo Application Server:** Runs the DFR custom addons and Odoo core.
*   **PostgreSQL Database Server:** Persists all DFR data.
*   **Nginx Reverse Proxy:** Handles incoming web traffic, provides HTTPS termination, and load balances (if multiple Odoo workers are configured).

These components will run in separate Docker containers, linked via a Docker network. Each environment (Dev, Staging, Prod) will have its own Docker Compose setup, potentially sharing common configurations.

## 4. Detailed Design Specifications

### 4.1 Root Directory

#### 4.1.1 `Makefile`
*   **Purpose:** Main entry point for orchestrating common deployment, build, and operational tasks.
*   **Implementation Details:**
    *   Uses standard Makefile syntax.
    *   Targets will delegate to shell scripts located in specific component or environment directories.
    *   Environment variables (e.g., `ENV=staging`, `COUNTRY=vu`) can be passed to `make` commands to target specific deployments if scripts are designed to handle them.
*   **Key Targets:**
    *   `build_odoo`: Builds the Odoo Docker image.
        *   Logic: Navigates to `components/odoo/` and runs `docker build`.
    *   `build_postgres`: Builds the PostgreSQL Docker image (if custom, otherwise pulls).
        *   Logic: Navigates to `components/postgres/` and runs `docker build`.
    *   `build_nginx`: Builds the Nginx Docker image.
        *   Logic: Navigates to `components/nginx/` and runs `docker build`.
    *   `build_all_images`: Builds all necessary Docker images.
        *   Logic: Calls `build_odoo`, `build_postgres`, `build_nginx`.
    *   `deploy_dev`: Deploys the development environment.
        *   Logic: Navigates to `environments/development/`, ensures `.env` exists (from `.env.template`), and runs `docker-compose up -d --build`.
    *   `deploy_staging`: Deploys the staging environment.
        *   Logic: Similar to `deploy_dev`, but for `environments/staging/` and using `staging.env` or equivalent. Requires pre-configuration of staging-specific variables.
    *   `deploy_production`: Deploys the production environment.
        *   Logic: Similar to `deploy_staging`, but for `environments/production/` and using production-specific variables. Emphasize secure handling of production environment variables.
    *   `stop_dev`, `stop_staging`, `stop_production`: Stops the respective environments.
        *   Logic: Navigates to the environment directory and runs `docker-compose down`.
    *   `logs_dev`, `logs_staging`, `logs_production`: Tails logs for the respective environments.
        *   Logic: Navigates to the environment directory and runs `docker-compose logs -f`.
    *   `backup_db_prod`: Triggers a database backup for the production environment.
        *   Logic: Executes `components/backup-restore/scripts/backup_db.sh` with production configuration. Requires `components/backup-restore/config/backup_vars.sh.production` to be configured.
    *   `restore_db_staging BACKUP_FILE=<path_to_backup_file>`: Restores a database backup to the staging environment.
        *   Logic: Executes `components/backup-restore/scripts/restore_db.sh` with staging configuration and the specified `BACKUP_FILE`. Requires `components/backup-restore/config/backup_vars.sh.staging` to be configured.
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006, REQ-DIO-007, B.2.2.9, B.3.B1.11.

#### 4.1.2 `VERSION`
*   **Purpose:** Tracks the version of the deployment scripts repository.
*   **Implementation Details:**
    *   Plain text file.
    *   Contains a Semantic Version string (e.g., `1.0.0`).
    *   Updated manually or via CI/CD script upon release of new deployment script versions.
*   **Requirements Mapping:** B.3.B1.11.

### 4.2 Component: Odoo (`components/odoo/`)

#### 4.2.1 `Dockerfile`
*   **Purpose:** Defines the DFR Odoo application server Docker image.
*   **Base Image:** `odoo:18.0` (or the specific minor/patch version of Odoo 18.0 CE being targeted).
*   **Key Steps:**
    1.  Set `DEBIAN_FRONTEND=noninteractive` argument.
    2.  Update package lists and install system dependencies:
        *   `wkhtmltopdf` (for PDF reports).
        *   `python3-pip`, `python3-dev`, `build-essential`, `libxml2-dev`, `libxslt1-dev`, `zlib1g-dev`, `libsasl2-dev`, `libldap2-dev`, `libssl-dev`, `libffi-dev`, `postgresql-client` (for `psql` utility if needed).
        *   Any other OS-level packages required by DFR custom addons or their Python dependencies.
    3.  Copy `requirements.txt` (if any specific Python dependencies beyond Odoo's are needed for custom addons) and install them using `pip3 install -r requirements.txt`.
        *   `requirements.txt` should list specific versions.
    4.  Create `/mnt/extra-addons` directory.
        *   Note: DFR custom addons will be mounted as a volume in Docker Compose to this path for development and copied during production image builds if a separate production Dockerfile variant is used or if addons are part of the image. For simplicity, this SDS assumes addons are mounted for dev/staging and could be baked in for production via a CI step or multi-stage build.
    5.  Copy `components/odoo/entrypoint.sh` to `/usr/local/bin/dfr_entrypoint.sh` and make it executable.
    6.  Copy `components/odoo/config/odoo.conf.template` to `/etc/odoo/odoo.conf.template`.
    7.  Set appropriate user and group (e.g., `odoo`).
    8.  Expose Odoo port (default `8069`).
    9.  Set `ENTRYPOINT ["/usr/local/bin/dfr_entrypoint.sh"]`.
    10. Set `CMD ["odoo"]`.
*   **Build Arguments:**
    *   Potentially `ODOO_VERSION` if base image tag needs to be dynamic.
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006, B.2.2.9, B.3.B1.11.

#### 4.2.2 `entrypoint.sh`
*   **Purpose:** Container startup script for the Odoo application.
*   **Implementation Details:**
    *   Shell script (Bash).
    *   Sources `shared/scripts/utils.sh` for logging.
    1.  **Wait for PostgreSQL:** Implement a loop to check PostgreSQL connectivity using `pg_isready` or `psql` before proceeding.
        *   Parameters: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD_FILE` (or `DB_PASSWORD`).
        *   Timeout and retry mechanism.
    2.  **Configuration Generation:**
        *   Copy `/etc/odoo/odoo.conf.template` to `/etc/odoo/odoo.conf`.
        *   Substitute placeholders in `/etc/odoo/odoo.conf` using environment variables (e.g., `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `ODOO_ADMIN_PASSWD`, `ODOO_WORKERS`, `ODOO_ADDONS_PATH`).
        *   `ODOO_ADDONS_PATH` should include Odoo's default addons path and `/mnt/extra-addons`.
    3.  **Database Initialization/Update (Optional in entrypoint, can be manual step):**
        *   Check if the database specified by `DB_NAME` exists.
        *   If `ODOO_AUTO_INIT_DB` is true and DB does not exist or `ODOO_AUTO_UPDATE_MODULES` is true:
            *   Construct Odoo command: `odoo -c /etc/odoo/odoo.conf -d $DB_NAME --init=$ODOO_MODULES_TO_INIT_OR_UPDATE --update=$ODOO_MODULES_TO_INIT_OR_UPDATE --stop-after-init` (or similar flags for initialization vs. update).
            *   `$ODOO_MODULES_TO_INIT_OR_UPDATE` could be a comma-separated list of DFR modules.
    4.  **Start Odoo Server:**
        *   Execute the original Odoo entrypoint or directly run `odoo -c /etc/odoo/odoo.conf "$@"`. `"$@"` passes CMD from Dockerfile.
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006.

#### 4.2.3 `config/odoo.conf.template`
*   **Purpose:** Template for Odoo server configuration.
*   **Key Placeholders/Variables (to be substituted by `entrypoint.sh` from environment variables):**
    *   `admin_passwd = {{ODOO_ADMIN_PASSWD}}`
    *   `db_host = {{ODOO_DB_HOST}}`
    *   `db_port = {{ODOO_DB_PORT}}`
    *   `db_user = {{ODOO_DB_USER}}`
    *   `db_password = {{ODOO_DB_PASSWORD}}`
    *   `addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons` (or actual Odoo standard path)
    *   `workers = {{ODOO_WORKERS | default(0)}}` (0 for cron/dev, >0 for HTTP workers)
    *   `limit_time_cpu = {{ODOO_LIMIT_TIME_CPU | default(600)}}`
    *   `limit_time_real = {{ODOO_LIMIT_TIME_REAL | default(1200)}}`
    *   `proxy_mode = True` (if Nginx is used)
    *   `log_level = {{ODOO_LOG_LEVEL | default("info")}}`
    *   `list_db = {{ODOO_LIST_DB | default("True")}}` (Set to False in production)
    *   `data_dir = /var/lib/odoo`
*   **Requirements Mapping:** REQ-DIO-006.

### 4.3 Component: PostgreSQL (`components/postgres/`)

#### 4.3.1 `Dockerfile`
*   **Purpose:** Defines the DFR PostgreSQL database server Docker image.
*   **Base Image:** `postgres:16-alpine` (or latest stable `postgres:16` variant, aligning with Odoo 18 requirements). Alpine is preferred for smaller image size.
*   **Key Steps:**
    1.  Copy custom initialization scripts (e.g., `components/postgres/initdb.d/01_init_user_db.sh`) to `/docker-entrypoint-initdb.d/`.
    2.  (Optional) Install PostgreSQL extensions if needed by DFR (e.g., `pgcrypto` if not already included, PostGIS if REQ-FHR-005 requires advanced spatial queries). This might require switching to a Debian-based Postgres image if Alpine makes extension installation difficult.
        *   Example for Debian-based: `RUN apt-get update && apt-get install -y postgresql-contrib-XX`
    3.  Expose PostgreSQL port (default `5432`).
*   **Environment Variables (Standard PostgreSQL image variables):**
    *   `POSTGRES_USER`
    *   `POSTGRES_PASSWORD`
    *   `POSTGRES_DB`
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006, B.2.2.9.

#### 4.3.2 `initdb.d/01_init_user_db.sh`
*   **Purpose:** Initializes the DFR database and user on first container start.
*   **Implementation Details:**
    *   Shell script (Bash or `sh` for Alpine).
    *   Uses `psql` command-line utility.
    *   Leverages environment variables passed to the PostgreSQL container (`POSTGRES_USER`, `POSTGRES_DB`).
    bash
    #!/bin/sh
    set -e # Exit immediately if a command exits with a non-zero status.

    # The standard postgres entrypoint script will have already created POSTGRES_USER
    # and POSTGRES_DB if they were specified and the database cluster was new.
    # This script can be used for additional setup, e.g., creating more users or databases,
    # or granting specific privileges if the DFR_APP_USER is different from POSTGRES_USER.

    DFR_APP_USER="${DFR_APP_USER:-${POSTGRES_USER}}" # Use POSTGRES_USER if DFR_APP_USER not set
    DFR_APP_DB="${DFR_APP_DB:-${POSTGRES_DB}}"     # Use POSTGRES_DB if DFR_APP_DB not set
    DFR_APP_PASSWORD="${DFR_APP_PASSWORD:-${POSTGRES_PASSWORD}}" # For DFR_APP_USER if different

    # Example: If DFR needs a separate user/db than the initial superuser/db
    # psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    #     CREATE USER ${DFR_APP_USER} WITH PASSWORD '${DFR_APP_PASSWORD}';
    #     CREATE DATABASE ${DFR_APP_DB} OWNER ${DFR_APP_USER};
    #     GRANT ALL PRIVILEGES ON DATABASE ${DFR_APP_DB} TO ${DFR_APP_USER};
    # EOSQL
    # echo "DFR user ${DFR_APP_USER} and database ${DFR_APP_DB} created."

    # If POSTGRES_USER and POSTGRES_DB are used directly by Odoo, this script might
    # only be needed for enabling extensions.
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DFR_APP_DB" <<-EOSQL
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- For potential field-level encryption
        -- Add other extensions like PostGIS if needed:
        -- CREATE EXTENSION IF NOT EXISTS postgis;
        -- CREATE EXTENSION IF NOT EXISTS postgis_topology;
    EOSQL
    echo "Required PostgreSQL extensions enabled in database ${DFR_APP_DB}."
    
*   **Requirements Mapping:** REQ-DIO-006.

### 4.4 Component: Nginx (`components/nginx/`)

#### 4.4.1 `Dockerfile`
*   **Purpose:** Defines the Nginx reverse proxy Docker image.
*   **Base Image:** `nginx:stable-alpine` (or latest stable).
*   **Key Steps:**
    1.  Remove default Nginx configuration: `RUN rm /etc/nginx/conf.d/default.conf`.
    2.  Copy custom main Nginx configuration template: `COPY components/nginx/config/nginx.conf.template /etc/nginx/nginx.conf.template`.
    3.  Copy DFR site configuration template: `COPY components/nginx/config/sites-available/dfr.conf.template /etc/nginx/sites-available/dfr.conf.template`.
    4.  (Optional) Copy custom SSL parameter snippets (e.g., for DH params, recommended ciphers) if not managed via certbot or similar on the host.
    5.  Create `/etc/nginx/ssl/` directory (certificates will be mounted here).
    6.  Copy an entrypoint script (`nginx_entrypoint.sh`) if dynamic configuration substitution is needed, otherwise Nginx can start directly.
    7.  Expose ports `80` and `443`.
    8.  If using an entrypoint: `ENTRYPOINT ["/usr/local/bin/nginx_entrypoint.sh"]`, `CMD ["nginx", "-g", "daemon off;"]`. Otherwise `CMD ["nginx", "-g", "daemon off;"]`.
*   **Requirements Mapping:** B.2.2.9.

#### 4.4.2 `nginx_entrypoint.sh` (Optional, if config substitution is needed at runtime)
*   **Purpose:** Prepares Nginx configuration files by substituting environment variables.
*   **Implementation Details:**
    *   Shell script (Bash or `sh`).
    1.  Copy template files to actual config locations (e.g., `/etc/nginx/nginx.conf.template` to `/etc/nginx/nginx.conf`).
    2.  Use `envsubst` or `sed` to replace placeholders (e.g., `{{NGINX_SERVER_NAME}}`, `{{ODOO_APP_SERVICE_HOST}}`, `{{ODOO_APP_SERVICE_PORT}}`) in configuration files with values from environment variables.
    3.  Create symlink from `sites-available/dfr.conf` to `sites-enabled/dfr.conf`.
    4.  Execute the original Nginx command: `exec nginx -g 'daemon off;'`.

#### 4.4.3 `config/nginx.conf.template`
*   **Purpose:** Template for the main Nginx configuration.
*   **Key Content:**
    nginx
    user nginx;
    worker_processes auto; # Or {{NGINX_WORKER_PROCESSES | default('auto')}}
    pid /var/run/nginx.pid;
    include /etc/nginx/modules-enabled/*.conf;

    events {
        worker_connections {{NGINX_WORKER_CONNECTIONS | default(1024)}};
    }

    http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off; # Recommended for production

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ssl_protocols TLSv1.2 TLSv1.3; # REQ-DIO-005
        ssl_prefer_server_ciphers off; # Modern clients select best

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip on;
        gzip_vary on;
        gzip_proxied any;
        gzip_comp_level 6;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
    }
    
*   **Requirements Mapping:** B.2.2.9.

#### 4.4.4 `config/sites-available/dfr.conf.template`
*   **Purpose:** Nginx site configuration for the DFR application.
*   **Key Content:**
    nginx
    # Upstream for Odoo longpolling
    upstream odoo_longpolling {
        server {{ODOO_APP_SERVICE_HOST}}:{{ODOO_LONGPOLLING_PORT | default(8072)}};
    }

    # Upstream for Odoo main application
    upstream odoo_app {
        server {{ODOO_APP_SERVICE_HOST}}:{{ODOO_APP_SERVICE_PORT | default(8069)}};
    }

    server {
        listen 80;
        server_name {{NGINX_SERVER_NAME}}; # e.g., dfr.example.country

        # Redirect all HTTP traffic to HTTPS
        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name {{NGINX_SERVER_NAME}};

        ssl_certificate /etc/nginx/ssl/{{SSL_CERTIFICATE_FILE}};
        ssl_certificate_key /etc/nginx/ssl/{{SSL_CERTIFICATE_KEY_FILE}};
        
        # Recommended SSL/TLS settings (can be in a separate snippet)
        # ssl_dhparam /etc/nginx/ssl/dhparam.pem; # If using custom DH params
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:10m;
        ssl_session_tickets off;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
        # Add HSTS header
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Odoo specific proxy settings
        proxy_buffers 16 64k;
        proxy_buffer_size 128k;
        proxy_read_timeout {{NGINX_PROXY_READ_TIMEOUT | default(720s)}}; # For longpolling
        proxy_connect_timeout {{NGINX_PROXY_CONNECT_TIMEOUT | default(300s)}};
        proxy_send_timeout {{NGINX_PROXY_SEND_TIMEOUT | default(300s)}};

        # Log format for more details
        # log_format odoo '$remote_addr - $remote_user [$time_local] "$request" '
        #                  '$status $body_bytes_sent "$http_referer" '
        #                  '"$http_user_agent" "$http_x_forwarded_for"';
        # access_log /var/log/nginx/odoo_access.log odoo;
        # error_log /var/log/nginx/odoo_error.log;

        location /longpolling {
            proxy_pass http://odoo_longpolling;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://odoo_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }

        # Cache static files
        location ~* /web/static/ {
            proxy_cache_valid 200 302 60m;
            proxy_cache_valid 404      1m;
            proxy_buffering    on;
            expires 864000; # 10 days
            proxy_pass http://odoo_app;
        }
    }
    
*   **Requirements Mapping:** B.2.2.9, REQ-DIO-005.

### 4.5 Component: Backup and Restore (`components/backup-restore/`)

#### 4.5.1 `scripts/backup_db.sh`
*   **Purpose:** Performs PostgreSQL database backup.
*   **Implementation Details:**
    *   Shell script (Bash). Sources `../shared/scripts/utils.sh` and `../config/backup_vars.sh.ENV` (where ENV is dev/staging/prod).
    *   **Parameters (from `backup_vars.sh`):**
        *   `DFR_DB_HOST`, `DFR_DB_PORT`, `DFR_DB_USER`, `DFR_DB_NAME`
        *   `DFR_DB_PASSWORD_FILE` (path to file containing password) or `DFR_DB_PASSWORD` (less secure)
        *   `BACKUP_DIR` (base directory for backups)
        *   `ODOO_FILESTORE_PATH` (path to Odoo filestore, if it needs separate backup)
        *   `BACKUP_METHOD` (`pg_dump` or `pg_basebackup`)
        *   `PG_DUMP_FORMAT` (`c` for custom, `p` for plain, `t` for tar - default 'c')
        *   `COMPRESS_BACKUP` (true/false)
        *   `RETENTION_DAYS` (for cleaning up old backups)
    *   **Logic:**
        1.  Create a timestamped subdirectory within `BACKUP_DIR`.
        2.  **If `BACKUP_METHOD` is `pg_dump`:**
            *   `pg_dump -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -d $DFR_DB_NAME -F $PG_DUMP_FORMAT -f $BACKUP_SUBDIR/dfr_db_$(date +%Y%m%d_%H%M%S).$PG_DUMP_FORMAT.dump`
            *   Use `PGPASSWORD=$(cat $DFR_DB_PASSWORD_FILE)` or equivalent.
        3.  **If `BACKUP_METHOD` is `pg_basebackup` (for PITR):**
            *   Requires PostgreSQL `archive_mode = on` and `archive_command` configured.
            *   `pg_basebackup -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -D $BACKUP_SUBDIR/db_basebackup -Ft -X stream -P -R` (creates `tar` format, streams WALs, adds progress, creates `standby.signal` and `postgresql.auto.conf` for recovery).
        4.  **Backup Filestore (if `ODOO_FILESTORE_PATH` is set):**
            *   `tar -czf $BACKUP_SUBDIR/dfr_filestore_$(date +%Y%m%d_%H%M%S).tar.gz $ODOO_FILESTORE_PATH`
        5.  (Optional) If `COMPRESS_BACKUP` is true and `pg_dump` was plain, compress the dump file using `gzip`.
        6.  Log success or failure.
        7.  **Cleanup:** Remove backups older than `RETENTION_DAYS` from `BACKUP_DIR`.
*   **Requirements Mapping:** REQ-DIO-007, B.2.2.9.

#### 4.5.2 `scripts/restore_db.sh`
*   **Purpose:** Restores PostgreSQL database from backup.
*   **Implementation Details:**
    *   Shell script (Bash). Sources `../shared/scripts/utils.sh` and `../config/backup_vars.sh.ENV`.
    *   **Parameters (from `backup_vars.sh` and command line):**
        *   `BACKUP_FILE` (path to the database dump file to restore - passed as argument)
        *   `FILESTORE_BACKUP_FILE` (optional path to filestore tarball - passed as argument)
        *   `DFR_DB_HOST`, `DFR_DB_PORT`, `DFR_DB_USER`, `DFR_DB_NAME`
        *   `DFR_DB_PASSWORD_FILE` or `DFR_DB_PASSWORD`
        *   `ODOO_SERVICE_NAME` (name of the Odoo Docker service/container)
        *   `ODOO_FILESTORE_PATH`
    *   **Logic:**
        1.  Prompt for confirmation: `confirm_action "Restore $BACKUP_FILE to $DFR_DB_NAME on $DFR_DB_HOST? This will overwrite existing data."`
        2.  **Stop Odoo Service:** (If running in Docker Compose) `docker-compose stop $ODOO_SERVICE_NAME` or use `docker_helpers.sh`.
        3.  **Drop/Recreate Database (for `pg_dump` restores):**
            *   `psql -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DFR_DB_NAME;"`
            *   `psql -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -d postgres -c "CREATE DATABASE $DFR_DB_NAME OWNER $DFR_DB_USER;"`
        4.  **Restore Database:**
            *   **If `pg_dump` file (e.g., `.dump`):**
                *   If compressed, decompress first.
                *   `pg_restore -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -d $DFR_DB_NAME $BACKUP_FILE` (for custom format)
                *   `psql -h $DFR_DB_HOST -p $DFR_DB_PORT -U $DFR_DB_USER -d $DFR_DB_NAME < $BACKUP_FILE` (for plain SQL format)
            *   **If `pg_basebackup` directory:**
                *   Requires stopping PostgreSQL server, replacing its data directory with the backup, and starting it. If PITR, also requires configuring `recovery.conf` or `postgresql.auto.conf` with restore command for WALs. This is more complex and might involve host-level operations or specific Docker volume management. The script might guide the user or perform these steps if run with sufficient privileges on the DB host.
        5.  **Restore Filestore (if `FILESTORE_BACKUP_FILE` provided):**
            *   Remove existing content in `$ODOO_FILESTORE_PATH`.
            *   `tar -xzf $FILESTORE_BACKUP_FILE -C $(dirname $ODOO_FILESTORE_PATH)`
        6.  Log success or failure.
        7.  **Start Odoo Service:** `docker-compose start $ODOO_SERVICE_NAME`.
*   **Requirements Mapping:** REQ-DIO-007.

#### 4.5.3 `config/backup_vars.sh.template`
*   **Purpose:** Configuration template for backup/restore scripts.
*   **Implementation Details:**
    *   Shell script defining variables. To be copied to `backup_vars.sh.development`, `backup_vars.sh.staging`, `backup_vars.sh.production` and customized.
    bash
    #!/bin/bash
    # DFR Backup/Restore Configuration Template for {{ENVIRONMENT_NAME}}

    # Database Connection
    DFR_DB_HOST="{{DB_HOST_PLACEHOLDER}}"
    DFR_DB_PORT="{{DB_PORT_PLACEHOLDER | default(5432)}}"
    DFR_DB_USER="{{DB_USER_PLACEHOLDER}}"
    DFR_DB_NAME="{{DB_NAME_PLACEHOLDER}}"
    # Store password in a file readable only by the backup user, e.g., /etc/dfr_backup/.pgpass
    # Ensure .pgpass format: hostname:port:database:username:password
    # Or, provide path to a file containing only the password:
    DFR_DB_PASSWORD_FILE="{{DB_PASSWORD_FILE_PLACEHOLDER}}" 
    # Alternatively, for less secure direct password (use with caution, e.g., for dev from .env):
    # DFR_DB_PASSWORD="{{DB_PASSWORD_PLACEHOLDER}}"

    # Backup Configuration
    BACKUP_DIR="/var/backups/dfr/{{COUNTRY_CODE}}/{{ENVIRONMENT_NAME}}" # Base directory
    ODOO_FILESTORE_PATH="/var/lib/odoo/filestore/$DFR_DB_NAME" # Path to Odoo filestore
    BACKUP_METHOD="pg_dump" # "pg_dump" or "pg_basebackup"
    PG_DUMP_FORMAT="c"      # "c" (custom), "p" (plain), "t" (tar) - for pg_dump
    COMPRESS_BACKUP="true" # "true" or "false"

    # Retention Policy
    RETENTION_DAYS_DAILY="7"
    RETENTION_WEEKS_WEEKLY="4" # Number of weekly backups to keep
    RETENTION_MONTHS_MONTHLY="6" # Number of monthly backups to keep

    # Docker Service Names (for restore script to stop/start services)
    ODOO_SERVICE_NAME="odoo"
    POSTGRES_SERVICE_NAME="postgres"
    
    # S3/Cloud Storage (Optional - if backups are uploaded to cloud)
    # S3_BUCKET_NAME="s3://your-dfr-backups-bucket/{{COUNTRY_CODE}}/{{ENVIRONMENT_NAME}}"
    # AWS_PROFILE_NAME="dfr_backup_profile" # if using AWS CLI profiles
    
*   **Requirements Mapping:** REQ-DIO-007.

### 4.6 Environment Orchestration (`environments/`)

#### 4.6.1 `common/docker-compose.common.yml`
*   **Purpose:** Shared Docker Compose definitions.
*   **Key Content:**
    yaml
    version: '3.8'

    networks:
      dfr_internal_network:
        driver: bridge
    
    *   May also include base service definitions with `<<: &service_defaults` anchors if complex common configurations are needed, to be merged by environment-specific files.
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006.

#### 4.6.2 `common/env.common.template`
*   **Purpose:** Template for common environment variables.
*   **Key Content:**
    env
    # Common Application Settings
    ODOO_IMAGE_NAME=dfr_odoo_app
    ODOO_IMAGE_TAG=latest # Should be specific in Staging/Prod, e.g., 1.0.0
    POSTGRES_IMAGE_NAME=dfr_postgres_db
    POSTGRES_IMAGE_TAG=16-alpine # Or custom tag if built
    NGINX_IMAGE_NAME=dfr_nginx_proxy
    NGINX_IMAGE_TAG=latest # Or custom tag

    # These might be common, or overridden per environment
    ODOO_LOG_LEVEL=info
    ODOO_WORKERS=2 # Example, adjust per environment
    ODOO_LIMIT_TIME_CPU=600
    ODOO_LIMIT_TIME_REAL=1200
    ODOO_PROXY_MODE=True
    
*   **Requirements Mapping:** REQ-DIO-006.

#### 4.6.3 Per-Environment Setup (`development/`, `staging/`, `production/`)

##### `docker-compose.yml` (Example for `development`)
*   **Purpose:** Environment-specific Docker Compose orchestration.
*   **Key Content:**
    yaml
    version: '3.8'

    # Optionally extend common configurations
    # services:
    #   odoo:
    #     <<: *common_odoo_service_definition # If defined in common
    #     ... development specific overrides ...

    services:
      postgres:
        image: ${POSTGRES_IMAGE_NAME}:${POSTGRES_IMAGE_TAG:-16-alpine}
        container_name: dfr_postgres_dev
        volumes:
          - dfr_postgres_data_dev:/var/lib/postgresql/data
          # Optional: Mount init scripts if not baked into a custom image
          # - ../../components/postgres/initdb.d:/docker-entrypoint-initdb.d 
        environment:
          - POSTGRES_USER=${DFR_DB_USER}
          - POSTGRES_PASSWORD=${DFR_DB_PASSWORD}
          - POSTGRES_DB=${DFR_DB_NAME}
        ports: # Expose only for dev convenience if needed
          - "${DFR_DB_EXTERNAL_PORT:-5433}:5432"
        networks:
          - dfr_internal_network
        restart: unless-stopped

      odoo:
        image: ${ODOO_IMAGE_NAME}:${ODOO_IMAGE_TAG:-latest} 
        # For local dev, build from local Dockerfile:
        # build:
        #   context: ../../components/odoo
        #   dockerfile: Dockerfile
        container_name: dfr_odoo_dev
        depends_on:
          - postgres
        volumes:
          # Mount custom addons for live development
          - ../../../dfr_addons:/mnt/extra-addons 
          - dfr_odoo_data_dev:/var/lib/odoo # For filestore
          # Mount odoo.conf if managed outside entrypoint for dev
          # - ./config/odoo.conf:/etc/odoo/odoo.conf 
        environment:
          - ODOO_DB_HOST=postgres
          - ODOO_DB_PORT=5432
          - ODOO_DB_USER=${DFR_DB_USER}
          - ODOO_DB_PASSWORD=${DFR_DB_PASSWORD}
          - ODOO_DB_NAME=${DFR_DB_NAME}
          - ODOO_ADMIN_PASSWD=${ODOO_MASTER_PASSWORD}
          - ODOO_DEMO_DATA=${ODOO_LOAD_DEMO_DATA:-false}
          - ODOO_WORKERS=${ODOO_DEV_WORKERS:-0} # 0 for easier debugging
          - ODOO_LOG_LEVEL=${ODOO_DEV_LOG_LEVEL:-debug}
          # Add other ODOO_* env vars used by entrypoint.sh
        ports:
          - "${ODOO_APP_EXTERNAL_PORT:-8069}:8069" # Odoo HTTP
          - "${ODOO_LONGPOLLING_EXTERNAL_PORT:-8072}:8072" # Odoo Longpolling
        networks:
          - dfr_internal_network
        restart: unless-stopped

      nginx: # Optional for development, but good for consistency
        image: ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG:-latest}
        # build:
        #   context: ../../components/nginx
        #   dockerfile: Dockerfile
        container_name: dfr_nginx_dev
        depends_on:
          - odoo
        ports:
          - "${NGINX_HTTP_PORT:-80}:80"
          - "${NGINX_HTTPS_PORT:-443}:443"
        volumes:
          - ../../components/nginx/config/sites-available/dfr.conf.template:/etc/nginx/templates/dfr.conf.template # If using envsubst in Nginx entrypoint
          # Or mount prepared config:
          # - ./config/nginx/dfr.conf:/etc/nginx/sites-enabled/dfr.conf 
          # Mount SSL certificates for development (e.g., self-signed)
          - ./certs:/etc/nginx/ssl 
        environment:
          - NGINX_SERVER_NAME=${DEV_SERVER_NAME:-localhost}
          - ODOO_APP_SERVICE_HOST=odoo
          - ODOO_APP_SERVICE_PORT=8069
          - ODOO_LONGPOLLING_PORT=8072
          - SSL_CERTIFICATE_FILE=dev.crt # Example
          - SSL_CERTIFICATE_KEY_FILE=dev.key # Example
        networks:
          - dfr_internal_network
        restart: unless-stopped
        # command: /bin/sh -c "envsubst < /etc/nginx/templates/dfr.conf.template > /etc/nginx/sites-enabled/dfr.conf && exec nginx -g 'daemon off;'" # If using envsubst

    volumes:
      dfr_postgres_data_dev:
      dfr_odoo_data_dev:

    networks:
      dfr_internal_network:
        # Use external network defined in common, or define here
        # external: true 
        # name: dfr_common_network 
        driver: bridge 
    
    *   **Staging/Production `docker-compose.yml` files:**
        *   Will not use local `build:` contexts for Odoo/Nginx/Postgres if pre-built images are pushed to a registry. They will reference specific image tags from the registry.
        *   Volume mounts for code (`../../../dfr_addons`) will be removed for Odoo; addons should be baked into the production image.
        *   Ports might not be exposed directly on the host, relying on the Nginx reverse proxy and cloud provider load balancers.
        *   Resource limits (`deploy: resources: limits/reservations`) should be defined for production.
        *   Logging drivers configured for production log aggregation.
*   **Requirements Mapping:** REQ-PCA-015, REQ-DIO-006, B.2.2.9, B.3.B1.11.

##### `.env.template` (Example for `development/.env.template`)
*   **Purpose:** Template for environment-specific variables.
*   **Key Content:**
    env
    # Development Environment Specifics
    # Copy this to .env and fill in values

    # PostgreSQL Credentials & DB
    DFR_DB_USER=odoo_dev_user
    DFR_DB_PASSWORD=supersecretdevpassword
    DFR_DB_NAME=dfr_dev_db
    DFR_DB_EXTERNAL_PORT=5433 # Host port to map to container's 5432

    # Odoo Configuration
    ODOO_MASTER_PASSWORD=devadminmasterpassword
    ODOO_LOAD_DEMO_DATA=false
    ODOO_DEV_WORKERS=0 # 0 means multi-threading, good for dev and cron
    ODOO_DEV_LOG_LEVEL=debug
    ODOO_APP_EXTERNAL_PORT=10069 # Host port for Odoo HTTP
    ODOO_LONGPOLLING_EXTERNAL_PORT=10072 # Host port for Odoo longpolling

    # Nginx Configuration (if used in dev)
    NGINX_HTTP_PORT=8088 # Host port for Nginx HTTP
    NGINX_HTTPS_PORT=8443 # Host port for Nginx HTTPS
    DEV_SERVER_NAME=localhost

    # Common settings can be inherited or redefined from common/env.common.template
    # ODOO_IMAGE_TAG=local-dev
    
    *   `staging/.env.staging.template` and `production/.env.production.template` will have similar structures but with placeholders for staging/production specific values, especially credentials and service endpoints. Production `.env` file must be managed securely and NOT committed to Git.
*   **Requirements Mapping:** REQ-DIO-006.

### 4.7 Shared Scripts (`shared/scripts/`)

#### 4.7.1 `utils.sh`
*   **Purpose:** Common utility functions for shell scripts.
*   **Implementation Details:**
    *   Bash script defining functions.
    *   **`log_info <message>`:** Prints message with INFO prefix and timestamp.
    *   **`log_warning <message>`:** Prints message with WARNING prefix and timestamp (e.g., yellow color).
    *   **`log_error <message>`:** Prints message with ERROR prefix and timestamp (e.g., red color), exits script with error code 1.
    *   **`log_success <message>`:** Prints message with SUCCESS prefix and timestamp (e.g., green color).
    *   **`confirm_action <prompt_message>`:** Asks user for [y/N] confirmation. Returns 0 if yes, 1 if no.
        bash
        # Example log_info
        log_info() {
            echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $1"
        }
        # Example confirm_action
        confirm_action() {
            local prompt="$1"
            read -r -p "${prompt} [y/N]: " response
            case "$response" in
                [yY][eE][sS]|[yY]) 
                    return 0
                    ;;
                *)
                    return 1
                    ;;
            esac
        }
        
*   **Requirements Mapping:** B.3.B1.11.

#### 4.7.2 `docker_helpers.sh`
*   **Purpose:** Helper functions for Docker and Docker Compose operations.
*   **Implementation Details:**
    *   Bash script. Sources `utils.sh`.
    *   **`is_container_running <container_name_or_id>`:** Checks if a container is running. Returns 0 if running, 1 otherwise.
        *   Uses `docker ps -q -f name=^/${container_name_or_id}$` or `docker inspect -f '{{.State.Running}}' $container_name_or_id`.
    *   **`stop_and_remove_container <container_name_or_id>`:** Safely stops and removes a container.
        *   Uses `docker stop $container_name_or_id && docker rm $container_name_or_id`.
    *   **`build_docker_image <dockerfile_path> <image_name> <tag> [build_args...]`:** Builds a Docker image.
        *   Uses `docker build -f $dockerfile_path -t $image_name:$tag ${build_args} .` (context might need adjustment).
    *   **`ensure_network_exists <network_name>`:** Creates a Docker network if it doesn't exist.
        *   Uses `docker network inspect $network_name >/dev/null 2>&1 || docker network create $network_name`.
    *   **`pull_image_if_not_exists <image_name_with_tag>`:** Pulls image if not present locally.
        *   `docker image inspect $image_name_with_tag >/dev/null 2>&1 || docker pull $image_name_with_tag`
*   **Requirements Mapping:** REQ-DIO-006, B.3.B1.11.

### 4.8 Kubernetes Manifests (`kubernetes/`) (Optional)
*   If Kubernetes is adopted, this directory will contain YAML manifest files for:
    *   `Deployments` or `StatefulSets` for Odoo, PostgreSQL.
    *   `Services` to expose Odoo and PostgreSQL internally.
    *   `Ingress` resources for Nginx-like external access and HTTPS termination.
    *   `ConfigMaps` and `Secrets` for configuration and sensitive data.
    *   `PersistentVolumeClaims` for data persistence.
    *   `CronJobs` for scheduled tasks like backups.
    *   Potentially Helm charts for packaging these manifests.
*   **Requirements Mapping:** REQ-PCA-015 (if k8s is the chosen method for an environment), REQ-DIO-006.

### 4.9 Ansible Playbooks (`ansible/`) (Optional)
*   If Ansible is adopted for infrastructure provisioning or more complex configuration management beyond Docker Compose:
    *   Playbooks for setting up Docker hosts, configuring cloud resources, deploying Docker Compose files to remote servers.
    *   Roles for Odoo, PostgreSQL, Nginx setup.
    *   Inventory files.
*   **Requirements Mapping:** REQ-PCA-015 (if Ansible is part of the deployment strategy), REQ-DIO-006.


## 5. Deployment Strategies

### 5.1 Local Development
1.  Clone the `DFR_DEPLOYMENT_SCRIPTS` repository.
2.  Navigate to `environments/development/`.
3.  Copy `.env.template` to `.env` and fill in the required values.
4.  Ensure DFR custom addons source code is available at the path specified in `docker-compose.yml` (e.g., `../../../dfr_addons`).
5.  Run `make deploy_dev` from the root directory, or `docker-compose up -d --build` from `environments/development/`.

### 5.2 Staging/Production Deployment
1.  **Prerequisites:**
    *   Host server(s) prepared with Docker and Docker Compose.
    *   Securely manage environment variables/secrets (e.g., using a secrets manager, CI/CD pipeline variables, or encrypted files).
    *   SSL/TLS certificates obtained and placed securely.
    *   Backup storage configured.
2.  **Image Preparation:**
    *   For Staging/Production, Docker images (Odoo, Nginx, potentially PostgreSQL if customized) should be pre-built by a CI/CD pipeline and pushed to a Docker registry. The `docker-compose.yml` files for these environments will reference these specific image tags.
3.  **Configuration:**
    *   Copy the appropriate `.env.<environment>.template` (e.g., `.env.staging.template`) to a secure location on the server or inject variables via CI/CD. Do NOT commit actual production secrets.
    *   Customize `components/backup-restore/config/backup_vars.sh.<environment>` with correct paths and credentials.
4.  **Deployment:**
    *   Use `make deploy_staging` or `make deploy_production` (which internally calls `docker-compose -f environments/<env>/docker-compose.yml up -d`).
    *   The initial Odoo database setup (installing modules) might be a manual step post-deployment or handled by the Odoo entrypoint script if `ODOO_AUTO_INIT_DB` or similar logic is robustly implemented.
5.  **Post-Deployment:**
    *   Verify all services are running.
    *   Test application accessibility.
    *   Configure automated backups (e.g., using `cron` to run `backup_db.sh`).

## 6. Backup and Restore Procedures

### 6.1 Backup
*   Use the `components/backup-restore/scripts/backup_db.sh` script.
*   Configure `components/backup-restore/config/backup_vars.sh.<environment>` for the target environment.
*   Schedule this script using `cron` or a similar job scheduler for automated daily backups.
*   Ensure backup files are regularly transferred to a secure, offsite/separate storage location.
*   **Requirements Mapping:** REQ-DIO-007.

### 6.2 Restore
*   Use the `components/backup-restore/scripts/restore_db.sh` script.
*   Configure `components/backup-restore/config/backup_vars.sh.<environment>` for the target environment (usually Staging or a temporary restore instance).
*   Provide the `BACKUP_FILE` path as an argument.
*   This script handles stopping Odoo, dropping/creating the DB (for `pg_dump`), restoring, and restarting Odoo.
*   Thoroughly test restored data in a non-production environment before considering any production restore.
*   For PITR using `pg_basebackup`, the restore process is more involved and typically includes setting up a recovery configuration for PostgreSQL to replay WAL files. The `restore_db.sh` would need significant enhancements or be part of a more detailed PostgreSQL-specific DR runbook for this scenario.
*   **Requirements Mapping:** REQ-DIO-007.

## 7. Error Handling and Logging
*   **Shell Scripts:**
    *   Use `set -e` to exit on error.
    *   Use `set -o pipefail` to catch errors in pipelines.
    *   Implement robust error checking after critical commands.
    *   Utilize logging functions from `shared/scripts/utils.sh` for consistent output.
    *   Redirect `stdout` and `stderr` of commands to log files where appropriate, especially for background jobs like backups.
*   **Docker Containers:**
    *   Container logs will be accessible via `docker logs <container_name>` or `docker-compose logs <service_name>`.
    *   For production, configure Docker logging drivers to send logs to a centralized logging system (e.g., ELK stack, Splunk, CloudWatch).
*   **Makefile:**
    *   Targets should report success or failure clearly.

## 8. Versioning and Changelog
*   The `VERSION` file in the root directory tracks the version of the `DFR_DEPLOYMENT_SCRIPTS` repository itself.
*   Docker images built by these scripts should be tagged with application versions (e.g., DFR Odoo app version) and/or Git commit SHAs for traceability.
*   A `CHANGELOG.md` (not part of these scripts but part of the overall DFR project) should document changes to the application that might impact deployment procedures.

## 9. Future Considerations (Optional Components)
*   **Kubernetes:** If adopted, detailed specifications for Kubernetes manifests, Helm charts, and `kubectl` based deployment scripts will be added under `kubernetes/`.
*   **Ansible:** If adopted for infrastructure provisioning or advanced configuration management, playbooks and roles will be specified under `ansible/`.
*   **Automated SSL Certificate Renewal:** Integration with Certbot or similar tools for automated SSL certificate management for Nginx.
*   **Advanced Monitoring Integration:** Scripts or configurations for deeper integration with monitoring tools like Prometheus (exporters) or Datadog.