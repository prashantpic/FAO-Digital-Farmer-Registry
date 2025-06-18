# This file configures the Terraform backend, which determines how Terraform stores its state.
# State allows Terraform to map real-world resources to your configuration, keep track of metadata,
# and improve performance for large infrastructures.
# It is highly recommended to use a remote backend for any collaborative or production environment.

# Example for AWS S3 backend (uncomment and configure as needed)
# Ensure the S3 bucket and DynamoDB table (for locking) are created beforehand.
# terraform {
#   backend "s3" {
#     bucket         = "dfr-terraform-state-bucket-unique-name" # Replace with your unique S3 bucket name
#     key            = "dfr_infra_config/terraform.tfstate"     # Path to the state file in the bucket (can be environment-specific)
#     region         = "ap-southeast-2"                         # Replace with your AWS region
#     encrypt        = true                                     # Encrypts the state file at rest
#     dynamodb_table = "dfr-terraform-state-lock"              # DynamoDB table for state locking and consistency
#
#     # Optional: Configure profile if not using default AWS credentials
#     # profile = "your-aws-profile"
#
#     # Optional: Configure role_arn if using IAM role for state access
#     # role_arn = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateAccessRole"
#   }
# }

# Example for Azure Blob Storage backend (uncomment and configure as needed)
# Ensure the Azure Storage Account and Blob Container are created beforehand.
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "dfr-terraform-rg"            # Name of the Azure Resource Group
#     storage_account_name = "dfrterraformstateunique"     # Name of the Azure Storage Account (must be globally unique)
#     container_name       = "tfstate"                     # Name of the Blob Container
#     key                  = "dfr_infra_config/terraform.tfstate" # Path to the state file in the container
#
#     # Optional: Configure access using SAS token or Service Principal
#     # use_azuread_auth = true # If using Azure AD authentication
#     # Or for Service Principal:
#     # subscription_id = "your-subscription-id"
#     # client_id       = "your-service-principal-client-id"
#     # client_secret   = "your-service-principal-client-secret"
#     # tenant_id       = "your-azure-ad-tenant-id"
#   }
# }

# Example for Google Cloud Storage (GCS) backend (uncomment and configure as needed)
# Ensure the GCS bucket is created beforehand.
# terraform {
#   backend "gcs" {
#     bucket  = "dfr-terraform-state-bucket-unique-name" # Replace with your unique GCS bucket name
#     prefix  = "dfr_infra_config/terraform/state"       # Path prefix for state files in the bucket
#
#     # Optional: Configure credentials if not using Application Default Credentials
#     # credentials = "/path/to/your/gcp-service-account-key.json"
#   }
# }

# Note:
# 1. Backend configuration must be done before running `terraform init`.
# 2. If you change backend configuration, you may need to re-initialize with `terraform init -reconfigure`.
# 3. Sensitive data should not be hardcoded here. Use environment variables or other secure methods
#    for credentials if not relying on default provider credential chains.
# 4. Choose ONE backend configuration appropriate for your project.