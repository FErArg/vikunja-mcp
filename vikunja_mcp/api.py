import requests
from typing import Any, Optional


class VikunjaClient:
    def __init__(self, api_base_url: str, headers: dict):
        self.api_base_url = api_base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(headers)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.api_base_url}{path}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get(self, path: str, **kwargs) -> Any:
        return self._request("GET", path, **kwargs).json()

    def post(self, path: str, **kwargs) -> Any:
        return self._request("POST", path, **kwargs).json()

    def put(self, path: str, **kwargs) -> Any:
        return self._request("PUT", path, **kwargs).json()

    def patch(self, path: str, **kwargs) -> Any:
        return self._request("PATCH", path, **kwargs).json()

    def delete(self, path: str, **kwargs) -> Any:
        self._request("DELETE", path, **kwargs)
        return True

    def list_projects(self, page: int = 1) -> list:
        return self.get("/projects", params={"page": page})

    def get_project(self, project_id: int) -> dict:
        return self.get(f"/projects/{project_id}")

    def create_project(self, data: dict) -> dict:
        return self.put("/projects", json=data)

    def update_project(self, project_id: int, data: dict) -> dict:
        return self.put(f"/projects/{project_id}", json=data)

    def delete_project(self, project_id: int) -> bool:
        return self.delete(f"/projects/{project_id}")

    def list_tasks(self, project_id: int, page: int = 1) -> list:
        return self.get(f"/projects/{project_id}/tasks", params={"page": page})

    def get_task(self, task_id: int) -> dict:
        return self.get(f"/tasks/{task_id}")

    def create_task(self, data: dict) -> dict:
        project_id = data.get("project_id")
        if not project_id:
            raise ValueError("project_id is required in data for create_task")
        return self.put(f"/projects/{project_id}/tasks", json=data)

    def update_task(self, task_id: int, data: dict) -> dict:
        return self.put(f"/tasks/{task_id}", json=data)

    def delete_task(self, task_id: int) -> bool:
        return self.delete(f"/tasks/{task_id}")

    def get_task_comments(self, task_id: int) -> list:
        return self.get(f"/tasks/{task_id}/comments")

    def add_comment(self, task_id: int, data: dict) -> dict:
        return self.put(f"/tasks/{task_id}/comments", json=data)

    def list_labels(self, project_id: Optional[int] = None) -> list:
        if project_id:
            return self.get(f"/projects/{project_id}/labels")
        return self.get("/labels")

    def get_label(self, label_id: int) -> dict:
        return self.get(f"/labels/{label_id}")

    def create_label(self, data: dict) -> dict:
        return self.put("/labels", json=data)

    def update_label(self, label_id: int, data: dict) -> dict:
        return self.put(f"/labels/{label_id}", json=data)

    def delete_label(self, label_id: int) -> bool:
        return self.delete(f"/labels/{label_id}")

    def list_task_attachments(self, task_id: int) -> list:
        return self.get(f"/tasks/{task_id}/attachments")

    def upload_attachment(self, task_id: int, file_data: dict) -> dict:
        return self.put(f"/tasks/{task_id}/attachments", json=file_data)

    def delete_attachment(self, task_id: int, attachment_id: int) -> bool:
        return self.delete(f"/tasks/{task_id}/attachments/{attachment_id}")

    def list_notifications(self, page: int = 1) -> list:
        return self.get("/notifications", params={"page": page})

    def get_notification(self, notification_id: int) -> dict:
        return self.get(f"/notifications/{notification_id}")

    def read_notification(self, notification_id: int) -> dict:
        return self.patch(f"/notifications/{notification_id}", json={"status": "read"})

    def read_all_notifications(self) -> dict:
        return self.post("/notifications/read_all", json={})

    def search_tasks(self, query: str, project_id: Optional[int] = None) -> list:
        params = {"query": query}
        if project_id:
            params["project_id"] = project_id
        return self.post("/tasks/search", json=params)

    def get_project_stats(self, project_id: int) -> dict:
        return self.get(f"/projects/{project_id}/statistics")

    def add_label_to_task(self, task_id: int, label_id: int) -> dict:
        return self.put(f"/tasks/{task_id}/labels", json={"label_id": label_id})

    def add_labels_to_task(self, task_id: int, label_ids: list) -> list:
        results = []
        for label_id in label_ids:
            results.append(self.add_label_to_task(task_id, label_id))
        return results

    def remove_task_labels(self, task_id: int) -> bool:
        return self.delete(f"/tasks/{task_id}/labels")

    def remove_task_label(self, task_id: int, label_id: int) -> bool:
        return self.delete(f"/tasks/{task_id}/labels", json={"label_id": label_id})

    def get_service_info(self) -> dict:
        return self.get("/info")

    def list_tasks_all(self, page: int = 1) -> list:
        return self.get("/tasks", params={"page": page})

    def list_project_members(self, project_id: int) -> list:
        return self.get(f"/projects/{project_id}/projectusers")

    def add_user_to_project(self, project_id: int, user_id: int, perm: int = 1) -> dict:
        return self.put(f"/projects/{project_id}/projectusers", json={"user_id": user_id, "perm": perm})

    def list_teams(self, page: int = 1) -> list:
        return self.get("/teams", params={"page": page})

    def get_team(self, team_id: int) -> dict:
        return self.get(f"/teams/{team_id}")

    def create_team(self, name: str) -> dict:
        return self.put("/teams", json={"name": name})

    def delete_team(self, team_id: int) -> bool:
        return self.delete(f"/teams/{team_id}")