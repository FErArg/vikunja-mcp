import pytest
import json
import os
from unittest.mock import Mock, patch
from vikunja_mcp.config import Config


@pytest.fixture
def config_file(tmp_path):
    config_data = {
        "vikunja_url": "https://vikunja.example.com",
        "vikunja_token": "test-token-123"
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_data))
    return str(config_path)


@pytest.fixture
def missing_config_file(tmp_path):
    return str(tmp_path / "nonexistent.json")


def test_config_loads_successfully(config_file):
    config = Config(config_file)
    assert config.vikunja_url == "https://vikunja.example.com"
    assert config.vikunja_token == "test-token-123"


def test_config_file_not_found(missing_config_file):
    with pytest.raises(FileNotFoundError):
        Config(missing_config_file)


def test_api_base_url(config_file):
    config = Config(config_file)
    assert config.api_base_url == "https://vikunja.example.com/api/v1"


def test_api_base_url_no_trailing_slash(tmp_path):
    config_data = {"vikunja_url": "https://vikunja.example.com/", "vikunja_token": "token"}
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_data))
    config = Config(str(config_path))
    assert config.api_base_url == "https://vikunja.example.com/api/v1"


def test_headers(config_file):
    config = Config(config_file)
    headers = config.headers()
    assert headers["Authorization"] == "Token test-token-123"
    assert headers["Content-Type"] == "application/json"


def test_missing_vikunja_url(tmp_path):
    config_data = {"vikunja_token": "test-token"}
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_data))
    with pytest.raises(ValueError):
        Config(str(config_path))


def test_missing_vikunja_token(tmp_path):
    config_data = {"vikunja_url": "https://vikunja.example.com"}
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_data))
    with pytest.raises(ValueError):
        Config(str(config_path))