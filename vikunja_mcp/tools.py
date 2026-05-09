from typing import Optional


def register_tools(mcp, client):
    @mcp.tool()
    def list_projects(page: int = 1) -> list:
        return client.list_projects(page)

    @mcp.tool()
    def get_project(project_id: int) -> dict:
        return client.get_project(project_id)

    @mcp.tool()
    def create_project(title: str, description: str = "", color: str = "#FFFFFF") -> dict:
        return client.create_project({
            "title": title,
            "description": description,
            "color": color
        })

    @mcp.tool()
    def update_project(project_id: int, title: Optional[str] = None,
                       description: Optional[str] = None, color: Optional[str] = None) -> dict:
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if color is not None:
            data["color"] = color
        return client.update_project(project_id, data)

    @mcp.tool()
    def delete_project(project_id: int) -> bool:
        return client.delete_project(project_id)

    @mcp.tool()
    def list_tasks(project_id: int, page: int = 1) -> list:
        return client.list_tasks(project_id, page)

    @mcp.tool()
    def get_task(task_id: int) -> dict:
        return client.get_task(task_id)

    @mcp.tool()
    def create_task(title: str, project_id: int, description: str = "",
                    due_date: Optional[str] = None, priority: int = 0) -> dict:
        data = {
            "title": title,
            "project_id": project_id,
            "description": description,
            "priority": priority
        }
        if due_date:
            data["due_date"] = due_date
        return client.create_task(data)

    @mcp.tool()
    def update_task(task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, due_date: Optional[str] = None,
                    priority: Optional[int] = None, done: Optional[bool] = None) -> dict:
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if due_date is not None:
            data["due_date"] = due_date
        if priority is not None:
            data["priority"] = priority
        if done is not None:
            data["done"] = done
        return client.update_task(task_id, data)

    @mcp.tool()
    def delete_task(task_id: int) -> bool:
        return client.delete_task(task_id)

    @mcp.tool()
    def get_task_comments(task_id: int) -> list:
        return client.get_task_comments(task_id)

    @mcp.tool()
    def add_comment(task_id: int, comment: str) -> dict:
        return client.add_comment(task_id, {"comment": comment})

    @mcp.tool()
    def list_labels(project_id: Optional[int] = None) -> list:
        return client.list_labels(project_id)

    @mcp.tool()
    def get_label(label_id: int) -> dict:
        return client.get_label(label_id)

    @mcp.tool()
    def create_label(title: str, description: str = "", color: str = "#FFFFFF",
                    project_id: Optional[int] = None) -> dict:
        data = {"title": title, "description": description, "color": color}
        if project_id is not None:
            data["project_id"] = project_id
        return client.create_label(data)

    @mcp.tool()
    def update_label(label_id: int, title: Optional[str] = None,
                     description: Optional[str] = None, color: Optional[str] = None) -> dict:
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if color is not None:
            data["color"] = color
        return client.update_label(label_id, data)

    @mcp.tool()
    def delete_label(label_id: int) -> bool:
        return client.delete_label(label_id)

    @mcp.tool()
    def add_label_to_task(task_id: int, label_ids: list[int]) -> dict:
        """Associate labels to a task. Replaces all existing labels on the task.

        Args:
            task_id: The ID of the task
            label_ids: List of label IDs to associate with the task

        Returns:
            The updated task with labels
        """
        return client.set_task_labels(task_id, label_ids)

    @mcp.tool()
    def remove_label_from_task(task_id: int) -> bool:
        """Remove all labels from a task.

        Note: Uses DELETE method. May fail if the Vikunja server
        only allows GET and PUT methods.

        Args:
            task_id: The ID of the task

        Returns:
            True if labels were removed
        """
        return client.remove_task_labels(task_id)

    @mcp.tool()
    def list_task_attachments(task_id: int) -> list:
        return client.list_task_attachments(task_id)

    @mcp.tool()
    def upload_attachment(task_id: int, name: str, url: str) -> dict:
        return client.upload_attachment(task_id, {"name": name, "url": url})

    @mcp.tool()
    def delete_attachment(task_id: int, attachment_id: int) -> bool:
        return client.delete_attachment(task_id, attachment_id)

    @mcp.tool()
    def list_notifications(page: int = 1) -> list:
        return client.list_notifications(page)

    @mcp.tool()
    def get_notification(notification_id: int) -> dict:
        return client.get_notification(notification_id)

    @mcp.tool()
    def read_notification(notification_id: int) -> dict:
        return client.read_notification(notification_id)

    @mcp.tool()
    def read_all_notifications() -> dict:
        return client.read_all_notifications()

    @mcp.tool()
    def search_tasks(query: str, project_id: Optional[int] = None) -> list:
        return client.search_tasks(query, project_id)

    @mcp.tool()
    def get_project_stats(project_id: int) -> dict:
        return client.get_project_stats(project_id)

    @mcp.tool()
    def get_service_info() -> dict:
        """Get Vikunja service info (version, frontend URL, MOTD, settings).

        Returns:
            Service information about the Vikunja instance
        """
        return client.get_service_info()

    @mcp.tool()
    def list_tasks_all(page: int = 1) -> list:
        """List all tasks the current user has access to across all projects.

        Args:
            page: Page number for pagination

        Returns:
            List of all tasks
        """
        return client.list_tasks_all(page)

    @mcp.tool()
    def list_project_members(project_id: int) -> list:
        """List all users with access to a project.

        Args:
            project_id: The project ID

        Returns:
            List of users on the project
        """
        return client.list_project_members(project_id)

    @mcp.tool()
    def add_user_to_project(project_id: int, user_id: int, perm: int = 1) -> dict:
        """Add a user to a project with specified permissions.

        Args:
            project_id: The project ID
            user_id: The user ID to add
            perm: Permission level (0=read only, 1=read/write, 2=admin). Default 1.

        Returns:
            The updated project user relation
        """
        return client.add_user_to_project(project_id, user_id, perm)

    @mcp.tool()
    def list_teams(page: int = 1) -> list:
        """List all teams the current user is part of.

        Args:
            page: Page number for pagination

        Returns:
            List of teams
        """
        return client.list_teams(page)

    @mcp.tool()
    def get_team(team_id: int) -> dict:
        """Get a team by its ID.

        Args:
            team_id: The team ID

        Returns:
            The team details
        """
        return client.get_team(team_id)

    @mcp.tool()
    def create_team(name: str) -> dict:
        """Create a new team.

        Args:
            name: The team name

        Returns:
            The created team
        """
        return client.create_team(name)

    @mcp.tool()
    def delete_team(team_id: int) -> bool:
        """Delete a team.

        Note: Uses DELETE method. May fail if the Vikunja server
        only allows GET and PUT methods.

        Args:
            team_id: The team ID to delete

        Returns:
            True if deleted successfully
        """
        return client.delete_team(team_id)