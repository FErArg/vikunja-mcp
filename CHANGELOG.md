# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2026-05-09

### Changed

- Vikunja API only allows GET and PUT methods (POST disabled on server)
- api.py: `create_project` now uses `PUT /projects` (was POST)
- api.py: `create_task` now uses `PUT /projects/{id}/tasks` (was POST /tasks)
- api.py: `create_label` now uses `PUT /labels` (was POST)
- api.py: `add_comment` now uses `PUT /tasks/{id}/comments` (was POST)
- api.py: `upload_attachment` now uses `PUT /tasks/{id}/attachments` (was POST)

### Limitations

- Bulk task updates (`POST /tasks/bulk`) not supported — requires POST
- Mark all notifications read (`POST /notifications/read_all`) not supported — requires POST
- Some delete operations require POST/DELETE which may be blocked on the Vikunja server

### Fixed

- Auth header: use `Bearer` instead of `Token` (Vikunja API requires `Authorization: Bearer <token>`)
- install.sh: API test curl also updated to use `Bearer`

## [0.0.2] - 2026-05-09

### Fixed

- install.sh: copy run_mcp.sh from repo to ~/.vikunja-mcp/mcp/
- install.sh: install vikunja_mcp package in editable mode (pip install -e)
- Fixed ModuleNotFoundError when launching MCP server

### Added

- Initial release
- MCP server for Vikunja project management API
- Support for Linux and macOS
- CRUD operations for projects and tasks
- Notifications access
- Labels, files, and comments management
- OpenCode MCP integration via local command
- Interactive installer with URL and token configuration
- Uninstall script
- Test suite