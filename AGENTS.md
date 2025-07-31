# Agent Instructions

## Startup Commands

Every time the development environment starts up, please run the following command to ensure the API code is available:

```bash
echo "$SUBMODULE_SSH_KEY" > /tmp/api_key
chmod 600 /tmp/api_key
export GIT_SSH_COMMAND="ssh -i /tmp/api_key -o StrictHostKeyChecking=no"
git submodule update --init --recursive
```

This command will:
- Initialize any git submodules that haven't been initialized yet
- Update all submodules to their latest committed versions
- Recursively handle nested submodules

This ensures that all API code dependencies are properly synchronized and available for development.
