import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_project_members(config, project_lookup, member_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        pid = project_lookup[data["project_name"]]
        for name in data.get("members", []):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "project_id": pid,
                    "member_id": member_lookup[name],
                }
            )
    return pd.DataFrame(rows)
