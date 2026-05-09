# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.10] - 2026-05-09

### Added

- `create_project` docstring now explains `parent_project_id` usage
- AGENTS.md documents correct child project creation (directly with `parent_project_id`, not via duplicate+delete)

### Removed

- `move_project_to_parent` from recommended workflow (results in "- duplicate" suffix, cannot rename on this server)

### Notes

- On this Vikunja server: POST /projects/{id} returns 405 (cannot update parent_project_id on existing projects)
- Recommended: `create_project("name", parent_project_id=parent_id)` creates child directly with exact name

## [0.0.9] - 2026-05-09

### Added

- `duplicate_project(project_id, parent_project_id)` — Duplicate a project into a parent project. Useful for establishing parent-child hierarchy when the server's POST /projects/{id} returns 405 Method Not Allowed (cannot update parent_project_id on existing projects).
- `move_project_to_parent(project_id, parent_project_id)` — Wrapper that duplicates the project into parent and deletes the original (establishes hierarchy via copy+delete pattern).

### Notes

- The duplicate includes all tasks, labels, comments, attachments, assignees, kanban data, user/team permissions and link shares
- Original project remains until manually deleted

## [0.0.7] - 2026-05-09

### Fixed

- `add_label_to_task`: body now uses `{"label_id": int}` instead of `{"labels": [...]}` (API requires single label per request)
- `remove_label_from_task(task_id)`: now correctly removes all labels (no body)

### Added

- `add_labels_to_task(task_id, label_ids)`: associate multiple labels (one API call per label)
- `remove_label_from_task_single(task_id, label_id)`: remove a single specific label from a task

### Changed

- `add_label_to_task(task_id, label_ids)` → `add_label_to_task(task_id, label_id)` (signature changed to single label)

## [0.0.6] - 2026-05-09

### Added

- `get_service_info()` — Get Vikunja service info (version, frontend URL, MOTD)
- `list_tasks_all(page)` — List all tasks across all projects
- `list_project_members(project_id)` — List users with access to a project
- `add_user_to_project(project_id, user_id, perm)` — Add user to project with permissions
- `list_teams(page)` — List all teams the current user is part of
- `get_team(team_id)` — Get a team by ID
- `create_team(name)` — Create a new team
- `delete_team(team_id)` — Delete a team

### Limitations

- `delete_team` uses DELETE method and may fail on PUT-only Vikunja servers

## [0.0.5] - 2026-05-09

### Added

- `add_label_to_task(task_id, label_ids)` — Associate labels to a task via PUT /tasks/{id}/labels
- `remove_label_from_task(task_id)` — Remove all labels from a task via DELETE /tasks/{id}/labels

### Limitations

- `add_label_to_task` replaces all existing labels on the task (PUT overwrites)
- `remove_label_from_task` uses DELETE method and may fail on PUT-only Vikunja servers

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