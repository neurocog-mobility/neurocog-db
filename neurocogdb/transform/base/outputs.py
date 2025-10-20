import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_outputs(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "outputs")

    set_output_names = set()
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("project_name") == "Project Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            set_output_names.update([c["type"] for c in metadata.get("outputs", [])])

    df = pd.DataFrame([{"id": str(uuid.uuid4()), "type": n} for n in set_output_names])
    return df, create_lookup(df, lookup_column="type")
