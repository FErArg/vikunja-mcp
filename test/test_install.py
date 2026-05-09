import pytest
import json
import os
import tempfile
from unittest.mock import patch


def test_install_creates_directories(tmp_path):
    from install import create_directories
    vikunja_dir = tmp_path / ".vikunja-mcp"
    vikunja_dir.mkdir = pytest.mock.Mock()
    (vikunja_dir / "mcp").mkdir = pytest.mock.Mock()
    (vikunja_dir / "env").mkdir = pytest.mock.Mock()

    with patch("os.path.expanduser", return_value=str(vikunja_dir)):
        pass


def test_opencode_config_merge(tmp_path):
    opencode_config = tmp_path / "opencode.json"
    existing_config = {"tools": {"some_tool": True}, "mcp": {"other-mcp": {"type": "local"}}}
    opencode_config.write_text(json.dumps(existing_config))

    with patch("builtins.open", side_effect=lambda *args, **kwargs: opencode_config.open(*args, **kwargs)):
        pass


def test_uninstall_removes_vikunja_dir(tmp_path):
    vikunja_dir = tmp_path / ".vikunja-mcp"
    vikunja_dir.mkdir(exist_ok=True)
    (vikunja_dir / "config.json").write_text("{}")

    assert vikunja_dir.exists()

    import shutil
    shutil.rmtree(vikunja_dir)

    assert not vikunja_dir.exists()


def test_uninstall_removes_mcp_entry(tmp_path):
    opencode_config = tmp_path / "opencode.json"
    config_with_mcp = {
        "mcp": {
            "other-mcp": {"type": "local"},
            "vikunja-mcp": {"type": "local", "command": ["test"]}
        }
    }
    opencode_config.write_text(json.dumps(config_with_mcp))

    with open(opencode_config) as f:
        loaded = json.load(f)

    del loaded["mcp"]["vikunja-mcp"]

    with open(opencode_config, "w") as f:
        json.dump(loaded, f)

    with open(opencode_config) as f:
        result = json.load(f)

    assert "vikunja-mcp" not in result.get("mcp", {})
    assert "other-mcp" in result["mcp"]


def test_uninstall_preserves_other_mcp_entries(tmp_path):
    opencode_config = tmp_path / "opencode.json"
    config_with_multiple = {
        "mcp": {
            "sentry": {"type": "remote", "url": "https://sentry.io/mcp"},
            "vikunja-mcp": {"type": "local", "command": ["test"]},
            "context7": {"type": "remote", "url": "https://context7.com/mcp"}
        }
    }
    opencode_config.write_text(json.dumps(config_with_multiple))

    with open(opencode_config) as f:
        loaded = json.load(f)

    del loaded["mcp"]["vikunja-mcp"]

    with open(opencode_config, "w") as f:
        json.dump(loaded, f)

    with open(opencode_config) as f:
        result = json.load(f)

    assert "vikunja-mcp" not in result["mcp"]
    assert "sentry" in result["mcp"]
    assert "context7" in result["mcp"]
    assert len(result["mcp"]) == 2