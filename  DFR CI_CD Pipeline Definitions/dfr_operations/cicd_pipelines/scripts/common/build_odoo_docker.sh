#!/bin/bash
# Shell script to build the DFR Odoo backend Docker image.
#
# Inputs/Parameters (Environment Variables or Arguments):
#   DOCKER_IMAGE_NAME: (Required) The name of the Docker image (e.g., your-registry/dfr-odoo-backend).
#   IMAGE_TAG: (Required) The tag for the Docker image (e.g., latest, v1.0.0, commit SHA).
#   DOCKERFILE_PATH: (Required) Path to the Dockerfile (e.g., path/to/odoo_modules/Dockerfile).
#   BUILD_CONTEXT: (Required) The build context directory for the Docker build command (e.g., path/to/odoo_modules).
#   PUSH_IMAGE: (Optional, boolean: true/false, default: false) Whether to push the image to a registry.
#   DOCKER_REGISTRY_URL: (Optional) URL of the Docker registry. Required if PUSH_IMAGE is true.
#   DOCKER_USERNAME: (Optional) Username for Docker registry login. Required if PUSH_IMAGE is true and registry requires auth.
#   DOCKER_PASSWORD: (Optional, secret) Password for Docker registry login. Required if PUSH_IMAGE is true and registry requires auth.
#   BUILD_ARGS: (Optional) String containing build arguments for Docker (e.g., "--build-arg KEY=VALUE").
#
# Standard OCI labels (org.opencontainers.image.*) will be added using information from environment variables
# typically available in CI/CD systems (e.g., CI_COMMIT_SHA, CI_REPOSITORY_URL, CI_COMMIT_TAG).
# These should be set in the calling environment if desired. Example:
#   OCI_SOURCE_URL (e.g., $CI_REPOSITORY_URL or equivalent GitHub var)
#   OCI_REVISION (e.g., $CI_COMMIT_SHA or equivalent GitHub var)
#   OCI_VERSION (e.g., $CI_COMMIT_TAG or $IMAGE_TAG)

set -e
set -o pipefail

# --- Parameter Validation & Defaults ---
if [ -z "$DOCKER_IMAGE_NAME" ]; then
    echo "Error: DOCKER_IMAGE_NAME is required." >&2
    exit 1
fi
if [ -z "$IMAGE_TAG" ]; then
    echo "Error: IMAGE_TAG is required." >&2
    exit 1
fi
if [ -z "$DOCKERFILE_PATH" ]; then
    echo "Error: DOCKERFILE_PATH is required." >&2
    exit 1
fi
if [ -z "$BUILD_CONTEXT" ]; then
    echo "Error: BUILD_CONTEXT is required." >&2
    exit 1
fi

PUSH_IMAGE="${PUSH_IMAGE:-false}"
OCI_VERSION_LABEL="${OCI_VERSION:-$IMAGE_TAG}" # Use IMAGE_TAG for version label if OCI_VERSION not set

# --- Main Logic ---
echo "Starting Docker image build..."
echo "Image Name: ${DOCKER_IMAGE_NAME}"
echo "Image Tag: ${IMAGE_TAG}"
echo "Dockerfile Path: ${DOCKERFILE_PATH}"
echo "Build Context: ${BUILD_CONTEXT}"
echo "Push Image: ${PUSH_IMAGE}"
[ -n "$DOCKER_REGISTRY_URL" ] && echo "Docker Registry URL: ${DOCKER_REGISTRY_URL}"
[ -n "$BUILD_ARGS" ] && echo "Build Args: ${BUILD_ARGS}"

# Navigate to build context
echo "Changing to build context: ${BUILD_CONTEXT}"
cd "${BUILD_CONTEXT}" || { echo "Error: Failed to change to build context '${BUILD_CONTEXT}'." >&2; exit 1; }

# Docker Login if PUSH_IMAGE is true
if [ "$PUSH_IMAGE" == "true" ]; then
    if [ -z "$DOCKER_REGISTRY_URL" ]; then
        echo "Error: DOCKER_REGISTRY_URL is required when PUSH_IMAGE is true." >&2
        exit 1
    fi
    if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
        echo "Logging in to Docker registry: ${DOCKER_REGISTRY_URL} as ${DOCKER_USERNAME}..."
        echo "$DOCKER_PASSWORD" | docker login "$DOCKER_REGISTRY_URL" -u "$DOCKER_USERNAME" --password-stdin
        if [ $? -ne 0 ]; then
            echo "Error: Docker login failed." >&2
            exit 1
        fi
        echo "Docker login successful."
    elif [ -n "$DOCKER_USERNAME" ] || [ -n "$DOCKER_PASSWORD" ]; then
        echo "Warning: DOCKER_USERNAME and DOCKER_PASSWORD must both be provided for registry login. Skipping explicit login, assuming pre-configured credentials." >&2
    else
        echo "Info: DOCKER_USERNAME and DOCKER_PASSWORD not provided. Assuming pre-configured credentials for registry operations if needed."
    fi
fi

# Construct OCI labels
LABEL_ARGS=""
if [ -n "$OCI_SOURCE_URL" ]; then
    LABEL_ARGS="$LABEL_ARGS --label org.opencontainers.image.source=${OCI_SOURCE_URL}"
fi
if [ -n "$OCI_REVISION" ]; then
    LABEL_ARGS="$LABEL_ARGS --label org.opencontainers.image.revision=${OCI_REVISION}"
fi
if [ -n "$OCI_VERSION_LABEL" ]; then
    LABEL_ARGS="$LABEL_ARGS --label org.opencontainers.image.version=${OCI_VERSION_LABEL}"
fi
echo "OCI Labels to be applied (if any): ${LABEL_ARGS}"


# Execute Docker Build
echo "Building Docker image ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}..."
# The dot (.) at the end specifies the current directory (BUILD_CONTEXT) as the context for the build.
# shellcheck disable=SC2086
docker build ${BUILD_ARGS} ${LABEL_ARGS} -t "${DOCKER_IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE_PATH}" .
if [ $? -ne 0 ]; then
    echo "Error: Docker build failed for ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}." >&2
    exit 1
fi
echo "Docker image ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} built successfully."

# Push image if PUSH_IMAGE is true
if [ "$PUSH_IMAGE" == "true" ]; then
    echo "Pushing Docker image ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} to ${DOCKER_REGISTRY_URL}..."
    docker push "${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
    if [ $? -ne 0 ]; then
        echo "Error: Docker push failed for ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}." >&2
        exit 1
    fi
    echo "Docker image ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} pushed successfully."
else
    echo "Skipping Docker image push as PUSH_IMAGE is not 'true'."
fi

echo "Script completed successfully."
exit 0