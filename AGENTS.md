# Agent Instructions

## Startup Commands

Every time the development environment starts up, please run the following command to ensure the API code is available:

```bash
git submodule update --init --recursive
```

This command will:
- Initialize any git submodules that haven't been initialized yet
- Update all submodules to their latest committed versions
- Recursively handle nested submodules

This ensures that all API code dependencies are properly synchronized and available for development.
