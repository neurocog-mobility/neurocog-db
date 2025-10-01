import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_programs(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        rows.append(
            {
                "id": str(uuid.uuid4()),
                "name": data["program_name"],
                "start_date": pd.to_datetime(data["start_date"]).date(),
                "end_date": pd.to_datetime(data["end_date"]).date(),
                "source_path": str(f),
            }
        )

    df = pd.DataFrame(rows)
    return df, create_lookup(df)
