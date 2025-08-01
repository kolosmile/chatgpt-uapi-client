#!/usr/bin/env bash
set -euo pipefail

SSH_DIR="$HOME/.ssh"
KEY_FILE="$SSH_DIR/api_read_key"

# 1. Kulcs létrehozása
mkdir -p "$SSH_DIR"
echo "$SUBMODULE_SSH_KEY" > "$KEY_FILE"
chmod 600 "$KEY_FILE"

# 2. SSH config bejegyzés
cat >> "$SSH_DIR/config" <<EOF

Host github.com
    HostName ssh.github.com
    User git
    Port 443
    IdentityFile $KEY_FILE
    IdentitiesOnly yes
EOF
chmod 600 "$SSH_DIR/config"

# 3. Agent-be töltés (ha fut)
eval "$(ssh-agent -s)" >/dev/null
ssh-add "$KEY_FILE" 2>/dev/null || true   # ha passphrase-nélküli, ez csendben sikerül

# 4. Submodule lehúzása
git submodule update --init --recursive
