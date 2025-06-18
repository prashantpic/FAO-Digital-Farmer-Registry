# This file defines a conceptual standard for outputs that environment configurations
# (e.g., terraform/environments/aws/ck_staging/outputs.tf) should expose.
# The actual values would reference outputs from the specific cloud provider module instance.

output "dfr_application_url" {
  description = "Main URL for accessing the DFR application. Typically the DNS of the load balancer."
  # Example value that an environment's output.tf might use:
  # value       = "https://${module.<cloud_stack_module_instance_name>.alb_dns_name}"
  # value       = "https://<your_domain_name>"
  value       = "Placeholder: e.g., https://module.aws_dfr_stack.alb_dns_name or https://module.azure_dfr_stack.app_gateway_dns_name"
}

output "odoo_app_server_ips" {
  description = "IP addresses of the Odoo application servers. Useful for direct access or troubleshooting (if allowed by security groups)."
  # Example value that an environment's output.tf might use:
  # value       = module.<cloud_stack_module_instance_name>.odoo_instance_ips
  value       = "Placeholder: e.g., module.aws_dfr_stack.odoo_instance_ips"
}

output "nginx_server_ips" {
  description = "IP addresses of the Nginx reverse proxy servers."
  # Example value that an environment's output.tf might use:
  # value       = module.<cloud_stack_module_instance_name>.nginx_instance_ips
  value       = "Placeholder: e.g., module.aws_dfr_stack.nginx_instance_ips"
}

output "database_endpoint_address" {
  description = "Endpoint address of the database server (e.g., RDS endpoint or IP of EC2 hosting PostgreSQL)."
  # Example value that an environment's output.tf might use:
  # value       = module.<cloud_stack_module_instance_name>.rds_endpoint_address # or similar for other DB types/clouds
  value       = "Placeholder: e.g., module.aws_dfr_stack.rds_endpoint_address or IP of self-hosted DB"
}

output "database_port" {
  description = "Port number for the database server."
  # Example value that an environment's output.tf might use:
  # value       = module.<cloud_stack_module_instance_name>.rds_port # or fixed value like 5432
  value       = "5432" # Default for PostgreSQL
}

output "backup_storage_location_id" {
  description = "Identifier for the backup storage (e.g., S3 bucket ID, Azure Blob Container name)."
  # Example value that an environment's output.tf might use:
  # value       = module.<cloud_stack_module_instance_name>.backup_s3_bucket_id
  value       = "Placeholder: e.g., module.aws_dfr_stack.backup_s3_bucket_id"
}

# Add other common outputs as standard requirements for DFR deployments:
# output "vpc_id" {
#   description = "ID of the Virtual Private Cloud or VNet."
#   value       = "Placeholder: e.g., module.<cloud_stack_module_instance_name>.vpc_id"
# }

# output "public_subnet_ids" {
#   description = "List of Public Subnet IDs."
#   value       = "Placeholder: e.g., module.<cloud_stack_module_instance_name>.public_subnet_ids"
# }

# output "private_subnet_ids" {
#   description = "List of Private Subnet IDs."
#   value       = "Placeholder: e.g., module.<cloud_stack_module_instance_name>.private_subnet_ids"
# }