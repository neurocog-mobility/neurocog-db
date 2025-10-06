import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_project_participants(config, project_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        pid = project_lookup[metadata["project_name"]]
        for group in metadata.get("participants", [])["groups"]:
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "project_id": pid,
                    **group
                }
            )
    
    return pd.DataFrame(rows)