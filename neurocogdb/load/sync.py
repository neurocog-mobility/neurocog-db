# %%
from neurocogdb.load.ddb_loader import create_ddb
from neurocogdb.transform.build import build_dataframes
from neurocogdb.extract.finder import load_schema

def sync_ddb():
    dict_tables = build_dataframes()

    if dict_tables:
        for base_table in dict_tables["base"]:
            key, df = list(base_table.items())[0]

            print(key, df.columns)
            schema_sql = load_schema(key)
            create_ddb(df, key, schema_sql)

        for link_table in dict_tables["linked"]:
            key, df = list(link_table.items())[0]

            print(key, df.columns)
            schema_sql = load_schema(key)
            create_ddb(df, key, schema_sql)

if __name__ == "__main__":
    sync_ddb()
