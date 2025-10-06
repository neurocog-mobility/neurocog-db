import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_members(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "members")

    for f in yaml_files:
        metadata = load_yaml(f)

        df = pd.DataFrame([{"id": str(uuid.uuid4()), **m, "valid": True} for m in metadata.get("members", [])])
        return df, create_lookup(df)

