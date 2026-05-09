#!/bin/bash
set -e

VIKUNJA_MCP_DIR="$HOME/.vikunja-mcp"
VENV_DIR="$VIKUNJA_MCP_DIR/env"
CONFIG_FILE="$VIKUNJA_MCP_DIR/config.json"
OPENCODE_CONFIG="$HOME/.config/opencode/opencode.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== vikunja-mcp installer ==="

OS="$(uname -s)"
case "$OS" in
  Darwin|Linux) ;;
  *)
    echo "Error: Unsupported OS: $OS"
    exit 1
    ;;
esac
echo "Detected OS: $OS"

PYTHON_CMD="python3"
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
  echo "Error: Python 3.11+ required. Found: $PYTHON_VERSION"
  echo "  macOS ships Python 3.9. Install Python 3.11+ from https://www.python.org/downloads/"
  exit 1
fi
echo "Python version: $PYTHON_VERSION OK"

if [ -d "$VIKUNJA_MCP_DIR" ]; then
  echo "Warning: $VIKUNJA_MCP_DIR already exists."
  read -p "Continue and overwrite? (yes/no): " CONFIRM
  if [ "$CONFIRM" != "yes" ]; then
    echo "Installation cancelled."
    exit 0
  fi
  rm -rf "$VIKUNJA_MCP_DIR"
fi

echo "Creating directory structure..."
mkdir -p "$VIKUNJA_MCP_DIR/mcp"
mkdir -p "$VIKUNJA_MCP_DIR/env"

echo "Creating virtual environment..."
$PYTHON_CMD -m venv "$VENV_DIR"

echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
pip install -e "$SCRIPT_DIR"

echo "Copying launcher script..."
cp "$SCRIPT_DIR/mcp/run_mcp.sh" "$VIKUNJA_MCP_DIR/mcp/"
chmod +x "$VIKUNJA_MCP_DIR/mcp/run_mcp.sh"

echo
read -p "Vikunja URL (e.g. https://try.vikunja.io): " VIKUNJA_URL
while [ -z "$VIKUNJA_URL" ]; do
  echo "URL cannot be empty."
  read -p "Vikunja URL: " VIKUNJA_URL
done

echo
read -p "API Token: " VIKUNJA_TOKEN
while [ -z "$VIKUNJA_TOKEN" ]; do
  echo "Token cannot be empty."
  read -p "API Token: " VIKUNJA_TOKEN
done

echo "Writing config to $CONFIG_FILE..."
cat > "$CONFIG_FILE" << EOF
{
  "vikunja_url": "$VIKUNJA_URL",
  "vikunja_token": "$VIKUNJA_TOKEN"
}
EOF

echo "Registering MCP server with OpenCode..."

mkdir -p "$(dirname "$OPENCODE_CONFIG")"

if [ -f "$OPENCODE_CONFIG" ]; then
  cp "$OPENCODE_CONFIG" "$OPENCODE_CONFIG.bak"
  echo "Backup created: $OPENCODE_CONFIG.bak"
fi

MCP_ENTRY='"vikunja-mcp": {
      "type": "local",
      "command": ["/bin/bash", "'"$VIKUNJA_MCP_DIR"'/mcp/run_mcp.sh"],
      "enabled": true
    }'

if [ -f "$OPENCODE_CONFIG" ] && [ -s "$OPENCODE_CONFIG" ]; then
  if grep -q '"mcp"' "$OPENCODE_CONFIG"; then
    python3 << PYEOF
import json
with open("$OPENCODE_CONFIG", "r") as f:
    config = json.load(f)
config.setdefault("mcp", {})["vikunja-mcp"] = {
    "type": "local",
    "command": ["/bin/bash", "$VIKUNJA_MCP_DIR/mcp/run_mcp.sh"],
    "enabled": True
}
with open("$OPENCODE_CONFIG", "w") as f:
    json.dump(config, f, indent=2)
PYEOF
  else
    python3 << PYEOF
import json
with open("$OPENCODE_CONFIG", "r") as f:
    config = json.load(f)
config["mcp"] = {
    "vikunja-mcp": {
        "type": "local",
        "command": ["/bin/bash", "$VIKUNJA_MCP_DIR/mcp/run_mcp.sh"],
        "enabled": True
    }
}
with open("$OPENCODE_CONFIG", "w") as f:
    json.dump(config, f, indent=2)
PYEOF
  fi
else
  python3 << PYEOF
import json
config = {
    "mcp": {
        "vikunja-mcp": {
            "type": "local",
            "command": ["/bin/bash", "$VIKUNJA_MCP_DIR/mcp/run_mcp.sh"],
            "enabled": True
        }
    }
}
with open("$OPENCODE_CONFIG", "w") as f:
    json.dump(config, f, indent=2)
PYEOF
fi

echo "Testing connection to Vikunja API..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Token $VIKUNJA_TOKEN" \
  "$VIKUNJA_URL/api/v1/projects?page=1")

if [ "$RESPONSE" = "200" ]; then
  echo "Connection successful!"
else
  echo "Warning: Could not connect to Vikunja API (HTTP $RESPONSE)"
  echo "Please verify your URL and token are correct."
fi

echo
echo "=== Installation complete ==="
echo "Config: $CONFIG_FILE"
echo "OpenCode MCP registered in: $OPENCODE_CONFIG"
echo
echo "To use with OpenCode, restart OpenCode or reload the configuration."