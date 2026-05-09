# Installation Guide

## Requirements

- Python 3.11 or higher
- Access to a Vikunja instance (self-hosted or Vikunja Cloud)
- API token from your Vikunja instance

**Note:** macOS ships with Python 3.9 by default. This project requires Python 3.11+. You must install a newer version before running the installer.

## Quick Install

```bash
git clone <repo-url>
cd vikunja-mcp
./install.sh
```

The installer will:

1. Detect your operating system (Linux/macOS) and verify Python 3.11+
2. Create a virtual environment at `~/.vikunja-mcp/env/`
3. Install the `vikunja_mcp` package in editable mode
4. Copy the launcher script to `~/.vikunja-mcp/mcp/run_mcp.sh`
5. Prompt for your Vikunja URL and API token
6. Register the MCP server with OpenCode's `opencode.json`
7. Test the connection to your Vikunja instance

## Getting Your Vikunja API Token

1. Log in to your Vikunja instance
2. Go to Settings → API Token
3. Create a new token
4. Copy the token (you won't be able to see it again)

## Manual Configuration

If you need to reconfigure after installation, edit `~/.vikunja-mcp/config.json`:

```json
{
  "vikunja_url": "https://your-vikunja.example.com",
  "vikunja_token": "your-api-token-here"
}
```

## Troubleshooting

### Python version error

```
Error: Python 3.11+ required. Found: 3.9
```

Install Python 3.11+ via [python.org](https://www.python.org/downloads/) or your package manager (brew, apt, etc.).

### ModuleNotFoundError: No module named 'vikunja_mcp'

Re-run the installer. The v0.0.1 installer had a bug that skipped installing the package and copying the launcher script. Run `./install.sh` again to fix.

### Connection refused

Verify your Vikunja URL is correct and that your Vikunja instance is running. Check that the API token is valid.

### OpenCode not finding the MCP server

Make sure `~/.config/opencode/opencode.json` contains the `vikunja-mcp` entry under `mcp`. You can check with:

```bash
cat ~/.config/opencode/opencode.json | grep -A5 "vikunja-mcp"
```

## Uninstallation

```bash
./uninstall.sh
```

This will remove:
- `~/.vikunja-mcp/` directory (virtual environment and configuration)
- MCP server registration from OpenCode

Your Vikunja data is not affected.