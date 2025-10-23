import pandas as pd
from neurocogdb.transform.utils import create_lookup
from neurocogdb.extract.parse import load_yaml
import uuid
from neurocogdb.extract.finder import find_yaml_files


def build_data(config):
    yaml_files = find_yaml_files(config["rootpath"], config, "data")

    sources = set()
    for f in yaml_files:
        metadata = load_yaml(f)
        if (
            not metadata.get("project_name") == "Project Name"
            and not metadata.get("start_date") == "YYYY-MM-DD"
        ):
            project_sources = metadata.get("data_sources", [])

            for src in project_sources:
                sources.add(tuple(sorted(src.items())))

    dict_sources = [dict(s) for s in sources]
    df = pd.DataFrame(
        [
            {
                "id": str(uuid.uuid4()),
                "category": src["category"],
                "modality": src["modality"],
                "device": src["device"],
            }
            for src in dict_sources
        ]
    )
    df["name"] = [
        f"{s['category']}_{s['modality']}_{s['device']}" for _, s in df.iterrows()
    ]

    return df.drop("name", axis=1), create_lookup(df)
