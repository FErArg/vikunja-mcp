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

## API Limitations

Vikunja servers that only allow GET and PUT methods require all create/update operations to use PUT:

| Method | Endpoint | Action |
|--------|----------|--------|
| PUT | `/projects` | Create project |
| PUT | `/projects/{id}/tasks` | Create task |
| PUT | `/labels` | Create label |
| PUT | `/tasks/{id}/comments` | Add comment |
| PUT | `/tasks/{id}/attachments` | Upload attachment |
| PUT | `/tasks/{id}/labels` | Set task labels (body: `{"label_id": int}`) |
| DELETE | `/tasks/{id}/labels` | Remove all labels from task (no body) |
| DELETE | `/tasks/{id}/labels` | Remove single label (body: `{"label_id": int}`) |
| GET | `/info` | Get Vikunja service info (version, frontend URL) |
| GET | `/tasks` | List all tasks (across all projects) |
| GET | `/projects/{id}/projectusers` | List project members |
| PUT | `/projects/{id}/projectusers` | Add user to project |
| GET | `/teams` | List teams |
| GET | `/teams/{id}` | Get team |
| PUT | `/teams` | Create team |
| DELETE | `/teams/{id}` | Delete team (may fail on PUT-only servers) |
| PUT | `/projects/{id}/duplicate` | Duplicate project into a parent project (body: `{"parent_project_id": int}`) |

### Important: Creating Child Projects

On this Vikunja server, POST /projects/{id} returns 405 Method Not Allowed (cannot update parent_project_id on existing projects).

**Correct approach:** Create the project directly with parent_project_id set:

```
create_project("child name", parent_project_id=parent_id)
```

**Do NOT use** `duplicate_project` + `delete_project` — it results in names like "child - duplicate" which cannot be renamed (PUT /projects/{id} = 405).
