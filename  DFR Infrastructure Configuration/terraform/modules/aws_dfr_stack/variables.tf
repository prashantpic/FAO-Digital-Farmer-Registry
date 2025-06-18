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
  description = "List of CIDR blocks for public subnets. Should correspond to availability_zones."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets. Should correspond to availability_zones."
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "availability_zones" {
  description = "List of Availability Zones to use for subnets. If empty, default AZs in the region will be used. Ensure count matches subnet CIDR lists."
  type        = list(string)
  default     = []
}

variable "odoo_instance_type" {
  description = "EC2 instance type for Odoo application server."
  type        = string
  default     = "t3.medium"
}

variable "odoo_instance_count" {
  description = "Number of Odoo EC2 instances to launch."
  type        = number
  default     = 1
}

variable "nginx_instance_type" {
  description = "EC2 instance type for Nginx reverse proxy server."
  type        = string
  default     = "t3.small"
}

variable "nginx_instance_count" {
  description = "Number of Nginx EC2 instances to launch."
  type        = number
  default     = 1
}

variable "deploy_managed_db_service" {
  description = "Flag to deploy RDS (true) or PostgreSQL in Docker container on EC2 (false)."
  type        = bool
  default     = true
}

variable "postgres_ec2_instance_type" {
  description = "EC2 instance type for PostgreSQL server if deploy_managed_db_service is false."
  type        = string
  default     = "t3.medium"
  # Only used if deploy_managed_db_service is false
}

variable "postgres_instance_class" {
  description = "RDS instance class for PostgreSQL if deploy_managed_db_service is true."
  type        = string
  default     = "db.t3.medium"
  # Only used if deploy_managed_db_service is true
}

variable "postgres_allocated_storage" {
  description = "Allocated storage for PostgreSQL RDS in GB (or EC2 volume size if on EC2)."
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
  # No default, must be provided. For EC2-based Postgres, Ansible will expect this password.
}

variable "odoo_image_uri" {
  description = "Docker image URI for the Odoo application (e.g., your-ecr-repo/dfr-odoo:latest). If deploying on EC2, Ansible will use this. If using pre-baked AMI, this might be for reference."
  type        = string
}

variable "postgres_image_uri" {
  description = "Docker image URI for PostgreSQL (if deploying as container on EC2 instead of RDS)."
  type        = string
  default     = "postgres:15" // Or specific DFR custom image
  # Only used if deploy_managed_db_service is false
}

variable "nginx_image_uri" {
  description = "Docker image URI for Nginx (e.g., your-ecr-repo/dfr-nginx:latest). If deploying on EC2, Ansible will use this. If using pre-baked AMI, this might be for reference."
  type        = string
}

variable "backup_s3_bucket_name_prefix" {
  description = "Prefix for the S3 bucket used for backups. A unique suffix (country-env) will be appended."
  type        = string
  default     = "dfr-backups"
}

variable "domain_name" {
  description = "The domain name for accessing the DFR instance (e.g., dfr.example.com). Used for ALB and Route 53."
  type        = string
  nullable    = true
  default     = null
}

variable "hosted_zone_id" {
  description = "Route 53 Hosted Zone ID to create DNS records in. Required if domain_name is set."
  type        = string
  nullable    = true
  default     = null
}

variable "ssl_certificate_arn" {
  description = "ARN of the ACM SSL certificate for the domain name. Required if domain_name is set for HTTPS ALB listener."
  type        = string
  nullable    = true
  default     = null
}

variable "ssh_key_name" {
  description = "Name of the EC2 SSH key pair to associate with instances for administrative access."
  type        = string
  nullable    = true
  default     = null
}

variable "admin_access_cidr" {
  description = "CIDR block allowed for SSH access to EC2 instances and potentially other management interfaces."
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING: Open to the world. Restrict this in production.
}

variable "tags" {
  description = "A map of tags to assign to all resources."
  type        = map(string)
  default     = {}
}

variable "ami_id_linux" {
  description = "Custom AMI ID for Linux instances. If not provided, will use latest Amazon Linux 2 or Ubuntu."
  type        = string
  default     = "" # Let AWS provider choose default or specify one e.g. based on region
}