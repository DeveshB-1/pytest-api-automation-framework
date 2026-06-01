import os
import yaml
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


def build_session(max_attempts=3, backoff_factor=0.5):
    session = requests.Session()
    retry = Retry(
        total=max_attempts,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class APIClient:
    def __init__(self, env=None):
        config = load_config()
        env = env or os.getenv("ENV", "dev")
        env_cfg = config["environments"][env]
        self.base_url = env_cfg["base_url"].rstrip("/")
        self.timeout = env_cfg.get("timeout", 10)
        self.session = build_session(
            max_attempts=config["retry"]["max_attempts"],
            backoff_factor=config["retry"]["backoff_factor"],
        )
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def set_auth_token(self, token):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, endpoint, params=None, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=self.timeout, **kwargs)

    def post(self, endpoint, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, timeout=self.timeout, **kwargs)

    def put(self, endpoint, json=None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", json=json, timeout=self.timeout, **kwargs)

    def patch(self, endpoint, json=None, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", json=json, timeout=self.timeout, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", timeout=self.timeout, **kwargs)
