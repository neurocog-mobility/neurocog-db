import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_members(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "members")

    names = set()
    for f in yaml_files:
        data = load_yaml(f)

        if "program" in f:
            names.update(data.get("lead", []))
            names.update(data.get("members", []))
            names.update([c["name"] for c in data.get("collaborators", [])])
        elif "project" in f:
            names.update(data.get("members", []))

    df = pd.DataFrame([{"id": str(uuid.uuid4()), "name": n} for n in names])
    return df, create_lookup(df)
