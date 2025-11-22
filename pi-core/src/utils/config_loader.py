import os
import yaml
from typing import Any, Dict


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")


def _load_yaml(name: str) -> Dict[str, Any]:
    path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_system_config() -> Dict[str, Any]:
    return _load_yaml("system.yaml")


def load_power_profiles() -> Dict[str, Any]:
    return _load_yaml("power_profiles.yaml")


def load_camera_config() -> Dict[str, Any]:
    return _load_yaml("camera.yaml")


def load_network_config() -> Dict[str, Any]:
    return _load_yaml("network.yaml")


def load_audio_config() -> Dict[str, Any]:
    return _load_yaml("audio.yaml")


def load_security_config() -> Dict[str, Any]:
    return _load_yaml("security.yaml")
