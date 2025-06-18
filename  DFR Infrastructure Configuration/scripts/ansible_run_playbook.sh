#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

PLAYBOOK_PATH=$1
INVENTORY_PATH=$2
EXTRA_VARS=$3 # Optional: e.g., "key1=value1 key2=value2" or "@vars.json" or '{"key1":"value1", "key2":"value2"}'

if [ -z "$PLAYBOOK_PATH" ] || [ -z "$INVENTORY_PATH" ]; then
  echo "Usage: $0 <ansible_playbook_path> <ansible_inventory_path> [extra_vars]"
  echo "Example: $0 ansible/playbooks/pb_provision_dfr_stack_vm.yml ansible/inventories/aws_ck_staging_inventory.ini"
  echo "Example with extra vars: $0 playbook.yml inventory.ini '{\"variable_host\":\"some_value\"}'"
  echo "Example with extra vars file: $0 playbook.yml inventory.ini '@my_vars.json'"
  exit 1
fi

if [ ! -f "$PLAYBOOK_PATH" ]; then
  echo "Error: Playbook '$PLAYBOOK_PATH' not found."
  exit 1
fi

# Check if inventory is a file or an executable script (for dynamic inventory)
if [ ! -f "$INVENTORY_PATH" ] && [ ! -x "$INVENTORY_PATH" ]; then
  echo "Error: Inventory '$INVENTORY_PATH' not found or is not an executable script (for dynamic inventory)."
  exit 1
fi

ANSIBLE_CMD_BASE="ansible-playbook -i \"$INVENTORY_PATH\" \"$PLAYBOOK_PATH\""
ANSIBLE_EXTRA_VARS_CMD=""

if [ -n "$EXTRA_VARS" ]; then
  # Check if EXTRA_VARS starts with @, indicating a vars file
  if [[ "$EXTRA_VARS" == @* ]]; then
    ANSIBLE_EXTRA_VARS_CMD="--extra-vars \"$EXTRA_VARS\""
  else
    # For inline JSON or key=value pairs, quote carefully
    ANSIBLE_EXTRA_VARS_CMD="--extra-vars '$EXTRA_VARS'"
  fi
fi

echo "==> Running Ansible playbook: $PLAYBOOK_PATH with inventory: $INVENTORY_PATH"
if [ -n "$ANSIBLE_EXTRA_VARS_CMD" ]; then
  echo "==> With extra variables: $EXTRA_VARS"
  # Using eval is generally risky, but ansible-playbook handles extra-vars string well.
  # For more complex scenarios, consider constructing an array for command arguments.
  eval "$ANSIBLE_CMD_BASE $ANSIBLE_EXTRA_VARS_CMD"
else
  eval "$ANSIBLE_CMD_BASE"
fi

echo "==> Ansible playbook $PLAYBOOK_PATH completed."