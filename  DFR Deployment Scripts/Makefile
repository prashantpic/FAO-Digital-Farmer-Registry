SHELL := /bin/bash
.DEFAULT_GOAL := help

# Environment configuration
# These can be overridden when calling make, e.g., make build_odoo ODOO_IMAGE_TAG=1.0.0
ODOO_IMAGE_NAME ?= dfr_odoo_app
ODOO_IMAGE_TAG ?= latest
POSTGRES_IMAGE_NAME ?= dfr_postgres_db
POSTGRES_IMAGE_TAG ?= 16-alpine
NGINX_IMAGE_NAME ?= dfr_nginx_proxy
NGINX_IMAGE_TAG ?= latest

# For restore_db_staging target
BACKUP_FILE ?=
FILESTORE_BACKUP_FILE ?=

# Environment for backup/restore scripts (e.g., production, staging)
ENV ?= development

.PHONY: help build_odoo build_postgres build_nginx build_all_images \
        deploy_dev deploy_staging deploy_production \
        stop_dev stop_staging stop_production \
        logs_dev logs_staging logs_production \
        backup_db_prod restore_db_staging clean

help:
	@echo "DFR Deployment Scripts Makefile"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Build Targets:"
	@echo "  build_odoo           Builds the Odoo Docker image."
	@echo "  build_postgres       Builds the PostgreSQL Docker image."
	@echo "  build_nginx          Builds the Nginx Docker image."
	@echo "  build_all_images     Builds all DFR Docker images."
	@echo ""
	@echo "Deployment Targets:"
	@echo "  deploy_dev           Deploys the development environment using Docker Compose."
	@echo "  deploy_staging       Deploys the staging environment using Docker Compose."
	@echo "  deploy_production    Deploys the production environment using Docker Compose."
	@echo ""
	@echo "Operational Targets:"
	@echo "  stop_dev             Stops the development environment."
	@echo "  stop_staging         Stops the staging environment."
	@echo "  stop_production      Stops the production environment."
	@echo "  logs_dev [service...]  Tails logs for the development environment (optionally specify services)."
	@echo "  logs_staging [service...] Tails logs for the staging environment (optionally specify services)."
	@echo "  logs_production [service...] Tails logs for the production environment (optionally specify services)."
	@echo "  backup_db_prod       Triggers a database backup for the production environment."
	@echo "                       Requires 'components/backup-restore/config/backup_vars.sh.production'."
	@echo "                       Can pass COUNTRY_CODE, e.g., make backup_db_prod COUNTRY_CODE=vu"
	@echo "  restore_db_staging   Restores a database backup to staging."
	@echo "                       Usage: make restore_db_staging BACKUP_FILE=<path_to_db_backup> [FILESTORE_BACKUP_FILE=<path_to_filestore_backup>]"
	@echo "                       Requires 'components/backup-restore/config/backup_vars.sh.staging'."
	@echo "                       Can pass COUNTRY_CODE, e.g., make restore_db_staging BACKUP_FILE=... COUNTRY_CODE=vu"
	@echo ""
	@echo "Cleanup Targets:"
	@echo "  clean                Removes Docker volumes for development (use with caution)."
	@echo ""

# Build Targets
build_odoo: ## Builds the Odoo Docker image
	@echo "Building Odoo image (${ODOO_IMAGE_NAME}:${ODOO_IMAGE_TAG})..."
	@docker build -t ${ODOO_IMAGE_NAME}:${ODOO_IMAGE_TAG} ./components/odoo

build_postgres: ## Builds the PostgreSQL Docker image
	@echo "Building PostgreSQL image (${POSTGRES_IMAGE_NAME}:${POSTGRES_IMAGE_TAG})..."
	@docker build -t ${POSTGRES_IMAGE_NAME}:${POSTGRES_IMAGE_TAG} ./components/postgres

build_nginx: ## Builds the Nginx Docker image
	@echo "Building Nginx image (${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG})..."
	@docker build -t ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG} ./components/nginx

build_all_images: build_odoo build_postgres build_nginx ## Builds all DFR Docker images
	@echo "All DFR images built."

# Deployment Targets
deploy_dev: ## Deploys the development environment
	@echo "Deploying development environment..."
	@cd environments/development/ && \
		(test -f .env || (echo "Warning: .env file not found. Copying from .env.template. Please fill it." && cp .env.template .env)) && \
		docker-compose up -d --build
	@echo "Development environment deployed."

