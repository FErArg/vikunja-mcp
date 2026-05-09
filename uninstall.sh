#!/bin/bash
set -e

VIKUNJA_MCP_DIR="$HOME/.vikunja-mcp"
OPENCODE_CONFIG="$HOME/.config/opencode/opencode.json"

echo "=== vikunja-mcp uninstaller ==="

read -p "Remove all vikunja-mcp files and configuration? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "Uninstallation cancelled."
  exit 0
fi

if [ -d "$VIKUNJA_MCP_DIR" ]; then
  echo "Removing $VIKUNJA_MCP_DIR..."
  rm -rf "$VIKUNJA_MCP_DIR"
  echo "Files removed."
else
  echo "Directory $VIKUNJA_MCP_DIR not found."
fi

if [ -f "$OPENCODE_CONFIG" ]; then
  if grep -q 'vikunja-mcp' "$OPENCODE_CONFIG"; then
    echo "Removing vikunja-mcp from $OPENCODE_CONFIG..."
    python3 << PYEOF
import json
with open("$OPENCODE_CONFIG", "r") as f:
    config = json.load(f)
if "mcp" in config and "vikunja-mcp" in config["mcp"]:
    del config["mcp"]["vikunja-mcp"]
    if not config["mcp"]:
        del config["mcp"]
with open("$OPENCODE_CONFIG", "w") as f:
    json.dump(config, f, indent=2)
PYEOF
    echo "OpenCode configuration updated."
  else
    echo "No vikunja-mcp entry found in OpenCode config."
  fi
else
  echo "OpenCode config not found: $OPENCODE_CONFIG"
fi

echo
echo "=== Uninstallation complete ==="
echo "Your Vikunja data was not affected."