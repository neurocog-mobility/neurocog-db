import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files
from neurocogdb.transform.utils import create_lookup


def build_program_members(config, program_lookup, df_members, member_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("program_name") == "Program Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            pid = program_lookup[metadata.get("program_name")]
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