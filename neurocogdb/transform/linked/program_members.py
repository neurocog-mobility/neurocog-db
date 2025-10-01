import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_program_members(config, program_lookup, member_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        pid = program_lookup[data["program_name"]]
        for name in data.get("lead", []):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "program_id": pid,
                    "member_id": member_lookup[name],
                    "role": "lead",
                }
            )
        for name in data.get("members", []):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "program_id": pid,
                    "member_id": member_lookup[name],
                    "role": "member",
                }
            )
        for c in data.get("collaborators", []):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "program_id": pid,
                    "member_id": member_lookup[c["name"]],
                    "role": "collaborator",
                }
            )
    return pd.DataFrame(rows)
