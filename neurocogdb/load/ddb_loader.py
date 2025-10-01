import duckdb
import os

def create_ddb(df, table_name, schema_sql):
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from load/ to src/
    ddb_dir = os.path.join(base_dir, "ddb")
    os.makedirs(ddb_dir, exist_ok=True)

    db_path = os.path.join(ddb_dir, "lab_catalog.ddb")

    con = duckdb.connect(db_path)

    # Drop table if it already exists
    con.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Recreate table
    con.execute(f"CREATE TABLE {table_name} ({schema_sql})")

    # Register the dataframe as a temporary view
    con.register("df_view", df)

    # Insert everything
    con.execute(f"""
        INSERT INTO {table_name}
        SELECT * FROM df_view
    """)

    con.unregister("df_view")
    con.close()


