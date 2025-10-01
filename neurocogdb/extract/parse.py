from pathlib import Path
import yaml
import pandas as pd

def load_yaml_files(root_dir, pattern="**/*_info.yaml"):
    return list(Path(root_dir).rglob(pattern))

def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
