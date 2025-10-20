import pandas as pd
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_program_funding(config, program_lookup, funding_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "programs")

    rows = []
    for f in yaml_files:
        metadata = load_yaml(f)
        if not metadata.get("program_name") == "Program Name" and not metadata.get("start_date") == "YYYY-MM-DD":
            pid = program_lookup[metadata.get("program_name")]
            for entry in metadata.get("funding", []):
                name = entry["organization"].strip().replace("_", " ")
                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "program_id": pid,
                        "funding_id": funding_lookup[name],
                        "start_date": pd.to_datetime(entry["start_date"]).date(),
                        "end_date": pd.to_datetime(entry["end_date"]).date(),
                        "notes": entry["notes"],
                    }
                )

    return pd.DataFrame(rows)
