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
# Use -reconfigure if backend or provider versions might change often.
# For stable setups, simple 'terraform init' might suffice after the first run.
terraform init -reconfigure

TFVARS_FILE="terraform.tfvars"
TFVARS_CMD="" # Initialize TFVARS_CMD

if [ -f "$TFVARS_FILE" ]; then
    echo "Info: Using '$TFVARS_FILE' for variable definitions."
    TFVARS_CMD="-var-file=$TFVARS_FILE"
else
    echo "Warning: '$TFVARS_FILE' not found in $ENVIRONMENT_PATH. Using default variable values or those passed via other means (e.g., environment variables)."
fi

echo "==> Running terraform $TF_ACTION for environment: $(basename "$PWD")..."
# Using $PWD to get the current directory name after cd, which is the environment name.

if [ "$TF_ACTION" == "apply" ] || [ "$TF_ACTION" == "destroy" ]; then
  # For apply and destroy, -auto-approve is used as specified in SDS.
  # Ensure this is appropriate for your workflow; interactive approval is safer for production.
  terraform "$TF_ACTION" $TFVARS_CMD -auto-approve
elif [ "$TF_ACTION" == "plan" ]; then
  terraform "$TF_ACTION" $TFVARS_CMD
else
  # For other actions like validate, show, etc.
  terraform "$TF_ACTION" $TFVARS_CMD
fi

echo "==> Terraform $TF_ACTION completed for $ENVIRONMENT_PATH."
cd - > /dev/null # Return to previous directory silently