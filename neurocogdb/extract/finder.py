# discovery/finder.py
import os
import glob
import yaml
from importlib import resources


def load_schema(table_name):
    package_name = "neurocogdb.config"
    yaml_file_path = "schema.yaml"

    try:
        with resources.files(package_name).joinpath(yaml_file_path).open("r") as f:
            schema = yaml.safe_load(f)

        cols = schema[table_name]
        schema_sql = ", ".join([f"{c['name']} {c['type']}" for c in cols])
        return schema_sql

    except FileNotFoundError:
        print(
            f"Error: YAML file '{yaml_file_path}' not found in package '{package_name}'."
        )

        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

        return None


def load_discovery_config():
    package_name = "neurocogdb.config"
    yaml_file_path = "config.yaml"

    try:
        with resources.files(package_name).joinpath(yaml_file_path).open("r") as f:
            data = yaml.safe_load(f)

        return data
    except FileNotFoundError:
        print(
            f"Error: YAML file '{yaml_file_path}' not found in package '{package_name}'."
        )

        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

        return None


def find_json_files(root, config, table_name):
    """Return all JSON files for a given table based on config.yaml"""
    discovered = []
    sources = config["sources"][table_name]["source"]

    for src in sources:
        pattern = os.path.join(root, src["location"].lstrip("/"), src["filename"])
        for filepath in glob.glob(pattern):
            discovered.append(filepath)

    return discovered


def find_yaml_files(root, config, table_name):
    """Return all YAML files for a given table based on config.yaml"""
    discovered = []
    sources = config["sources"][table_name]["source"]

    for src in sources:
        pattern = os.path.join(root, src["location"].lstrip("/"), src["filename"])
        for filepath in glob.glob(pattern):
            discovered.append(filepath)

    return discovered
