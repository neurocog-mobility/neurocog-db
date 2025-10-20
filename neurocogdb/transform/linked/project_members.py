import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files
from neurocogdb.transform.utils import create_lookup


def build_project_members(config, project_lookup, df_members, member_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("project_name") == "Project Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            pid = project_lookup[metadata.get("project_name")]
            for member in metadata.get("members", []):
                # handle erroneous members
                if not member in member_lookup.keys():
                    df = pd.DataFrame(
                        {
                            "id": [str(uuid.uuid4())],
                            "name": [member],
                            "role": ["na"],
                            "active": [True],
                            "valid": [False],
                        }
                    )
                    df_members = pd.concat([df_members, df])
                    member_lookup = create_lookup(df_members)

                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "project_id": pid,
                        "member_id": member_lookup[member],
                    }
                )

    return pd.DataFrame(rows), df_members, member_lookup
