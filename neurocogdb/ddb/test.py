#%%
import duckdb, os

db_path = os.path.join(os.path.dirname(__file__), "lab_catalog.ddb")
con = duckdb.connect(db_path)
print(con.execute("SHOW TABLES").fetchall())

#%%
print(con.execute("DESCRIBE projects").fetchall())
