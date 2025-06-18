#!/bin/bash
# Shell script to create and push a Git tag based on Semantic Versioning.
#
# Purpose: Automates the process of tagging releases in Git according
#          to Semantic Versioning principles.
#
# Inputs/Parameters (Environment Variables or Arguments):
#   VERSION: (Required) The semantic version string (e.g., v1.2.3). Must start with 'v'.
#   GIT_REMOTE_NAME: (Optional, default: origin) Name of the Git remote.
#   TAG_MESSAGE: (Optional, default: "Release ${VERSION}") Annotation message for the tag.

set -e
set -o pipefail

# --- Parameter Validation & Defaults ---
if [ -z "$VERSION" ]; then
    echo "Error: VERSION is required." >&2
    exit 1
fi

# Validate VERSION format (starts with 'v', basic SemVer pattern vX.Y.Z)
# This regex checks for 'v' followed by three dot-separated numbers.
# It doesn't validate numeric ranges or pre-release/build metadata extensions of full SemVer.
SEMVER_PATTERN="^v[0-9]+\.[0-9]+\.[0-9]+$"
if ! [[ "$VERSION" =~ $SEMVER_PATTERN ]]; then
    echo "Error: VERSION '${VERSION}' is not in the format vX.Y.Z (e.g., v1.2.3)." >&2
    exit 1
fi

GIT_REMOTE_NAME="${GIT_REMOTE_NAME:-origin}"
TAG_MESSAGE_DEFAULT="Release ${VERSION}"
TAG_MESSAGE="${TAG_MESSAGE:-$TAG_MESSAGE_DEFAULT}"

# --- Main Logic ---
echo "Starting Git release tagging..."
echo "Version: ${VERSION}"
echo "Git Remote Name: ${GIT_REMOTE_NAME}"
echo "Tag Message: ${TAG_MESSAGE}"

# Check if tag already exists locally
if git rev-parse "${VERSION}" >/dev/null 2>&1; then
    echo "Warning: Tag '${VERSION}' already exists locally. Will attempt to push it."
    # Depending on policy, you might want to exit here or force update the tag.
    # Forcing update: git tag -f -a "${VERSION}" -m "${TAG_MESSAGE}"
else
    echo "Creating annotated Git tag '${VERSION}'..."
    git tag -a "${VERSION}" -m "${TAG_MESSAGE}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create Git tag '${VERSION}'." >&2
        exit 1
    fi
    echo "Git tag '${VERSION}' created successfully."
fi


echo "Pushing tag '${VERSION}' to remote '${GIT_REMOTE_NAME}'..."
git push "${GIT_REMOTE_NAME}" "${VERSION}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to push Git tag '${VERSION}' to remote '${GIT_REMOTE_NAME}'." >&2
    # It's possible the tag already exists on the remote. `git push` will fail in that case
    # unless --force is used, which is generally discouraged for release tags.
    # Check if the tag exists on the remote if push fails
    if git ls-remote --tags "${GIT_REMOTE_NAME}" | grep -q "refs/tags/${VERSION}$"; then
        echo "Info: Tag '${VERSION}' already exists on remote '${GIT_REMOTE_NAME}'. Assuming this is okay."
    else
        exit 1 # Exit if push failed for other reasons
    fi
fi
echo "Git tag '${VERSION}' pushed successfully to remote '${GIT_REMOTE_NAME}'."

echo "Script completed successfully."
exit 0