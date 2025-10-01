#%%
import duckdb as ddb

con = ddb.connect(database='lab_catalog.ddb')

df = con.execute("SELECT * FROM funding").fetchdf()

print(df)

con.close()