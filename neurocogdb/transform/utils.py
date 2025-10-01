def create_lookup(df, lookup_column="name"):
    return dict(zip(df[lookup_column], df["id"]))
