#!/bin/bash
set -e
set -o pipefail

# Docker and Docker Compose Helper Functions
# This script should be sourced by other scripts that need these functions.

# Determine script's directory to source utils.sh reliably if it's in the same directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
UTILS_SCRIPT_PATH="${SCRIPT_DIR}/utils.sh" # Assumes utils.sh is in the same directory

if [ ! -f "$UTILS_SCRIPT_PATH" ]; then
    # Try an alternative path if the above fails in some sourcing contexts
    ALT_UTILS_PATH="$(dirname "$0")/utils.sh"
    if [ -f "$ALT_UTILS_PATH" ]; then
        UTILS_SCRIPT_PATH="$ALT_UTILS_PATH"
    else
        echo "Error: utils.sh not found at $UTILS_SCRIPT_PATH or $ALT_UTILS_PATH"
        exit 1
    fi
fi
# shellcheck source=./utils.sh
source "$UTILS_SCRIPT_PATH"

# Checks if a container is running.
# Usage: is_container_running <container_name_or_id>
# Returns 0 if running, 1 otherwise.
is_container_running() {
    local container_name_or_id="$1"
    if [ -z "$container_name_or_id" ]; then
        log_error "Usage: is_container_running <container_name_or_id>"
        return 2 # Different error code for usage error
    fi

    # `docker ps -q` lists IDs of running containers.
    # `-f name=^/${container_name_or_id}$` filters by exact name.
    # The `^/` and `$` ensure exact match for names. For IDs, it should still work.
    if [[ -n "$(docker ps -q -f name="^/${container_name_or_id}$")" ]]; then
        log_info "Container '$container_name_or_id' is running."
        return 0 # True, running
    elif docker inspect "$container_name_or_id" &>/dev/null && \
         [[ "$(docker inspect -f '{{.State.Running}}' "$container_name_or_id")" == "true" ]]; then
        # Fallback for ID if name filter fails or if it's an ID
        log_info "Container '$container_name_or_id' is running (checked by ID)."
        return 0 # True, running
    else
        log_info "Container '$container_name_or_id' is not running."
        return 1 # False, not running
    fi
}

# Safely stops and removes a container.
# Usage: stop_and_remove_container <container_name_or_id>
stop_and_remove_container() {
    local container_name_or_id="$1"
    if [ -z "$container_name_or_id" ]; then
        log_error "Usage: stop_and_remove_container <container_name_or_id>"
        return 2
    fi

    log_info "Attempting to stop container '$container_name_or_id'..."
    if docker stop "$container_name_or_id" >/dev/null 2>&1; then
        log_success "Container '$container_name_or_id' stopped."
    else
        # Check if it was already stopped or didn't exist
        if ! docker inspect "$container_name_or_id" &>/dev/null; then
            log_warning "Container '$container_name_or_id' does not exist. No need to stop."
        elif [[ "$(docker inspect -f '{{.State.Status}}' "$container_name_or_id")" != "running" ]]; then
            log_info "Container '$container_name_or_id' was already stopped."
        else
            log_warning "Failed to stop container '$container_name_or_id', or it was already stopped."
            # Continue to removal attempt
        fi
    fi

    log_info "Attempting to remove container '$container_name_or_id'..."
    if docker rm "$container_name_or_id" >/dev/null 2>&1; then
        log_success "Container '$container_name_or_id' removed."
    else
         if ! docker inspect "$container_name_or_id" &>/dev/null; then # Check if it was already removed
            log_info "Container '$container_name_or_id' was already removed or did not exist."
        else
            log_warning "Failed to remove container '$container_name_or_id'. It might not exist or be in use."
            # It's not a critical error if it's already gone.
        fi
    fi
}

