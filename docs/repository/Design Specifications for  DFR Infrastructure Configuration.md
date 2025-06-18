# Software Design Specification: DFR Infrastructure Configuration (DFR_INFRA_CONFIG)

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the DFR Infrastructure Configuration (DFR_INFRA_CONFIG) repository. This repository is responsible for providing Infrastructure as Code (IaC) scripts using Terraform and Ansible to provision and manage the necessary infrastructure for deploying the Digital Farmer Registry (DFR) system. The configurations aim to support deployments across diverse environments, including government data centers (VM-based) and approved cloud providers (AWS, Azure, GCP), ensuring consistency, repeatability, and adherence to specified requirements for each of the five Project Targeted Pacific Island Countries.

### 1.2 Scope
The scope of this SDS covers:
-   Terraform configurations for provisioning cloud infrastructure (VPCs, subnets, compute instances, managed databases, storage, IAM roles, security groups, load balancers).
-   Ansible playbooks and roles for configuring operating systems, installing prerequisite software (Docker, Nginx), deploying DFR application containers (Odoo, PostgreSQL, Nginx reverse proxy), and setting up operational aspects like backups and monitoring.
-   Modular design to support different cloud providers (AWS as primary example, with placeholders/structure for Azure and GCP) and on-premise VM deployments.
-   Parameterization for environment-specific configurations (e.g., staging, production for each country).
-   Scripts to simplify the execution of Terraform and Ansible configurations.

This SDS addresses the deployment of the following conceptual components:
-   `dfr-infra-odoo-app-container-019` (Odoo Application)
-   `dfr-infra-postgres-db-container-020` (PostgreSQL Database)
-   `dfr-infra-reverse-proxy-021` (Nginx Reverse Proxy)

### 1.3 Definitions, Acronyms, and Abbreviations
-   **DFR:** Digital Farmer Registry
-   **IaC:** Infrastructure as Code
-   **Terraform:** An open-source IaC software tool.
-   **Ansible:** An open-source software provisioning, configuration management, and application-deployment tool.
-   **AWS:** Amazon Web Services
-   **Azure:** Microsoft Azure
-   **GCP:** Google Cloud Platform
-   **VM:** Virtual Machine
-   **VPC:** Virtual Private Cloud
-   **EC2:** Elastic Compute Cloud (AWS)
-   **RDS:** Relational Database Service (AWS)
-   **S3:** Simple Storage Service (AWS)
-   **IAM:** Identity and Access Management
-   **HCL:** HashiCorp Configuration Language
-   **YAML:** YAML Ain't Markup Language
-   **CKI:** Cook Islands
-   **CI/CD:** Continuous Integration/Continuous Deployment
-   **DR:** Disaster Recovery
-   **RTO:** Recovery Time Objective
-   **RPO:** Recovery Point Objective
-   **SDK:** Software Development Kit
-   **CLI:** Command Line Interface
-   **DNS:** Domain Name System
-   **SSL/TLS:** Secure Sockets Layer/Transport Layer Security
-   **OS:** Operating System
-   **SOP:** Standard Operating Procedure

