#!/bin/bash
# Generic shell script for deploying applications.
#
# Purpose: Provides a common interface for application deployment logic,
#          abstracting specific deployment tool commands.
#
# Inputs/Parameters (Environment Variables or Arguments):
#   DEPLOYMENT_ENV: (Required, e.g., staging, production) Target deployment environment.
#   APP_NAME: (Required) Name of the application to deploy (e.g., dfr-odoo-backend, dfr-mobile-app-distribution).
#   IMAGE_TAG_OR_ARTIFACT_PATH: (Required) Docker image tag (for containerized apps) or path to the deployment artifact (for mobile apps).
#   CONFIG_FILE_PATH: (Optional) Path to an environment-specific configuration file (e.g., docker-compose.yml, Kubernetes manifest).
#   DEPLOYMENT_TYPE: (Required, e.g., docker-compose, kubernetes, s3-upload, app-store-deploy) Type of deployment.
#   KUBE_CONTEXT: (Optional) Kubernetes context if DEPLOYMENT_TYPE is kubernetes.
#   AWS_PROFILE: (Optional) AWS CLI profile if DEPLOYMENT_TYPE is s3-upload or involves AWS.
#   GCP_PROJECT: (Optional) GCP project ID if deployment involves GCP.
#   APP_NAME_SERVICE_IN_COMPOSE_IF_SPECIFIC: (Optional) Specific service name in docker-compose file if deploying only one service from a multi-service file.

set -e
set -o pipefail

# --- Parameter Validation ---
if [ -z "$DEPLOYMENT_ENV" ]; then
    echo "Error: DEPLOYMENT_ENV is required." >&2
    exit 1
fi
if [ -z "$APP_NAME" ]; then
    echo "Error: APP_NAME is required." >&2
    exit 1
fi
if [ -z "$IMAGE_TAG_OR_ARTIFACT_PATH" ]; then
    echo "Error: IMAGE_TAG_OR_ARTIFACT_PATH is required." >&2
    exit 1
fi
if [ -z "$DEPLOYMENT_TYPE" ]; then
    echo "Error: DEPLOYMENT_TYPE is required." >&2
    exit 1
fi

# --- Main Logic ---
echo "Starting application deployment..."
echo "Deployment Environment: ${DEPLOYMENT_ENV}"
echo "Application Name: ${APP_NAME}"
echo "Image Tag or Artifact Path: ${IMAGE_TAG_OR_ARTIFACT_PATH}"
echo "Deployment Type: ${DEPLOYMENT_TYPE}"
[ -n "$CONFIG_FILE_PATH" ] && echo "Config File Path: ${CONFIG_FILE_PATH}"
[ -n "$KUBE_CONTEXT" ] && echo "Kubernetes Context: ${KUBE_CONTEXT}"
[ -n "$AWS_PROFILE" ] && echo "AWS Profile: ${AWS_PROFILE}"
[ -n "$GCP_PROJECT" ] && echo "GCP Project: ${GCP_PROJECT}"

# Load environment-specific configurations from CONFIG_FILE_PATH if provided
# This script assumes that if CONFIG_FILE_PATH is needed, it contains all necessary details
# like image versions etc., or that IMAGE_TAG_OR_ARTIFACT_PATH is used to update these files
# before deployment (e.g. sed command to update image tag in a k8s manifest).
# For simplicity, this script will directly use CONFIG_FILE_PATH where applicable.

