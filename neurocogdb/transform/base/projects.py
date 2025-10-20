import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_projects(config, df_programs, program_lookup):
    yaml_files = find_yaml_files(config["rootpath"], config, "projects")

    rows = []
    for f in yaml_files:
        data = load_yaml(f)
        # if not template
        if not data["project_name"] == "Project Name" and not data.get("start_date") == "YYYY-MM-DD":
            start_date = pd.to_datetime(data.get("start_date")).date()
            # check for valid end date
            if data.get("end_date") == "YYYY-MM-DD":
                end_date = start_date + pd.DateOffset(years=1)
            else:
                end_date = pd.to_datetime(data.get("end_date")).date()

            # check for valid program
            # handle erroneous members
            if not data["program"] in program_lookup.keys():
                df = pd.DataFrame(
                    {
                        "id": [str(uuid.uuid4())],
                        "name": [data["program"]],
                        "start_date": [start_date],
                        "end_date": [end_date],
                        "source_path": [""],
                    }
                )
                df_programs = pd.concat([df_programs, df])
                program_lookup = create_lookup(df_programs)
            
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": data["project_name"],
                    "ethics": data.get("ethics"),
                    "start_date": start_date,
                    "end_date": end_date,
                    "data_path": data.get("data_path"),
                    "program_id": program_lookup[data["program"]],
                    "source_path": str(f),
                }
            )

    df = pd.DataFrame(rows)
    return df, create_lookup(df), df_programs, program_lookup
