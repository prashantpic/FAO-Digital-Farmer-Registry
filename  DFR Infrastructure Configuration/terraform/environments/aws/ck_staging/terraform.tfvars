# Example terraform.tfvars for AWS CKI Staging environment.
# These values override or provide defaults for variables defined in .tf files.
# Sensitive values like ARNs for secrets are better passed as environment variables
# or CI/CD variables rather than committed directly, even if this file is in .gitignore.
# The `cki_staging_db_password_secret_arn` is expected to be defined in a .tfvars file
# or passed as a command-line variable due to its sensitivity if not handled by CI/CD.

# aws_region_override = "ap-southeast-2"

# cki_staging_db_password_secret_arn = "arn:aws:secretsmanager:ap-southeast-2:123456789012:secret:cki-staging/db_password-xxxxxx"

# odoo_image_uri_cki_staging = "your-custom-ecr/dfr-odoo-app:ck-staging-custom-tag"
# nginx_image_uri_cki_staging = "your-custom-ecr/dfr-nginx-proxy:ck-staging-custom-tag"

# domain_name_cki_staging = "staging.ck.dfr.yourdomain.com"
# ssl_certificate_arn_cki_staging = "arn:aws:acm:ap-southeast-2:123456789012:certificate/your-staging-cert-id"

# Note:
# For actual deployment, ensure cki_staging_db_password_secret_arn is set.
# If you are not overriding variables defined with defaults in main.tf for this environment,
# you don't need to specify them here unless you want to change their values.