from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigLoader:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def load(self, name: str) -> Dict[str, Any]:
        """
        name: 'system', 'power_profiles', 'camera', ...
        """
        path = self.root_dir / f"{name}.yaml"
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
