# %%
import yaml
import tkinter as tk
from tkinter import filedialog, simpledialog
from importlib import resources
import os


def choose_folder():
    """
    Opens a dialog box for the user to select a folder.
    Returns the path of the selected folder or an empty string if canceled.
    """
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open the folder selection dialog
    folder_path = filedialog.askdirectory(title="Select a Folder")

    # Destroy the hidden root window
    root.destroy()

    return folder_path or ""


def choose_folder_textbox():
    """
    Opens a textbox dialog for the user to paste a folder path.
    Returns the entered path or an empty string if canceled.
    """
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Ask user to enter the path
    folder_path = simpledialog.askstring(
        "Input", "Enter the neurocog drive folder path:"
    )

    root.destroy()
    return folder_path or ""


def config_root_path():
    dirname = choose_folder_textbox()
    if dirname=="":
        rootdir = None
    else:
        rootdir = os.path.abspath(os.path.expanduser(dirname))

    package_name = "neurocogdb.config"
    yaml_file_path = "config.yaml"

    try:
        with resources.files(package_name).joinpath(yaml_file_path).open("r") as f:
            data = yaml.safe_load(f)

        data["rootpath"] = rootdir

        with resources.files(package_name).joinpath(yaml_file_path).open("w") as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"Configuration root path successfully updated.")

    except FileNotFoundError:
        print(
            f"Error: YAML file '{yaml_file_path}' not found in package '{package_name}'."
        )
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")


def confirm_root_path():
    package_name = "neurocogdb.config"
    yaml_file_path = "config.yaml"

    try:
        with resources.files(package_name).joinpath(yaml_file_path).open("r") as f:
            data = yaml.safe_load(f)

        print("Currently configured neurocog drive folder path: ", data["rootpath"])

    except FileNotFoundError:
        print(
            f"Error: YAML file '{yaml_file_path}' not found in package '{package_name}'."
        )
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")


def fetch_ddb_path():
    package_name = "neurocogdb.ddb"
    ddb_file_path = "lab_catalog.ddb"
    return resources.files(package_name).joinpath(ddb_file_path) or ""
