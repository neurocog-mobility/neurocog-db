import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files

def build_locations(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "locations")

    set_location_names = set()
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("project_name") == "Project Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            set_location_names.update([c["name"] for c in metadata.get("location", [])])

    df = pd.DataFrame([{"id": str(uuid.uuid4()), "name": n} for n in set_location_names])
    return df, create_lookup(df)