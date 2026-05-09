# vikunja-mcp

**Version:** 0.0.1

MCP (Model Context Protocol) server that connects an AI agent (OpenCode) to [Vikunja](https://vikunja.io/) project management system via its REST API.

## Capabilities

- **Projects:** List, create, read, update, delete
- **Tasks:** Full CRUD with comments, attachments, labels
- **Labels:** Manage project and task labels
- **Notifications:** Read and manage notifications
- **Files:** Upload and manage task attachments
- **Comments:** Add and read task comments

## Supported Platforms

- Linux
- macOS

## Requirements

- Python 3.11+
- Access to a Vikunja instance with API token

## Installation

```bash
git clone <repo-url>
cd vikunja-mcp
./install.sh
```

The installer will prompt for your Vikunja URL and API token.

## Uninstallation

```bash
./uninstall.sh
```

## Configuration

Configuration is stored in `~/.vikunja-mcp/config.json` and registered in OpenCode's `opencode.json`.

## Collaborators

- **FErArg** ([ferarg.com](https://ferarg.com)) — Project Owner
- **Deepseek** — AI assistant
- **Miramax** — AI assistant
- **Kimi** — AI assistant

## License

GPLv3 — see [LICENSE](LICENSE)