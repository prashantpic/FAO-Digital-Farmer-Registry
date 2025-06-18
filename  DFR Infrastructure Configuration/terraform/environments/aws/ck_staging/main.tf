# Terraform configuration for the Cook Islands (CKI) Staging environment on AWS.
# This file instantiates the aws_dfr_stack module with CKI Staging specific parameters.

variable "aws_region_override" {
  description = "AWS region for the CKI Staging environment. Overrides module default."
  type        = string
  nullable    = true
  default     = null # If null, module default or provider default will be used.
}

variable "cki_staging_db_password_secret_arn" {
  description = "ARN of the AWS Secrets Manager secret for the CKI Staging PostgreSQL database master password."
  type        = string
  sensitive   = true
  # No default, this must be provided for RDS deployments.
}

variable "odoo_image_uri_cki_staging" {
  description = "Docker image URI for the Odoo application in CKI Staging."
  type        = string
  default     = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dfr-odoo-app:ck-staging-v1.0.1" # Example
}

variable "nginx_image_uri_cki_staging" {
  description = "Docker image URI for the Nginx reverse proxy in CKI Staging."
  type        = string
  default     = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/dfr-nginx-proxy:ck-staging-v1.0.1" # Example
}

variable "domain_name_cki_staging" {
  description = "Domain name for the CKI Staging DFR instance."
  type        = string
  default     = "ck-staging.dfr.example.org" # Example
}

variable "ssl_certificate_arn_cki_staging" {
  description = "ARN of the ACM SSL certificate for the CKI Staging domain name."
  type        = string
  nullable    = true
  default     = "arn:aws:acm:ap-southeast-2:123456789012:certificate/your-cert-id" # Example, replace with actual or set to null
}

module "cki_staging_dfr_aws" {
  source = "../../../modules/aws_dfr_stack"

  aws_region                      = var.aws_region_override != null ? var.aws_region_override : null # Uses module default if var.aws_region_override is null
  environment_name                = "staging"
  country_code                    = "ck"
  
  vpc_cidr                        = "10.10.0.0/16" // CKI Staging specific
  public_subnet_cidrs             = ["10.10.1.0/24", "10.10.2.0/24"] // CKI Staging specific
  private_subnet_cidrs            = ["10.10.101.0/24", "10.10.102.0/24"] // CKI Staging specific
  
  odoo_instance_type              = "t3.large"     // CKI Staging specific
  nginx_instance_type             = "t3.small"     // CKI Staging specific, can be adjusted
  
  deploy_managed_db_service       = true // Use RDS for this environment example
  postgres_instance_class         = "db.t3.large"  // CKI Staging specific
  postgres_db_password_secret_arn = var.cki_staging_db_password_secret_arn
  
  odoo_image_uri                  = var.odoo_image_uri_cki_staging
  nginx_image_uri                 = var.nginx_image_uri_cki_staging
  # postgres_image_uri is only used if deploy_managed_db_service is false

  domain_name                     = var.domain_name_cki_staging
  ssl_certificate_arn             = var.ssl_certificate_arn_cki_staging
  
  backup_s3_bucket_name_prefix    = "dfr-backups-ck-staging"

  # Example tags, can be expanded
  tags = {
    Project     = "DFR"
    Environment = "CK-Staging"
    ManagedBy   = "Terraform"
    Country     = "CK"
  }

  # availability_zones can be specified if needed, e.g., ["ap-southeast-2a", "ap-southeast-2b"]
  # Default AZs for the region will be used if not specified in the module or here.
}

# Define outputs for this specific environment based on the module's outputs
output "cki_staging_alb_dns_name" {
  description = "DNS name of the Application Load Balancer for CKI Staging."
  value       = module.cki_staging_dfr_aws.alb_dns_name
}

output "cki_staging_dfr_application_url" {
  description = "Main URL for the DFR application in CKI Staging."
  value       = "https://${module.cki_staging_dfr_aws.alb_dns_name}" # Assumes ALB serves on domain_name if domain_name is configured with Route53
  # If domain_name and Route53 are not managed by this Terraform, use ALB DNS directly or manually configure DNS.
}

output "cki_staging_odoo_instance_ips" {
  description = "Private IP addresses of the Odoo EC2 instances for CKI Staging."
  value       = module.cki_staging_dfr_aws.odoo_instance_ips
}

output "cki_staging_nginx_instance_ips" {
  description = "Private IP addresses of the Nginx EC2 instances for CKI Staging."
  value       = module.cki_staging_dfr_aws.nginx_instance_ips
}

output "cki_staging_rds_endpoint_address" {
  description = "Endpoint address of the RDS PostgreSQL instance for CKI Staging."
  value       = module.cki_staging_dfr_aws.rds_endpoint_address
}

output "cki_staging_backup_s3_bucket_id" {
  description = "ID of the S3 bucket for backups for CKI Staging."
  value       = module.cki_staging_dfr_aws.backup_s3_bucket_id
}