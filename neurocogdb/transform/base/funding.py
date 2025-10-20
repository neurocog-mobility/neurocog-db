import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_funding(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "funding")

    funding = set()
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("program_name") == "Program Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            funding_entries = metadata.get("funding", [])
            for entry in funding_entries:
                funding.update([entry["organization"].strip().replace("_", " ")])

    df = pd.DataFrame([{"id": str(uuid.uuid4()), "organization": n} for n in funding])
    return df, create_lookup(df, lookup_column="organization")
