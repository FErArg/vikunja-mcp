#!/bin/bash
set -e

VIKUNJA_MCP_DIR="$HOME/.vikunja-mcp"
VENV_DIR="$VIKUNJA_MCP_DIR/env"
CONFIG_FILE="$VIKUNJA_MCP_DIR/config.json"

OS="$(uname -s)"
case "$OS" in
  Darwin*)  PYTHON_CMD="python3" ;;
  Linux*)   PYTHON_CMD="python3" ;;
  *)        echo "Unsupported OS: $OS" && exit 1 ;;
esac

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info[1])' 2>/dev/null || echo "0")
if [ "$PYTHON_VERSION" -lt 11 ]; then
  echo "Python 3.11+ required. Current version: $PYTHON_VERSION"
  exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Config file not found: $CONFIG_FILE"
  exit 1
fi

source "$VENV_DIR/bin/activate"
exec python -m vikunja_mcp.server "$CONFIG_FILE"