deploy_staging: ## Deploys the staging environment
	@echo "Deploying staging environment..."
	@cd environments/staging/ && \
		(test -f .env.staging || (echo "Error: .env.staging file not found. Please create and configure it from .env.staging.template." && exit 1)) && \
		docker-compose -f docker-compose.yml --env-file .env.staging up -d
	@echo "Staging environment deployed."

deploy_production: ## Deploys the production environment
	@echo "Deploying production environment..."
	@cd environments/production/ && \
		(test -f .env.production || (echo "Error: .env.production file not found. Please create and configure it securely from .env.production.template." && exit 1)) && \
		docker-compose -f docker-compose.yml --env-file .env.production up -d
	@echo "Production environment deployed."

# Operational Targets - Stop
stop_dev: ## Stops the development environment
	@echo "Stopping development environment..."
	@cd environments/development/ && docker-compose down
	@echo "Development environment stopped."

stop_staging: ## Stops the staging environment
	@echo "Stopping staging environment..."
	@cd environments/staging/ && docker-compose -f docker-compose.yml --env-file .env.staging down
	@echo "Staging environment stopped."

stop_production: ## Stops the production environment
	@echo "Stopping production environment..."
	@cd environments/production/ && docker-compose -f docker-compose.yml --env-file .env.production down
	@echo "Production environment stopped."

# Operational Targets - Logs
logs_dev: ## Tails logs for the development environment
	@echo "Tailing logs for development environment... Press Ctrl+C to stop."
	@cd environments/development/ && docker-compose logs -f $(filter-out $@,$(MAKECMDGOALS))

logs_staging: ## Tails logs for the staging environment
	@echo "Tailing logs for staging environment... Press Ctrl+C to stop."
	@cd environments/staging/ && docker-compose -f docker-compose.yml --env-file .env.staging logs -f $(filter-out $@,$(MAKECMDGOALS))

logs_production: ## Tails logs for the production environment
	@echo "Tailing logs for production environment... Press Ctrl+C to stop."
	@cd environments/production/ && docker-compose -f docker-compose.yml --env-file .env.production logs -f $(filter-out $@,$(MAKECMDGOALS))

# Operational Targets - Backup & Restore
backup_db_prod: ## Triggers a database backup for the production environment
	@echo "Starting production database backup..."
	@if [ ! -f "components/backup-restore/config/backup_vars.sh.production" ]; then \
		echo "Error: Production backup configuration 'components/backup-restore/config/backup_vars.sh.production' not found." && exit 1; \
	fi
	@ENV=production components/backup-restore/scripts/backup_db.sh
	@echo "Production database backup process initiated."

restore_db_staging: ## Restores a database backup to the staging environment
	@echo "Starting staging database restore..."
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: BACKUP_FILE variable is not set. Usage: make restore_db_staging BACKUP_FILE=/path/to/backup.dump"; exit 1; \
	fi
	@if [ ! -f "components/backup-restore/config/backup_vars.sh.staging" ]; then \
		echo "Error: Staging backup configuration 'components/backup-restore/config/backup_vars.sh.staging' not found." && exit 1; \
	fi
	@echo "Using DB backup file: $(BACKUP_FILE)"
	@if [ ! -z "$(FILESTORE_BACKUP_FILE)" ]; then \
		echo "Using Filestore backup file: $(FILESTORE_BACKUP_FILE)"; \
	fi
	@ENV=staging components/backup-restore/scripts/restore_db.sh "$(BACKUP_FILE)" "$(FILESTORE_BACKUP_FILE)"
	@echo "Staging database restore process initiated."

# Cleanup Targets
clean: ## Removes Docker volumes for development (use with caution)
	@echo "WARNING: This will remove development Docker volumes. This is a destructive operation."
	@read -r -p "Are you sure you want to continue? [y/N] " response; \
	if [[ "$$response" =~ ^([yY][eE][sS]|[yY]) ]]; then \
		echo "Removing development Docker volumes..."; \
		cd environments/development/ && docker-compose down -v; \
		echo "Development Docker volumes removed."; \
	else \
		echo "Cleanup cancelled."; \
	fi