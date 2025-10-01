import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_project_data(config, project_lookup, data_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        pid = project_lookup[data["project_name"]]
        for entry in data.get("data_sources", []):
            name = f"{entry['category']}_{entry['modality']}_{entry['device']}"
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "project_id": pid,
                    "data_id": data_lookup[name],
                }
            )

    return pd.DataFrame(rows)