case "$DEPLOYMENT_TYPE" in
    docker-compose)
        echo "Executing docker-compose deployment for ${APP_NAME}..."
        if [ -z "$CONFIG_FILE_PATH" ]; then
            echo "Error: CONFIG_FILE_PATH (path to docker-compose file) is required for docker-compose deployment." >&2
            exit 1
        fi
        if [ ! -f "$CONFIG_FILE_PATH" ]; then
            echo "Error: Docker compose file '$CONFIG_FILE_PATH' not found." >&2
            exit 1
        fi

        echo "Pulling latest images referenced in ${CONFIG_FILE_PATH}..."
        docker-compose -f "${CONFIG_FILE_PATH}" pull ${APP_NAME_SERVICE_IN_COMPOSE_IF_SPECIFIC}
        if [ $? -ne 0 ]; then
            echo "Error: docker-compose pull failed." >&2
            exit 1
        fi

        echo "Bringing services up with docker-compose..."
        # Note: IMAGE_TAG_OR_ARTIFACT_PATH might need to be injected into the docker-compose file
        # or set as an environment variable that the compose file uses, e.g. DFR_IMAGE_TAG=${IMAGE_TAG_OR_ARTIFACT_PATH}
        # This script assumes the compose file is already configured or uses environment variables.
        docker-compose -f "${CONFIG_FILE_PATH}" up -d --remove-orphans ${APP_NAME_SERVICE_IN_COMPOSE_IF_SPECIFIC}
        if [ $? -ne 0 ]; then
            echo "Error: docker-compose up failed." >&2
            exit 1
        fi
        echo "Docker-compose deployment successful."
        ;;

    kubernetes)
        echo "Executing kubernetes deployment for ${APP_NAME}..."
        if [ -z "$CONFIG_FILE_PATH" ]; then
            echo "Error: CONFIG_FILE_PATH (path to Kubernetes manifest or kustomization.yaml) is required for kubernetes deployment." >&2
            exit 1
        fi
        if [ ! -e "$CONFIG_FILE_PATH" ]; then # -e checks for file or directory (for kustomize)
            echo "Error: Kubernetes config '$CONFIG_FILE_PATH' not found." >&2
            exit 1
        fi

        KUBE_CONTEXT_ARG=""
        if [ -n "$KUBE_CONTEXT" ]; then
            KUBE_CONTEXT_ARG="--context ${KUBE_CONTEXT}"
        fi

        echo "Applying Kubernetes manifests from ${CONFIG_FILE_PATH}..."
        # Assumption: IMAGE_TAG_OR_ARTIFACT_PATH is used to update the image tag within the manifest(s)
        # before this script is called, or the manifests use a variable substitution mechanism.
        # Example using kustomize (if CONFIG_FILE_PATH is a directory with kustomization.yaml):
        #   kubectl apply -k "${CONFIG_FILE_PATH}" ${KUBE_CONTEXT_ARG}
        # Example using plain manifest file:
        #   kubectl apply -f "${CONFIG_FILE_PATH}" ${KUBE_CONTEXT_ARG}
        # This script uses -f for simplicity, adjust if kustomize or Helm is standard.
        kubectl apply -f "${CONFIG_FILE_PATH}" ${KUBE_CONTEXT_ARG}
        if [ $? -ne 0 ]; then
            echo "Error: kubectl apply failed." >&2
            exit 1
        fi
        echo "Kubernetes deployment successful. May take time for resources to be ready."
        ;;

    s3-upload)
        echo "Executing S3 upload for ${APP_NAME}..."
        if ! command -v aws &> /dev/null; then
            echo "Error: AWS CLI (aws) could not be found. Please install it." >&2
            exit 1
        fi
        # Assuming S3_BUCKET_NAME is an environment variable or part of IMAGE_TAG_OR_ARTIFACT_PATH logic
        # For this script, we'll construct a path like "s3://your-bucket/${DEPLOYMENT_ENV}/${APP_NAME}/"
        # The actual bucket name needs to be configured. Example: S3_BUCKET_TARGET="s3://your-dfr-bucket"
        if [ -z "$S3_BUCKET_TARGET" ]; then
            echo "Error: S3_BUCKET_TARGET environment variable (e.g., s3://your-bucket-name) is required for s3-upload." >&2
            exit 1
        fi

        S3_DEST_PATH="${S3_BUCKET_TARGET}/${DEPLOYMENT_ENV}/${APP_NAME}/$(basename "${IMAGE_TAG_OR_ARTIFACT_PATH}")"
        AWS_PROFILE_ARG=""
        if [ -n "$AWS_PROFILE" ]; then
            AWS_PROFILE_ARG="--profile ${AWS_PROFILE}"
        fi

        echo "Uploading ${IMAGE_TAG_OR_ARTIFACT_PATH} to ${S3_DEST_PATH}..."
        aws s3 cp "${IMAGE_TAG_OR_ARTIFACT_PATH}" "${S3_DEST_PATH}" ${AWS_PROFILE_ARG}
        if [ $? -ne 0 ]; then
            echo "Error: aws s3 cp failed." >&2
            exit 1
        fi
        echo "S3 upload successful."
        ;;

    app-store-deploy)
        echo "Executing conceptual app-store deployment for ${APP_NAME}..."
        # This is a placeholder. Actual deployment would use tools like fastlane or specific store APIs.
        # Example: fastlane deploy --env "${DEPLOYMENT_ENV}" --apk "${IMAGE_TAG_OR_ARTIFACT_PATH}"
        if [ ! -f "$IMAGE_TAG_OR_ARTIFACT_PATH" ]; then
             echo "Error: Artifact for app store deployment '${IMAGE_TAG_OR_ARTIFACT_PATH}' not found." >&2
             exit 1
        fi
        echo "Conceptual: Deploying ${APP_NAME} artifact ${IMAGE_TAG_OR_ARTIFACT_PATH} to ${DEPLOYMENT_ENV} app store track."
        echo "Actual implementation requires specific tools like fastlane or store-specific upload scripts."
        # Simulate success for placeholder
        echo "App-store deployment (conceptual) successful."
        ;;

    *)
        echo "Error: Unknown DEPLOYMENT_TYPE '${DEPLOYMENT_TYPE}'." >&2
        exit 1
        ;;
esac

# --- Basic Post-Deployment Health Checks (Conceptual) ---
echo "Performing basic post-deployment health checks (conceptual)..."
# This is highly dependent on the application and deployment type.
# For a web service, it might be a curl request.
# Example:
# HEALTH_CHECK_URL="http://your-app-service-url" # This needs to be configured
# if [ -n "$HEALTH_CHECK_URL" ]; then
#     echo "Checking health at ${HEALTH_CHECK_URL}..."
#     response_code=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTH_CHECK_URL}")
#     if [ "$response_code" == "200" ]; then
#         echo "Health check passed (HTTP 200)."
#     else
#         echo "Warning: Health check failed or returned non-200 code: ${response_code}." >&2
#         # Depending on policy, this could be an error: exit 1;
#     fi
# else
    echo "No specific health check URL configured, skipping detailed health check."
# fi
echo "Post-deployment checks complete (conceptual)."


echo "Deployment script completed successfully."
exit 0