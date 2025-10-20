import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_programs(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        # if not template
        if not metadata.get("program_name") == "Program Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            if metadata.get("end_date") == "YYYY-MM-DD":
                end_date = pd.to_datetime(metadata.get("start_date")).date() + pd.DateOffset(years=5)
            else:
                end_date = pd.to_datetime(metadata.get("end_date")).date()

            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": metadata["program_name"],
                    "start_date": pd.to_datetime(metadata["start_date"]).date(),
                    "end_date": end_date,
                    "source_path": str(f),
                }
            )

    df = pd.DataFrame(rows)
    return df, create_lookup(df)
