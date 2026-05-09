import json
import os


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.vikunja_url = None
        self.vikunja_token = None
        self._load()

    def _load(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            data = json.load(f)

        self.vikunja_url = data.get("vikunja_url", "")
        self.vikunja_token = data.get("vikunja_token", "")

        if not self.vikunja_url or not self.vikunja_token:
            raise ValueError("Config must contain vikunja_url and vikunja_token")

    @property
    def api_base_url(self) -> str:
        return f"{self.vikunja_url.rstrip('/')}/api/v1"

    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.vikunja_token}",
            "Content-Type": "application/json"
        }