### 1.4 References
-   Digital Farmer Registry (DFR) - Software Requirement Specification (SRS) document (especially sections A.2.4, A.3.4, REQ-PCA-012, REQ-DIO-002)
-   DFR Architecture Design Document
-   Terraform Documentation (https://developer.hashicorp.com/terraform/docs)
-   Ansible Documentation (https://docs.ansible.com/ansible/latest/index.html)
-   Cloud provider documentation (AWS, Azure, GCP)

## 2. System Overview
The DFR_INFRA_CONFIG repository provides a set of scripts and configuration files to automate the provisioning and setup of the DFR system's infrastructure. It leverages Terraform for provisioning cloud resources or preparing on-premise environments, and Ansible for configuring the operating systems and deploying the DFR application components (Odoo, PostgreSQL, Nginx) as Docker containers.

The design emphasizes modularity, allowing for adaptation to different cloud providers or on-premise scenarios. Environment-specific configurations are managed through variable files and inventory definitions.

## 3. Design Considerations

### 3.1 Assumptions and Dependencies
-   Target environments (cloud or on-premise) will provide necessary API access for Terraform and SSH access for Ansible.
-   Cloud provider accounts and credentials (API keys, service principals) will be securely managed and made available to the IaC tools.
-   Network connectivity will be available from the execution environment of IaC scripts to target cloud APIs and/or VMs.
-   Pre-built Docker images for Odoo (dfr-infra-odoo-app-container-019), PostgreSQL (dfr-infra-postgres-db-container-020), and Nginx (dfr-infra-reverse-proxy-021) are available in a specified Docker registry.
-   SSL/TLS certificates will be provided or a mechanism for obtaining them (e.g., Let's Encrypt with Certbot) will be integrated.
-   DNS records will be managed (potentially outside this repository's scope but required for FQDN access).
-   Specific backup, monitoring, and DR requirements (RTO/RPO) will be finalized per country and incorporated into configurations.

### 3.2 General Constraints
-   The primary cloud provider for detailed implementation examples will be AWS. Azure and GCP configurations will be structured as extendable placeholders.
-   On-premise VM provisioning is out of scope; Ansible playbooks will assume VMs are pre-existing.
-   Security is paramount: configurations must adhere to the principle of least privilege, secure network configurations (security groups, firewalls), and secure credential management.
-   Idempotency: Ansible playbooks and Terraform configurations should be idempotent.
-   Consistency: Ensure consistent environments across development, staging, and production tiers.

### 3.3 Goals and Guidelines
-   **Automation:** Automate infrastructure provisioning and configuration to the maximum extent possible.
-   **Repeatability:** Ensure DFR environments can be reliably and repeatedly created.
-   **Modularity:** Design reusable Terraform modules and Ansible roles.
-   **Parameterization:** Allow for easy customization for different environments (dev, staging, prod) and countries.
-   **Security by Design:** Embed security best practices in IaC scripts.
-   **Maintainability:** Create clear, well-documented code.
-   **Support for Diverse Hosting:** The scripts should be adaptable for major cloud providers and on-premise VM deployments (Linux-based).

## 4. Detailed Design

### 4.1 Terraform Configuration (`terraform/`)

#### 4.1.1 Global Files
1.  **`terraform/providers.tf`**
    *   **Purpose:** Declare and configure Terraform providers for AWS, Azure, and GCP.
    *   **Logic:**
        hcl
        terraform {
          required_providers {
            aws = {
              source  = "hashicorp/aws"
              version = "~> 5.0" // Specify appropriate version
            }
            azurerm = {
              source  = "hashicorp/azurerm"
              version = "~> 3.0" // Specify appropriate version
            }
            google = {
              source  = "hashicorp/google"
              version = "~> 5.0" // Specify appropriate version
            }
          }
        }

        provider "aws" {
          region = var.aws_region // Default region, can be overridden
          // Credentials configured via environment variables, IAM roles, or shared credentials file
        }

        provider "azurerm" {
          features {}
          // Credentials configured via environment variables, Azure CLI, or service principal
        }

        provider "google" {
          // Credentials configured via environment variables, gcloud CLI, or service account key
          project = var.gcp_project_id // If applicable
          region  = var.gcp_region     // If applicable
        }
        
    *   **Variables Referenced:** `var.aws_region`, `var.gcp_project_id`, `var.gcp_region` (to be defined in environment or module variables).

2.  **`terraform/versions.tf`**
    *   **Purpose:** Specify the required Terraform CLI version.
    *   **Logic:**
        hcl
        terraform {
          required_version = "~> 1.8.5" // Align with specified framework version
        }
        

3.  **`terraform/backend.tf`**
    *   **Purpose:** Configure remote state storage. Placeholder for specific backend configuration.
    *   **Logic:**
        *This file will initially contain commented-out examples or a generic structure. The actual backend configuration will be specific to the chosen state storage solution for the project (e.g., S3, Azure Blob, GCS).*
        hcl
        # Example for AWS S3 backend (uncomment and configure as needed)
        # terraform {
        #   backend "s3" {
        #     bucket         = "dfr-terraform-state-bucket-unique-name" # Replace with actual bucket name
        #     key            = "global/s1/terraform.tfstate" # Example path
        #     region         = "ap-southeast-2" # Example region
        #     encrypt        = true
        #     dynamodb_table = "dfr-terraform-state-lock" # For state locking
        #   }
        # }

        # Example for Azure Blob Storage (uncomment and configure as needed)
        # terraform {
        #   backend "azurerm" {
        #     resource_group_name  = "dfr-terraform-rg"
        #     storage_account_name = "dfrterraformstateunique"
        #     container_name       = "tfstate"
        #     key                  = "terraform.tfstate"
        #   }
        # }

        # Example for Google Cloud Storage (uncomment and configure as needed)
        # terraform {
        #   backend "gcs" {
        #     bucket  = "dfr-terraform-state-bucket-unique-name"
        #     prefix  = "terraform/state"
        #   }
        # }
        
    *   **Note:** Actual backend configuration must be done per project setup instructions.

#### 4.1.2 AWS DFR Stack Module (`terraform/modules/aws_dfr_stack/`)
This module encapsulates the resources needed to deploy a DFR instance on AWS.

1.  **`variables.tf`**
    *   **Purpose:** Define input variables for the AWS DFR stack.
    *   **Selected Variables (examples, to be expanded):**
        hcl
        variable "aws_region" {
          description = "AWS region for deployment."
          type        = string
          default     = "ap-southeast-2"
        }
        variable "environment_name" {
          description = "Name of the environment (e.g., staging, prod, cki-staging)."
          type        = string
        }
        variable "country_code" {
          description = "Two-letter country code (e.g., ck, ws, to, sb, vu)."
          type        = string
        }
        variable "vpc_cidr" {
          description = "CIDR block for the VPC."
          type        = string
          default     = "10.0.0.0/16"
        }
        variable "public_subnet_cidrs" {
          description = "List of CIDR blocks for public subnets."
          type        = list(string)
          default     = ["10.0.1.0/24", "10.0.2.0/24"]
        }
        variable "private_subnet_cidrs" {
          description = "List of CIDR blocks for private subnets."
          type        = list(string)
          default     = ["10.0.101.0/24", "10.0.102.0/24"]
        }
        variable "availability_zones" {
          description = "List of Availability Zones to use."
          type        = list(string)
          default     = [] // If empty, will use default AZs in the region
        }
        variable "odoo_instance_type" {
          description = "EC2 instance type for Odoo application server."
          type        = string
          default     = "t3.medium"
        }
        variable "nginx_instance_type" {
          description = "EC2 instance type for Nginx reverse proxy server."
          type        = string
          default     = "t3.small"
        }
        variable "postgres_instance_class" {
          description = "RDS instance class for PostgreSQL."
          type        = string
          default     = "db.t3.medium"
        }
        variable "postgres_allocated_storage" {
          description = "Allocated storage for PostgreSQL RDS in GB."
          type        = number
          default     = 100
        }
        variable "postgres_db_name" {
          description = "Name of the PostgreSQL database."
          type        = string
          default     = "odoodb"
        }
        variable "postgres_db_username" {
          description = "Username for the PostgreSQL database master user."
          type        = string
          default     = "odoo"
        }
        variable "postgres_db_password_secret_arn" {
          description = "ARN of the AWS Secrets Manager secret containing the PostgreSQL database master password."
          type        = string
          // No default, must be provided
        }
        variable "odoo_image_uri" {
          description = "Docker image URI for the Odoo application."
          type        = string
          // Example: "your-ecr-repo/dfr-odoo:latest"
        }
        variable "postgres_image_uri" {
          description = "Docker image URI for PostgreSQL (if deploying as container on EC2 instead of RDS)."
          type        = string
          default     = "postgres:15" // Or specific DFR custom image
        }
        variable "nginx_image_uri" {
          description = "Docker image URI for Nginx."
          type        = string
          // Example: "your-ecr-repo/dfr-nginx:latest"
        }
        variable "backup_s3_bucket_name_prefix" {
          description = "Prefix for the S3 bucket used for backups. A unique suffix will be appended."
          type        = string
          default     = "dfr-backups"
        }
        variable "domain_name" {
          description = "The domain name for accessing the DFR instance (e.g., dfr.example.com)."
          type        = string
          nullable    = true // May not be available/used in all envs
          default     = null
        }
        variable "ssl_certificate_arn" {
          description = "ARN of the ACM SSL certificate for the domain name."
          type        = string
          nullable    = true
          default     = null
        }
        variable "deploy_managed_db_service" {
          description = "Flag to deploy RDS (true) or PostgreSQL in Docker container on EC2 (false)."
          type        = bool
          default     = true
        }
        // Add more variables for SSH keys, desired counts for instances, etc.
        

2.  **`main.tf`**
    *   **Purpose:** Define and provision AWS resources for the DFR stack.
    *   **Logic Outline:**
        *   **Networking:**
            *   `aws_vpc`, `aws_subnet` (public, private across multiple AZs), `aws_internet_gateway`, `aws_nat_gateway` (or NAT instance), `aws_route_table`, `aws_route_table_association`.
        *   **Security Groups:**
            *   `aws_security_group` for Load Balancer (HTTPS inbound).
            *   `aws_security_group` for Nginx instances (HTTP/HTTPS from LB, SSH from bastion/admin).
            *   `aws_security_group` for Odoo instances (Odoo port from Nginx SG, SSH from bastion/admin).
            *   `aws_security_group` for PostgreSQL (RDS or EC2 container) (PostgreSQL port from Odoo SG).
        *   **IAM Roles and Policies:**
            *   `aws_iam_role` and `aws_iam_policy` / `aws_iam_role_policy_attachment` for EC2 instances (e.g., S3 access for backups, CloudWatch logs, Secrets Manager access).
            *   `aws_iam_role` for RDS if specific integrations are needed.
        *   **Compute (EC2 or ECS/EKS - assuming EC2 for simpler initial setup with Ansible configuration):**
            *   `aws_instance` for Odoo application servers (using `var.odoo_image_uri` if pre-baked AMI, otherwise base AMI for Ansible provisioning).
            *   `aws_instance` for Nginx reverse proxy servers (using `var.nginx_image_uri` if pre-baked AMI).
            *   Consider `aws_launch_template` and `aws_autoscaling_group` for scalability and resilience.
        *   **Database:**
            *   Conditional resource: `aws_db_instance` for RDS PostgreSQL if `var.deploy_managed_db_service` is true. Configure with `var.postgres_instance_class`, `var.postgres_allocated_storage`, `var.postgres_db_name`, `var.postgres_db_username`, fetch password from Secrets Manager using `aws_secretsmanager_secret_version` data source.
            *   If `var.deploy_managed_db_service` is false, PostgreSQL will be deployed as a Docker container by Ansible on a dedicated EC2 instance (provisioned similarly to Odoo instances).
        *   **Load Balancer:**
            *   `aws_lb` (Application Load Balancer), `aws_lb_target_group` (pointing to Nginx instances), `aws_lb_listener` (HTTPS, using `var.ssl_certificate_arn`). HTTP to HTTPS redirect listener.
        *   **Storage (Backups):**
            *   `aws_s3_bucket` for database and filestore backups (e.g., `"${var.backup_s3_bucket_name_prefix}-${var.country_code}-${var.environment_name}"`).
            *   `aws_s3_bucket_policy` for secure access.
        *   **DNS (Optional, if managing Route 53 records):**
            *   `aws_route53_record` to point `var.domain_name` to the ALB DNS.

3.  **`outputs.tf`**
    *   **Purpose:** Expose key resource identifiers.
    *   **Logic (examples):**
        hcl
        output "alb_dns_name" {
          description = "DNS name of the Application Load Balancer."
          value       = aws_lb.main.dns_name // Assuming ALB is named 'main'
        }
        output "odoo_instance_ips" {
          description = "Private IP addresses of the Odoo EC2 instances."
          value       = [for instance in aws_instance.odoo_app : instance.private_ip] // Assuming instances are defined as aws_instance.odoo_app
        }
        output "nginx_instance_ips" {
          description = "Private IP addresses of the Nginx EC2 instances."
          value       = [for instance in aws_instance.nginx_proxy : instance.private_ip]
        }
        output "rds_endpoint_address" {
          description = "Endpoint address of the RDS PostgreSQL instance."
          value       = var.deploy_managed_db_service ? aws_db_instance.main_postgres[0].address : "N/A (PostgreSQL on EC2)"
        }
        output "backup_s3_bucket_id" {
          description = "ID of the S3 bucket for backups."
          value       = aws_s3_bucket.backups.id // Assuming S3 bucket is named 'backups'
        }
        // Add other relevant outputs
        

#### 4.1.3 Azure DFR Stack Module (`terraform/modules/azure_dfr_stack/`) - Placeholder
Structure similar to `aws_dfr_stack` but using Azure resources (`azurerm_resource_group`, `azurerm_virtual_network`, `azurerm_subnet`, `azurerm_network_security_group`, `azurerm_virtual_machine`, `azurerm_postgresql_flexible_server`, `azurerm_storage_blob_container`, `azurerm_application_gateway`, etc.).
-   `variables.tf`: Define Azure-specific variables (e.g., `location`, `vm_size`, `postgresql_sku_name`).
-   `main.tf`: Provision Azure resources.
-   `outputs.tf`: Output Azure resource identifiers.

#### 4.1.4 GCP DFR Stack Module (`terraform/modules/gcp_dfr_stack/`) - Placeholder
Structure similar to `aws_dfr_stack` but using GCP resources (`google_compute_network`, `google_compute_subnetwork`, `google_compute_firewall`, `google_compute_instance`, `google_sql_database_instance` for PostgreSQL, `google_storage_bucket`, `google_compute_health_check`, `google_compute_backend_service`, `google_compute_url_map`, `google_compute_target_http_proxy`, `google_compute_global_forwarding_rule`, etc.).
-   `variables.tf`: Define GCP-specific variables (e.g., `project_id`, `region`, `zone`, `machine_type`).
-   `main.tf`: Provision GCP resources.
-   `outputs.tf`: Output GCP resource identifiers.

#### 4.1.5 Environment Configurations (e.g., `terraform/environments/aws/ck_staging/`)
1.  **`main.tf`**
    *   **Purpose:** Instantiate the cloud-specific DFR stack module for a particular environment.
    *   **Logic:**
        hcl
        # Example for AWS CKI Staging
        module "cki_staging_dfr_aws" {
          source = "../../../modules/aws_dfr_stack"

          aws_region                      = var.aws_region_override // Or directly use a value
          environment_name                = "staging"
          country_code                    = "ck"
          vpc_cidr                        = "10.10.0.0/16" // CKI Staging specific
          odoo_instance_type              = "t3.large"     // CKI Staging specific
          postgres_instance_class         = "db.t3.large"  // CKI Staging specific
          postgres_db_password_secret_arn = var.cki_staging_db_password_secret_arn
          odoo_image_uri                  = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dfr-odoo-app:ck-staging-v1.0.1"
          nginx_image_uri                 = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dfr-nginx-proxy:ck-staging-v1.0.1"
          domain_name                     = "ck-staging.dfr.example.org"
          ssl_certificate_arn             = "arn:aws:acm:ap-southeast-2:123456789012:certificate/your-cert-id"
          // ... other environment-specific overrides
        }
        
    *   **Variables:** May define local variables or reference variables from `terraform.tfvars`.

2.  **`terraform.tfvars`**
    *   **Purpose:** Provide environment-specific values for variables.
    *   **Logic:** Key-value pairs.
        tfvars
        # Example for AWS CKI Staging
        # aws_region_override = "ap-southeast-2"
        # cki_staging_db_password_secret_arn = "arn:aws:secretsmanager:ap-southeast-2:123456789012:secret:cki-staging/db_password-xxxxxx"
        
    *   **Note:** Sensitive values like ARNs for secrets are better passed as environment variables or CI/CD variables rather than committed directly.

#### 4.1.6 Common Outputs (`terraform/modules/common_outputs.tf`) - Conceptual
This file is less about direct implementation and more about defining a standard for what outputs environment configurations should expose. For instance, an environment's `outputs.tf` (e.g., `terraform/environments/aws/ck_staging/outputs.tf`) would reference module outputs:
hcl
// terraform/environments/aws/ck_staging/outputs.tf
output "dfr_application_url" {
  description = "Main URL for the DFR application."
  value       = "https://${module.cki_staging_dfr_aws.alb_dns_name}" // Assuming ALB serves on domain_name
}

output "odoo_app_server_ips" {
  description = "IPs of the Odoo application servers."
  value       = module.cki_staging_dfr_aws.odoo_instance_ips
}
// ... and so on, mapping to the module's actual outputs.


### 4.2 Ansible Configuration (`ansible/`)

#### 4.2.1 Global Files
1.  **`ansible/ansible.cfg`**
    *   **Purpose:** Global Ansible settings.
    *   **Logic:**
        ini
        [defaults]
        inventory          = ./inventories/
        remote_user        = ubuntu ; Default, can be overridden by inventory or playbook
        private_key_file   = ~/.ssh/dfr_key ; Example, adjust as needed
        roles_path         = ./roles
        log_path           = ./ansible.log
        host_key_checking  = False ; For dev/testing, set to True for production
        forks              = 5
        deprecation_warnings = False

        [privilege_escalation]
        become            = True
        become_method     = sudo
        become_user       = root
        become_ask_pass   = False
        

#### 4.2.2 Inventories (e.g., `ansible/inventories/aws_ck_staging_inventory.ini`)
*   **Purpose:** Define target hosts for Ansible.
*   **Logic:**
    *   Static inventory for VMs. For resources provisioned by Terraform, IP addresses or DNS names can be populated from Terraform outputs.
    *   A dynamic inventory script (e.g., using AWS SDK `boto3`) is highly recommended for cloud environments to automatically fetch instances based on tags.
    *   **Example (static, to be replaced by dynamic or populated from Terraform):**
        ini
        [odoo_app_servers]
        # dfr-odoo-ck-staging-01 ansible_host=<terraform_output_odoo_ip_1> ansible_user=ubuntu
        # dfr-odoo-ck-staging-02 ansible_host=<terraform_output_odoo_ip_2> ansible_user=ubuntu

        [postgres_db_servers] ; Only if deploying PostgreSQL on EC2 via Ansible
        # dfr-pg-ck-staging-01 ansible_host=<terraform_output_pg_ip_1> ansible_user=ubuntu

        [nginx_servers]
        # dfr-nginx-ck-staging-01 ansible_host=<terraform_output_nginx_ip_1> ansible_user=ubuntu

        [all:vars]
        ansible_python_interpreter=/usr/bin/python3
        # Environment-specific variables can be defined here or in group_vars/host_vars
        # odoo_image_tag = "ck-staging-v1.0.1"
        # nginx_image_tag = "ck-staging-v1.0.1"
        # postgres_image_tag = "15-alpine"
        # odoo_db_host = "<terraform_output_rds_endpoint_or_pg_ip>"
        # odoo_db_port = 5432
        # odoo_db_user = "odoo"
        # odoo_db_password = "{{ lookup('aws_secretsmanager', 'cki-staging/db_password', region='ap-southeast-2') }}" # Example of fetching from Secrets Manager
        # odoo_admin_password = "{{ lookup('aws_secretsmanager', 'cki-staging/odoo_admin_password', region='ap-southeast-2') }}"
        
    *   **Dynamic Inventory (Conceptual):** A Python script using `boto3` to query EC2 instances based on tags (e.g., `Environment=cki-staging`, `Role=odoo-app`) and output JSON in Ansible's dynamic inventory format.

#### 4.2.3 Ansible Roles (`ansible/roles/`)

1.  **Role: `common`** (New, not in file structure, but good practice)
    *   `tasks/main.yml`: OS hardening, common packages (python3-pip, common utilities), set timezone, configure NTP.
2.  **Role: `docker`** (`ansible/roles/docker/tasks/main.yml`)
    *   **Purpose:** Install Docker and Docker Compose.
    *   **Tasks:**
        *   Add Docker GPG key and repository.
        *   Install Docker Engine (e.g., `docker-ce`, `docker-ce-cli`, `containerd.io`).
        *   Install Docker Compose (from GitHub releases or pip).
        *   Start and enable Docker service.
        *   (Optional) Add `remote_user` to the `docker` group to run Docker commands without sudo (requires logout/login or new shell).
3.  **Role: `odoo_app_config`** (`ansible/roles/odoo_app_config/tasks/main.yml`)
    *   **Purpose:** Deploy and configure Odoo application container.
    *   **Variables (defined in `vars/main.yml` or passed via playbook):**
        *   `odoo_image_name`: e.g., "your-repo/dfr-odoo"
        *   `odoo_image_tag`: e.g., "latest" or specific version
        *   `odoo_container_name`: e.g., "dfr_odoo_app"
        *   `odoo_filestore_path`: Host path for Odoo filestore volume.
        *   `odoo_custom_addons_path`: Host path for custom addons volume.
        *   `odoo_config_path`: Host path for `odoo.conf` if mounted.
        *   `odoo_env_vars`: Dictionary of environment variables (DB connection, admin password, etc.).
        *   `odoo_ports`: List of port mappings (e.g., "8069:8069").
    *   **Tasks:**
        *   Create host directories for Odoo filestore, custom addons, config.
        *   Set appropriate permissions on these directories.
        *   Use `community.docker.docker_image` to pull the Odoo image.
        *   Use `community.docker.docker_container` to run the Odoo container, mounting volumes, setting environment variables (including `HOST`, `PORT`, `USER`, `PASSWORD` for PostgreSQL, `ADMIN_PASSWD`), and mapping ports.
4.  **Role: `postgres_db_config`** (`ansible/roles/postgres_db_config/tasks/main.yml`)
    *   **Purpose:** Deploy and configure PostgreSQL container (if not using RDS).
    *   **Variables:**
        *   `postgres_image_name`: e.g., "postgres"
        *   `postgres_image_tag`: e.g., "15-alpine"
        *   `postgres_container_name`: e.g., "dfr_postgres_db"
        *   `postgres_data_path`: Host path for PostgreSQL data volume.
        *   `postgres_env_vars`: Dict for `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.
        *   `postgres_ports`: e.g., "5432:5432".
    *   **Tasks:**
        *   Create host directory for PostgreSQL data.
        *   Set permissions.
        *   Pull PostgreSQL image using `community.docker.docker_image`.
        *   Run PostgreSQL container using `community.docker.docker_container`, mounting data volume, setting environment variables.
5.  **Role: `nginx` (or `reverse_proxy_config`)** (`ansible/roles/nginx/tasks/main.yml`)
    *   **Purpose:** Install and configure Nginx as a reverse proxy.
    *   **Variables:**
        *   `nginx_image_name`: e.g., "nginx" (if running as container) or ensure Nginx package.
        *   `nginx_image_tag`: e.g., "latest"
        *   `nginx_container_name`: e.g., "dfr_nginx_proxy"
        *   `odoo_app_upstream_host`: Hostname/IP of the Odoo app server(s).
        *   `odoo_app_upstream_port`: Port Odoo is listening on (e.g., 8069).
        *   `server_domain_name`: e.g., "dfr.example.com"
        *   `ssl_certificate_path_on_host`: Path to SSL certificate on the Nginx host.
        *   `ssl_certificate_key_path_on_host`: Path to SSL private key on the Nginx host.
        *   `use_lets_encrypt`: Boolean, if true, tasks for Certbot will be included.
    *   **Tasks:**
        *   Install Nginx (if not using containerized Nginx).
        *   Deploy Nginx configuration template (`nginx.conf.j2`) for Odoo reverse proxy (proxy pass to Odoo, handle longpolling, websockets, static assets, SSL termination).
            *   **`templates/nginx.conf.j2`:**
                nginx
                server {
                    listen 80;
                    server_name {{ server_domain_name }};
                    # Redirect HTTP to HTTPS
                    location / {
                        return 301 https://$host$request_uri;
                    }
                }

                server {
                    listen 443 ssl http2;
                    server_name {{ server_domain_name }};

                    ssl_certificate {{ ssl_certificate_path_on_host_container_path_if_docker }}; // Adjust path if Nginx is containerized
                    ssl_certificate_key {{ ssl_certificate_key_path_on_host_container_path_if_docker }};
                    # Add other SSL best practices (protocols, ciphers, HSTS)

                    # Odoo Proxy Configuration
                    proxy_buffers 16 64k;
                    proxy_buffer_size 128k;
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    location / {
                        proxy_pass http://{{ odoo_app_upstream_host }}:{{ odoo_app_upstream_port }};
                        proxy_redirect off;
                    }

                    location /longpolling {
                        proxy_pass http://{{ odoo_app_upstream_host }}:8072; # Or correct longpolling port
                        proxy_read_timeout 3600;
                    }

                    # Cache static files
                    location ~* /web/static/ {
                        proxy_cache_valid 200 302 60m;
                        proxy_buffering on;
                        expires 864000; # 10 days
                        proxy_pass http://{{ odoo_app_upstream_host }}:{{ odoo_app_upstream_port }};
                    }
                }
                
        *   If `use_lets_encrypt` is true: include tasks to install Certbot and obtain/renew certificates.
        *   Enable Nginx site configuration and restart/reload Nginx service.
        *   If running Nginx as a container: use `community.docker.docker_container` with appropriate volume mounts for configs and certs.
6.  **Role: `backup_config`** (Conceptual, tasks to be integrated into playbooks or a dedicated role)
    *   **Tasks:**
        *   Install backup tools (e.g., `postgresql-client` for `pg_dump`, `aws-cli` for S3 sync).
        *   Create backup scripts (e.g., shell script for `pg_dump` and Odoo filestore backup).
        *   Set up cron jobs to execute backup scripts.
        *   Configure log rotation for backup logs.
7.  **Role: `monitoring_config`** (Conceptual, tasks to be integrated into playbooks or a dedicated role)
    *   **Tasks:**
        *   Install monitoring agents (e.g., Prometheus `node_exporter`, Telegraf, Zabbix agent).
        *   Configure agents to point to the central monitoring server.
        *   Start and enable agent services.

#### 4.2.4 Ansible Playbooks (`ansible/playbooks/`)

1.  **`pb_provision_dfr_stack_vm.yml`**
    *   **Purpose:** Main playbook for setting up DFR stack on VMs.
    *   **Logic:**
        yaml
        ---
        - name: Provision Common OS Base
          hosts: all # Or specific groups like odoo_app_servers,nginx_servers,postgres_db_servers
          become: true
          roles:
            - role: common
            - role: docker

        - name: Provision PostgreSQL Database Server (if on VM)
          hosts: postgres_db_servers # This group is relevant if not using RDS
          become: true
          vars_files:
            - ../group_vars/{{ inventory_hostname }}.yml # Or general env vars
            - ../vault.yml # For secrets
          roles:
            - role: postgres_db_config
          when: not deploy_managed_db_service_flag | default(true) # deploy_managed_db_service_flag comes from inventory or extra-vars

        - name: Provision Odoo Application Servers
          hosts: odoo_app_servers
          become: true
          vars_files:
            - ../group_vars/{{ inventory_hostname }}.yml
            - ../vault.yml
          roles:
            - role: odoo_app_config
          vars:
            odoo_db_host: "{{ hostvars[groups['postgres_db_servers'][0]]['ansible_default_ipv4']['address'] if groups['postgres_db_servers'] and not deploy_managed_db_service_flag | default(true) else terraform_rds_endpoint }}"
            # terraform_rds_endpoint would be an extra-var passed from TF output or inventory

        - name: Provision Nginx Reverse Proxy Servers
          hosts: nginx_servers
          become: true
          vars_files:
            - ../group_vars/{{ inventory_hostname }}.yml
            - ../vault.yml
          roles:
            - role: nginx
          vars:
            odoo_app_upstream_host: "{{ hostvars[groups['odoo_app_servers'][0]]['ansible_default_ipv4']['address'] }}" # Simple example, needs to handle multiple Odoo servers for LB
        

2.  **`pb_configure_backups.yml`**
    *   **Purpose:** Configure backups.
    *   **Logic:**
        yaml
        ---
        - name: Configure Database Backups
          hosts: postgres_db_servers # Or Odoo app servers if they manage pg_dump locally for RDS
          become: true
          roles:
            - role: backup_config # This role would contain DB backup tasks
          vars:
            backup_type: "database"
            # Add S3 bucket names, credentials (from vault)

        - name: Configure Odoo Filestore Backups
          hosts: odoo_app_servers
          become: true
          roles:
            - role: backup_config # This role would contain filestore backup tasks
          vars:
            backup_type: "filestore"
            odoo_filestore_path: "/opt/odoo/data/filestore" # Example
            # Add S3 bucket names, credentials
        

3.  **`pb_configure_monitoring.yml`**
    *   **Purpose:** Configure monitoring agents.
    *   **Logic:**
        yaml
        ---
        - name: Install and Configure Monitoring Agents
          hosts: all # Or specific groups
          become: true
          roles:
            - role: monitoring_config
          vars:
            monitoring_server_ip: "x.x.x.x" # Central monitoring server
            # Other agent specific configs
        

### 4.3 Utility Scripts (`scripts/`)

1.  **`scripts/terraform_apply.sh`**
    *   **Purpose:** Wrapper for `terraform apply`.
    *   **Logic:**
        bash
        #!/bin/bash
        set -e # Exit immediately if a command exits with a non-zero status.

        ENVIRONMENT_PATH=$1
        TF_ACTION=${2:-apply} # Default to apply, can pass plan, destroy etc.

        if [ -z "$ENVIRONMENT_PATH" ]; then
          echo "Usage: $0 <terraform_environment_path> [plan|apply|destroy]"
          echo "Example: $0 terraform/environments/aws/ck_staging"
          exit 1
        fi

        if [ ! -d "$ENVIRONMENT_PATH" ]; then
          echo "Error: Environment path '$ENVIRONMENT_PATH' does not exist."
          exit 1
        fi

        echo "==> Navigating to $ENVIRONMENT_PATH"
        cd "$ENVIRONMENT_PATH"

        echo "==> Running terraform init..."
        terraform init -reconfigure # Or just init if backend is stable

        TFVARS_FILE="terraform.tfvars"
        if [ ! -f "$TFVARS_FILE" ]; then
            echo "Warning: $TFVARS_FILE not found in $ENVIRONMENT_PATH. Using defaults."
            TFVARS_CMD=""
        else
            TFVARS_CMD="-var-file=$TFVARS_FILE"
        fi
        
        echo "==> Running terraform $TF_ACTION for environment: $(basename "$ENVIRONMENT_PATH")..."
        if [ "$TF_ACTION" == "apply" ] || [ "$TF_ACTION" == "destroy" ]; then
          terraform "$TF_ACTION" $TFVARS_CMD -auto-approve
        else
          terraform "$TF_ACTION" $TFVARS_CMD
        fi

        echo "==> Terraform $TF_ACTION completed for $ENVIRONMENT_PATH."
        cd - > /dev/null # Return to previous directory
        

2.  **`scripts/ansible_run_playbook.sh`**
    *   **Purpose:** Wrapper for `ansible-playbook`.
    *   **Logic:**
        bash
        #!/bin/bash
        set -e

        PLAYBOOK_PATH=$1
        INVENTORY_PATH=$2
        EXTRA_VARS=$3 # Optional: e.g., "key1=value1 key2=value2" or "@vars.json"

        if [ -z "$PLAYBOOK_PATH" ] || [ -z "$INVENTORY_PATH" ]; then
          echo "Usage: $0 <ansible_playbook_path> <ansible_inventory_path> [extra_vars]"
          echo "Example: $0 ansible/playbooks/pb_provision_dfr_stack_vm.yml ansible/inventories/aws_ck_staging_inventory.ini"
          exit 1
        fi

        if [ ! -f "$PLAYBOOK_PATH" ]; then
          echo "Error: Playbook '$PLAYBOOK_PATH' not found."
          exit 1
        fi

        if [ ! -f "$INVENTORY_PATH" ] && [ ! -x "$INVENTORY_PATH" ]; then # Check if file or executable script
          echo "Error: Inventory '$INVENTORY_PATH' not found or not executable (for dynamic inventory)."
          exit 1
        fi
        
        ANSIBLE_CMD="ansible-playbook -i \"$INVENTORY_PATH\" \"$PLAYBOOK_PATH\""

        if [ -n "$EXTRA_VARS" ]; then
          ANSIBLE_CMD="$ANSIBLE_CMD --extra-vars \"$EXTRA_VARS\""
        fi

        echo "==> Running Ansible playbook: $PLAYBOOK_PATH with inventory: $INVENTORY_PATH"
        eval "$ANSIBLE_CMD" # Use eval to correctly parse extra_vars if it contains spaces

        echo "==> Ansible playbook $PLAYBOOK_PATH completed."
        

## 5. Data Design
This repository primarily deals with configuration data for Terraform and Ansible, not application data models. Key data points managed include:
-   Terraform state files (managed by Terraform backend).
-   Terraform variable files (`.tfvars`) containing environment-specific parameters.
-   Ansible inventory files defining hosts and groups.
-   Ansible variable files (`group_vars/`, `host_vars/`, playbook `vars:`) for configuration parameters.
-   Secrets (passwords, API keys) should ideally be managed by a dedicated secrets management tool (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) and fetched by Terraform/Ansible at runtime, rather than stored in version control. Placeholders or ARNs to secrets will be in version-controlled files.

## 6. Deployment Strategy
1.  **Prerequisites:**
    *   Terraform CLI installed.
    *   Ansible installed.
    *   Cloud provider CLI configured with necessary credentials (or IAM roles/service principals set up).
    *   Access to Docker registry with DFR application images.
    *   SSH key pair for accessing VMs (if applicable).
2.  **Terraform Provisioning:**
    *   Select the target environment (e.g., `terraform/environments/aws/ck_staging`).
    *   Configure `backend.tf` if not already set up.
    *   Populate or ensure `terraform.tfvars` has the correct values for the environment (or pass variables via CLI/env vars).
    *   Run `scripts/terraform_apply.sh <environment_path> plan` to review changes.
    *   Run `scripts/terraform_apply.sh <environment_path> apply` to provision infrastructure.
    *   Terraform outputs (e.g., instance IPs, DNS names) will be used to populate the Ansible inventory.
3.  **Ansible Configuration:**
    *   Update the Ansible inventory file for the target environment (e.g., `ansible/inventories/aws_ck_staging_inventory.ini`) with IP addresses/hostnames from Terraform outputs. Dynamic inventory is preferred.
    *   Ensure `group_vars` or `host_vars` contain necessary configurations.
    *   Ensure Ansible vault is used for sensitive data if not fetched from cloud secrets managers.
    *   Run `scripts/ansible_run_playbook.sh <playbook_path> <inventory_path> [extra_vars]` to apply configurations.
        *   Example: `scripts/ansible_run_playbook.sh ansible/playbooks/pb_provision_dfr_stack_vm.yml ansible/inventories/aws_ck_staging_inventory.ini`
4.  **Containerized Deployment:** Ansible playbooks will orchestrate pulling Docker images and running Odoo, PostgreSQL (if not RDS), and Nginx containers with the correct configurations, volume mounts, and network settings as defined in the respective Ansible roles.

## 7. Security Considerations
-   **Principle of Least Privilege:** IAM roles and policies for Terraform and cloud resources will grant only necessary permissions. Ansible users will have minimal required privileges.
-   **Network Security:** Security groups and firewall rules will restrict traffic to only necessary ports and sources.
-   **Secrets Management:** Sensitive data like passwords, API keys will be managed using cloud provider secret management services (e.g., AWS Secrets Manager, Azure Key Vault) or HashiCorp Vault, and accessed by Terraform/Ansible dynamically. Ansible Vault will be used for secrets managed directly within Ansible.
-   **SSH Access:** SSH access to VMs will be restricted, ideally through bastion hosts or specific IP whitelists, using key-based authentication.
-   **HTTPS Enforcement:** Nginx will be configured for SSL/TLS termination, enforcing HTTPS for all DFR application traffic.
-   **Regular Updates:** Underlying OS, Docker, Nginx, PostgreSQL, and Odoo dependencies should be regularly patched as part of maintenance (may be handled by separate Ansible playbooks or operational procedures).
-   **IaC Security:** Terraform state files should be secured (encryption at rest, access controls on the backend storage).

## 8. Future Considerations / Scalability
-   **Dynamic Inventory:** Implement dynamic Ansible inventory scripts for AWS, Azure, and GCP.
-   **Container Orchestration:** For larger deployments, consider migrating EC2 instance management to container orchestration platforms like Amazon ECS, EKS, Azure AKS, or Google GKE. Terraform modules would need to be updated to support this.
-   **Advanced Backup/DR:** Implement more sophisticated DR strategies, potentially involving cross-region replication of data and infrastructure.
-   **Centralized Logging & Monitoring:** Enhance integration with centralized logging (e.g., ELK stack, CloudWatch Logs) and monitoring solutions (Prometheus/Grafana, Datadog, cloud provider specific tools).
-   **Automated SSL Certificate Renewal:** Fully automate SSL certificate renewal using Certbot or cloud provider certificate managers.
-   **Terraform Workspaces:** Utilize Terraform workspaces more extensively for managing multiple instances of the same environment (e.g., multiple dev environments).

This SDS provides a blueprint for the DFR_INFRA_CONFIG repository. Specific details within Terraform resource blocks and Ansible tasks will be implemented according to best practices for each technology and cloud provider, aligning with the DFR project's requirements.