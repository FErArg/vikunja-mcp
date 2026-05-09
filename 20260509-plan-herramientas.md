# Plan: Extender herramientas MCP vikunja-mcp

Fecha: 2026-05-09
Versión MCP actual: 0.0.5
Herramientas implementadas: 25

---

## Estado actual

### Implementadas (25 tools)

| Categoría | Tools |
|----------|-------|
| Projects | list_projects, get_project, create_project, update_project, delete_project |
| Tasks | list_tasks, get_task, create_task, update_task, delete_task |
| Task relations | get_task_comments, add_comment |
| Labels | list_labels, get_label, create_label, update_label, delete_label |
| Label-task | add_label_to_task, remove_label_from_task |
| Attachments | list_task_attachments, upload_attachment, delete_attachment |
| Notifications | list_notifications, get_notification, read_notification, read_all_notifications |
| Search/stats | search_tasks, get_project_stats |

---

## Funcionalidades NO implementadas (según API Vikunja)

### HIGH PRIORITY (útiles para usuarios generales)

| # | Tool | Endpoint | Método | Descripción |
|---|------|----------|--------|-------------|
| 1 | get_service_info | /info | GET | Info del servidor Vikunja (versión, frontend URL, MOTD) |
| 2 | list_tasks_all | /tasks | GET | Listar TODAS las tareas del usuario (no solo por proyecto) |
| 3 | list_project_members | /projects/{id}/projectusers | GET | Listar usuarios con acceso a un proyecto |
| 4 | add_user_to_project | /projects/{id}/projectusers | PUT | Agregar usuario a proyecto |
| 5 | list_teams | /teams | GET | Listar todos los equipos del usuario |
| 6 | get_team | /teams/{id} | GET | Obtener un equipo |
| 7 | create_team | /teams | PUT | Crear equipo |
| 8 | update_team | /teams/{id} | POST | Actualizar equipo |
| 9 | delete_team | /teams/{id} | DELETE | Eliminar equipo |

### MEDIUM PRIORITY (colaboración y workflows)

| # | Tool | Endpoint | Método | Descripción |
|---|------|----------|--------|-------------|
| 10 | list_saved_filters | /filters | GET | Listar filtros guardados del usuario |
| 11 | get_saved_filter | /filters/{id} | GET | Obtener un filtro guardado |
| 12 | create_saved_filter | /filters | PUT | Crear filtro guardado |
| 13 | update_saved_filter | /filters/{id} | POST | Actualizar filtro guardado |
| 14 | delete_saved_filter | /filters/{id} | DELETE | Eliminar filtro guardado |
| 15 | create_share_link | /projects/{id}/shares | PUT | Crear enlace para compartir proyecto |
| 16 | list_project_shares | /projects/{id}/shares | GET | Listar enlaces compartidos de un proyecto |
| 17 | duplicate_project | /projects/{id}/duplicate | PUT | Duplicar proyecto |
| 18 | subscribe_to_task | /subscriptions/tasks/{id} | PUT | Suscribirse a tarea (notificaciones) |
| 19 | unsubscribe_from_task | /subscriptions/tasks/{id} | DELETE | Desuscribirse de tarea |
| 20 | subscribe_to_project | /subscriptions/projects/{id} | PUT | Suscribirse a proyecto |
| 21 | unsubscribe_from_project | /subscriptions/projects/{id} | DELETE | Desuscribirse de proyecto |

### LOW PRIORITY (casos específicos)

| # | Tool | Endpoint | Método | Descripción |
|---|------|----------|--------|-------------|
| 22 | get_user | /user | GET | Obtener perfil del usuario actual |
| 23 | list_project_webhooks | /projects/{id}/webhooks | GET | Listar webhooks de un proyecto |
| 24 | create_project_webhook | /projects/{id}/webhooks | PUT | Crear webhook en proyecto |
| 25 | delete_project_webhook | /projects/{id}/webhooks/{webhookId} | DELETE | Eliminar webhook |
| 26 | get_task_relations | /tasks/{id}/relations | GET | Listar relaciones de una tarea |
| 27 | add_task_relation | /tasks/{id}/relations | PUT | Crear relación entre tareas |
| 28 | remove_task_relation | /tasks/{id}/relations/{relationId} | DELETE | Eliminar relación |
| 29 | list_task_assignees | /tasks/{id}/assignees | GET | Listar asignados a tarea |
| 30 | add_task_assignee | /tasks/{id}/assignees | PUT | Asignar usuario a tarea |
| 31 | search_project_backgrounds | /backgrounds/unsplash/search | GET | Buscar fondos de Unsplash |
| 32 | upload_project_background | /projects/{id}/backgrounds/upload | PUT | Subir fondo de proyecto |
| 33 | add_task_reaction | /tasks/{id}/reactions | PUT | Reaccionar a tarea/comentario |
| 34 | remove_task_reaction | /tasks/{id}/reactions/{reactionId} | DELETE | Eliminar reacción |

### NO IMPLEMENTABLES (requieren POST, limitado por servidor PUT-only)

| Operation | Endpoint | Método | Razón |
|-----------|----------|--------|-------|
| Bulk task updates | /tasks/bulk | POST | No hay alternativa PUT |
| CSV import | /migration/csv/* | PUT | Soporta PUT, pero multipart/form-data complejo |
| Migraciones | /migration/ticktick/*, /migration/wekan/*, etc. | PUT/GET | Solo para migración inicial |

---

## Recomendación de implementación

### Fase 1 — Alta prioridad (9 tools)
1, 2, 3, 4, 5, 6, 7, 8, 9

### Fase 2 — Media prioridad (12 tools)
10-21 (filtros, shares, subscriptions, duplicate)

### Fase 3 — Baja prioridad (13 tools)
22-34 (user profile, webhooks, reactions, assignees, backgrounds)

---

## Limitaciones conocidas

- PUT-only server: algunas tools usan DELETE (subscriptions, reactions, team delete)
- Bulk operations (tasks/bulk) no soportadas sin POST
- File uploads (multipart) no implementados en upload_project_background
- Admin endpoints (/admin/*) excluidos por ser específicos de instancia
