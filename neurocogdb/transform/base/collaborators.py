import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_collaborators(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "collaborators")

    collaborators = set()
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("program_name") == "Program Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            collaborator_entries = metadata.get("collaborators", [])
            for entry in collaborator_entries:
                collaborators.update([frozenset(entry.items())])

    collaborators = [dict(c) for c in collaborators]

    df = pd.DataFrame([{"id": str(uuid.uuid4()), **c} for c in collaborators])
    return df, create_lookup(df)
