#%%
import duckdb
from neurocogdb.config.paths import fetch_ddb_path

# open your database file
con = duckdb.connect(fetch_ddb_path())

# list all tables
print(con.execute("SHOW TABLES;").fetchdf())

#%
# preview the data_sources table
df = con.execute("SELECT * FROM data LIMIT 10;").fetchdf()
print(df)

con.close()

#%%
from neurocogdb.transform.build import build_dataframes

_ = build_dataframes()