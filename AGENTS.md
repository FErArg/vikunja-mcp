# Agents

<!-- Fill in as the project evolves -->

## Project Overview

vikunja-mcp is an MCP (Model Context Protocol) server that connects an AI agent (OpenCode) to the Vikunja project management system via its REST API. It enables the AI to perform full CRUD operations on projects, tasks, labels, files, comments, and notifications.

## Developer Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test/ -v

# Run MCP server directly
python -m vikunja_mcp.server ~/.vikunja-mcp/config.json
```

## Architecture

- `vikunja_mcp/server.py` — FastMCP server entrypoint
- `vikunja_mcp/api.py` — Vikunja API HTTP client (Bearer token auth)
- `vikunja_mcp/config.py` — Reads `~/.vikunja-mcp/config.json`
- `vikunja_mcp/tools.py` — All MCP tool definitions
- `mcp/run_mcp.sh` — Platform-aware launcher (Linux/macOS)

## Installation

Managed by `install.sh`. Installs to `~/.vikunja-mcp/`. Config is stored in `~/.vikunja-mcp/config.json`.

OpenCode MCP integration is registered in `~/.config/opencode/opencode.json`.

## Testing

Unit tests in `test/`:
- `test_api.py` — API client (mocked HTTP)
- `test_server.py` — Server initialization
- `test_install.py` — Installer logic

## Notes

- Python 3.11+ required (macOS ships 3.9; installer detects and aborts)
- Venv created at `~/.vikunja-mcp/env/`
- Launcher uses absolute path `~/.vikunja-mcp/mcp/run_mcp.sh` in opencode.json
- Config file path passed as argument to server, never hardcoded
- install.sh must run from the repo directory (uses `SCRIPT_DIR` to locate vikunja_mcp package and run_mcp.sh)
- vikunja_mcp package installed via `pip install -e` in editable mode
