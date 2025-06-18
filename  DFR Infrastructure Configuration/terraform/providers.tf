terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "aws_region" {
  description = "Default AWS region for the provider. Can be overridden in environment configurations."
  type        = string
  nullable    = true
  default     = null # This encourages setting it at the environment or module level.
}

variable "gcp_project_id" {
  description = "Default GCP project ID for the provider. Can be overridden."
  type        = string
  nullable    = true
  default     = null
}

variable "gcp_region" {
  description = "Default GCP region for the provider. Can be overridden."
  type        = string
  nullable    = true
  default     = null
}

provider "aws" {
  region = var.aws_region
  # Credentials are expected to be configured via environment variables,
  # IAM roles for EC2/ECS, or shared credentials file (~/.aws/credentials).
}

provider "azurerm" {
  features {}
  # Credentials are expected to be configured via environment variables,
  # Azure CLI login, or a Service Principal.
  # Example:
  # subscription_id = var.azure_subscription_id
  # client_id       = var.azure_client_id
  # client_secret   = var.azure_client_secret
  # tenant_id       = var.azure_tenant_id
}

provider "google" {
  # Credentials are expected to be configured via environment variables (GOOGLE_CREDENTIALS),
  # gcloud CLI, or service account key file.
  project = var.gcp_project_id
  region  = var.gcp_region
  # Example:
  # credentials = file(var.gcp_service_account_key_path)
}