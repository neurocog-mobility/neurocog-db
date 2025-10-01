import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_projects(config, program_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        rows.append(
            {
                "id": str(uuid.uuid4()),
                "name": data["project_name"],
                "ethics": data.get("ethics"),
                "status": data.get("status"),
                "start_date": pd.to_datetime(data.get("start_date")).date(),
                "end_date": pd.to_datetime(data.get("end_date")).date(),
                "data_path": data.get("data_path"),
                "program_id": program_lookup[data["program"]],
                "source_path": str(f),
            }
        )

    df = pd.DataFrame(rows)
    return df, create_lookup(df)