# Builds a Docker image.
# Usage: build_docker_image <dockerfile_path> <image_name> <tag> [context_path] [build_args...]
# Example: build_docker_image components/odoo/Dockerfile myapp/odoo latest components/odoo --build-arg VERSION=1.0
build_docker_image() {
    local dockerfile_path="$1"
    local image_name="$2"
    local tag="$3"
    local context_path="${4:-.}" # Default context is current directory or one specified
    shift 4 # Remove first four args, rest are build_args

    if [ -z "$dockerfile_path" ] || [ -z "$image_name" ] || [ -z "$tag" ]; then
        log_error "Usage: build_docker_image <dockerfile_path> <image_name> <tag> [context_path] [build_args...]"
        return 2
    fi

    if [ ! -f "$dockerfile_path" ]; then
        # If dockerfile_path is relative, it might be relative to context_path or current dir
        # For simplicity, assume dockerfile_path is absolute or relative to where script is called.
        # Or, assume it's relative to context_path.
        # SDS: docker build -f $dockerfile_path ... . (implies dockerfile path can be anywhere, context is .)
        # Let's assume dockerfile_path is a full or resolvable path.
        # Context path is where the build process looks for files (e.g. to COPY).
        log_error "Dockerfile '$dockerfile_path' not found."
        return 1
    fi
     if [ ! -d "$context_path" ]; then
        log_error "Build context path '$context_path' not found or not a directory."
        return 1
    fi

    local full_image_name="${image_name}:${tag}"
    log_info "Building Docker image '$full_image_name' from Dockerfile '$dockerfile_path' with context '$context_path'..."
    log_info "Build arguments: $*"

    # Construct build-arg options
    local build_arg_opts=()
    for barg in "$@"; do
        build_arg_opts+=("--build-arg" "$barg")
    done

    if docker build -f "$dockerfile_path" -t "$full_image_name" "${build_arg_opts[@]}" "$context_path"; then
        log_success "Docker image '$full_image_name' built successfully."
    else
        log_error "Failed to build Docker image '$full_image_name'."
        return 1
    fi
}

# Creates a Docker network if it doesn't exist.
# Usage: ensure_network_exists <network_name>
ensure_network_exists() {
    local network_name="$1"
    if [ -z "$network_name" ]; then
        log_error "Usage: ensure_network_exists <network_name>"
        return 2
    fi

    if docker network inspect "$network_name" >/dev/null 2>&1; then
        log_info "Docker network '$network_name' already exists."
    else
        log_info "Docker network '$network_name' not found. Creating..."
        if docker network create "$network_name"; then
            log_success "Docker network '$network_name' created successfully."
        else
            log_error "Failed to create Docker network '$network_name'."
            return 1
        fi
    fi
}

# Pulls a Docker image if it's not present locally.
# Usage: pull_image_if_not_exists <image_name_with_tag>
pull_image_if_not_exists() {
    local image_name_with_tag="$1"
    if [ -z "$image_name_with_tag" ]; then
        log_error "Usage: pull_image_if_not_exists <image_name_with_tag>"
        return 2
    fi

    if docker image inspect "$image_name_with_tag" >/dev/null 2>&1; then
        log_info "Docker image '$image_name_with_tag' already exists locally."
    else
        log_info "Docker image '$image_name_with_tag' not found locally. Pulling..."
        if docker pull "$image_name_with_tag"; then
            log_success "Docker image '$image_name_with_tag' pulled successfully."
        else
            log_error "Failed to pull Docker image '$image_name_with_tag'."
            return 1
        fi
    fi
}

# Example of how to use docker-compose commands with multiple compose files
# Usage: run_compose_command <project_dir> <env> <compose_command_and_args...>
# Example: run_compose_command environments/development dev up -d
# function run_compose_command() {
#     local project_dir="$1" # e.g., environments/development
#     local env_name="$2" # e.g., dev - could be used for naming or .env file context
#     shift 2
#     local compose_cmd_args=("$@")

#     local main_compose_file="${project_dir}/docker-compose.yml"
#     local common_compose_file="${project_dir}/../common/docker-compose.common.yml" # Adjust path

#     local compose_opts=()
#     if [ ! -f "$main_compose_file" ]; then
#         log_error "Main Docker Compose file not found: $main_compose_file"
#         return 1
#     fi
#     compose_opts+=("-f" "$main_compose_file")

#     if [ -f "$common_compose_file" ]; then
#         compose_opts+=("-f" "$common_compose_file")
#     fi
    
#     # Docker Compose typically loads .env from the project directory.
#     # If project_dir is not where docker-compose is run from, --project-directory might be needed.
#     # Or cd into project_dir.
#     # Using --project-directory to specify context for .env loading and relative paths in compose files.

#     log_info "Running Docker Compose command in $project_dir: ${compose_cmd_args[*]}"
#     if docker-compose --project-directory "$project_dir" "${compose_opts[@]}" "${compose_cmd_args[@]}"; then
#         log_success "Docker Compose command successful."
#     else
#         log_error "Docker Compose command failed."
#         return 1
#     fi
# }

log_info "Docker helper functions loaded."