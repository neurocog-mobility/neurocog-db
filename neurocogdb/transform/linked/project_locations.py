import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_project_locations(config, project_lookup, location_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("project_name") == "Project Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            pid = project_lookup[metadata.get("project_name")]
            for location in metadata.get("location", []):
                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "project_id": pid,
                        "location_id": location_lookup[location["name"]],
                    }
                )

    return pd.DataFrame(rows)