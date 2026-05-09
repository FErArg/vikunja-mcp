import pytest
from unittest.mock import Mock, patch
from vikunja_mcp.api import VikunjaClient


@pytest.fixture
def client():
    return VikunjaClient(
        api_base_url="https://vikunja.example.com/api/v1",
        headers={"Authorization": "Token test-token", "Content-Type": "application/json"}
    )


def test_api_base_url(client):
    assert client.api_base_url == "https://vikunja.example.com/api/v1"


def test_headers(client):
    assert client.headers["Authorization"] == "Token test-token"


@patch("requests.Session.request")
def test_list_projects(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "title": "Test Project"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_projects(page=1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/projects", params={"page": 1})
    assert result == [{"id": 1, "title": "Test Project"}]


@patch("requests.Session.request")
def test_get_project(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Test Project"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_project(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/projects/1")
    assert result == {"id": 1, "title": "Test Project"}


@patch("requests.Session.request")
def test_create_project(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "New Project"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.create_project({"title": "New Project", "description": "A test project"})

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/projects",
        json={"title": "New Project", "description": "A test project"}
    )
    assert result["id"] == 1


@patch("requests.Session.request")
def test_update_project(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Updated Title"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.update_project(1, {"title": "Updated Title"})

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/projects/1",
        json={"title": "Updated Title"}
    )
    assert result["title"] == "Updated Title"


@patch("requests.Session.request")
def test_delete_project(mock_request, client):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.delete_project(1)

    mock_request.assert_called_once_with("DELETE", "https://vikunja.example.com/api/v1/projects/1")
    assert result is True


@patch("requests.Session.request")
def test_list_tasks(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "title": "Task 1"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_tasks(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/projects/1/tasks", params={"page": 1})
    assert len(result) == 1


@patch("requests.Session.request")
def test_get_task(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Test Task"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_task(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/tasks/1")
    assert result["title"] == "Test Task"


@patch("requests.Session.request")
def test_create_task(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "New Task", "project_id": 1}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.create_task({"title": "New Task", "project_id": 1})

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/projects/1/tasks",
        json={"title": "New Task", "project_id": 1}
    )
    assert result["project_id"] == 1


@patch("requests.Session.request")
def test_delete_task(mock_request, client):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.delete_task(1)

    mock_request.assert_called_once_with("DELETE", "https://vikunja.example.com/api/v1/tasks/1")
    assert result is True


@patch("requests.Session.request")
def test_get_task_comments(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "content": "A comment"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_task_comments(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/tasks/1/comments")
    assert len(result) == 1


@patch("requests.Session.request")
def test_add_comment(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "content": "New comment"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.add_comment(1, {"comment": "New comment"})

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/tasks/1/comments",
        json={"comment": "New comment"}
    )
    assert result["content"] == "New comment"


@patch("requests.Session.request")
def test_list_notifications(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "message": "You were assigned a task"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_notifications(page=1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/notifications", params={"page": 1})
    assert len(result) == 1


@patch("requests.Session.request")
def test_read_notification(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "status": "read"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.read_notification(1)

    mock_request.assert_called_once_with(
        "PATCH",
        "https://vikunja.example.com/api/v1/notifications/1",
        json={"status": "read"}
    )
    assert result["status"] == "read"


@patch("requests.Session.request")
def test_search_tasks(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "title": "Found task"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.search_tasks("test query", project_id=1)

    mock_request.assert_called_once_with(
        "POST",
        "https://vikunja.example.com/api/v1/tasks/search",
        json={"query": "test query", "project_id": 1}
    )
    assert len(result) == 1


@patch("requests.Session.request")
def test_get_project_stats(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"total_tasks": 10, "done_tasks": 5}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_project_stats(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/projects/1/statistics")
    assert result["total_tasks"] == 10


@patch("requests.Session.request")
def test_set_task_labels(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Task with labels", "labels": [1, 2]}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.set_task_labels(1, [1, 2])

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/tasks/1/labels",
        json={"labels": [1, 2]}
    )
    assert result["labels"] == [1, 2]


@patch("requests.Session.request")
def test_remove_task_labels(mock_request, client):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.remove_task_labels(1)

    mock_request.assert_called_once_with("DELETE", "https://vikunja.example.com/api/v1/tasks/1/labels")
    assert result is True


@patch("requests.Session.request")
def test_get_service_info(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"version": "v0.22.0", "frontend_url": "https://vikunja.example.com"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_service_info()

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/info")
    assert result["version"] == "v0.22.0"


@patch("requests.Session.request")
def test_list_tasks_all(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_tasks_all(page=1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/tasks", params={"page": 1})
    assert len(result) == 2


@patch("requests.Session.request")
def test_list_project_members(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_project_members(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/projects/1/projectusers", params={})
    assert len(result) == 2


@patch("requests.Session.request")
def test_add_user_to_project(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"project_id": 1, "user_id": 5, "perm": 1}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.add_user_to_project(1, 5, perm=1)

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/projects/1/projectusers",
        json={"user_id": 5, "perm": 1}
    )
    assert result["user_id"] == 5


@patch("requests.Session.request")
def test_list_teams(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "name": "Team Alpha"}]
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.list_teams(page=1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/teams", params={"page": 1})
    assert len(result) == 1


@patch("requests.Session.request")
def test_get_team(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Team Alpha", "members": []}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.get_team(1)

    mock_request.assert_called_once_with("GET", "https://vikunja.example.com/api/v1/teams/1")
    assert result["name"] == "Team Alpha"


@patch("requests.Session.request")
def test_create_team(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "New Team"}
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.create_team("New Team")

    mock_request.assert_called_once_with(
        "PUT",
        "https://vikunja.example.com/api/v1/teams",
        json={"name": "New Team"}
    )
    assert result["name"] == "New Team"


@patch("requests.Session.request")
def test_delete_team(mock_request, client):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_request.return_value = mock_response

    result = client.delete_team(1)

    mock_request.assert_called_once_with("DELETE", "https://vikunja.example.com/api/v1/teams/1")
    assert result is True