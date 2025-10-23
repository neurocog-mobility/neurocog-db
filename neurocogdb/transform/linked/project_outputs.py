import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_project_outputs(config, project_lookup, output_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        print(f)
        metadata = load_yaml(f)
        if not metadata.get("project_name") == "Project Name" and not metadata.get("start_date") == "YYYY-MM-DD" and metadata.get("outputs", []):
            pid = project_lookup[metadata.get("project_name")]
            for output in metadata.get("outputs", []):
                try:
                    output_date = pd.to_datetime(output["date"]).date()
                except Exception as e:
                    print(f"\t ** Output {output["name"]} - date invalid: {output["date"]}. Setting 'today' as date.")
                    output_date = pd.to_datetime("today").date()

                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "project_id": pid,
                        "output_id": output_lookup[output["type"]],
                        "name": output["name"],
                        "url": output["url"],
                        "date": output_date,
                    }
                )

    return pd.DataFrame(rows)
