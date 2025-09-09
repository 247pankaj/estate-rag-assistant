from pathlib import Path
import os
import yaml


def get_project_root() -> Path:
    """
    Returns the root directory of the project.
    Assumes this file is located at .../utils/config_loader.py,
    so the project root is two levels up.
    """
    return Path(__file__).resolve().parents[1]


def load_config(config_path: str | None = None) -> dict:
    """
    Loads a YAML configuration file with reliable path resolution,
    regardless of the current working directory.

    Priority:
    1. Explicit argument
    2. CONFIG_PATH environment variable
    3. <project_root>/config/config.yaml
    """
    env_path = os.getenv("CONFIG_PATH")

    if config_path is None:
        config_path = env_path or str(get_project_root() / "config" / "config.yaml")

    path = Path(config_path)
    if not path.is_absolute():
        path = get_project_root() / path

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
    

# if __name__ == "__main__":
#     config = load_config(str(get_project_root() / "config" / "config.yaml"))
#     print(config)