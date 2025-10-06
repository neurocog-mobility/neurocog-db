import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_program_collaborators(config, program_lookup, collaborator_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        pid = program_lookup[metadata["program_name"]]
        for entry in metadata.get("collaborators", []):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "program_id": pid,
                    "collaborator_id": collaborator_lookup[entry["name"]],
                }
            )

    return pd.DataFrame(rows)
