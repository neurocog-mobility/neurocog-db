# %%
from neurocogdb.config.paths import config_root_path, confirm_root_path
from neurocogdb.extract.finder import load_discovery_config, find_yaml_files
from neurocogdb.transform.base import data, programs, projects, members, funding
from neurocogdb.transform.linked import (
    program_members,
    program_funding,
    project_data,
    project_members,
)


def build_dataframes():
    config = load_discovery_config()

    if config["rootpath"]:
        # build base
        df_programs, program_lookup = programs.build_programs(config)
        df_projects, project_lookup = projects.build_projects(config, program_lookup)
        df_members, member_lookup = members.build_members(config)
        df_funding, funding_lookup = funding.build_funding(config)
        df_data, data_lookup = data.build_data(config)

        # build linked
        df_program_members = program_members.build_program_members(
            config, program_lookup, member_lookup
        )
        df_program_funding = program_funding.build_program_funding(
            config, program_lookup, funding_lookup
        )
        df_project_members = project_members.build_project_members(
            config, project_lookup, member_lookup
        )
        df_project_data = project_data.build_project_data(
            config, project_lookup, data_lookup
        )

        return {
            "base": [
                {"programs": df_programs},
                {"projects": df_projects},
                {"members": df_members},
                {"data": df_data},
                {"funding": df_funding},
            ],
            "linked": [
                {"program_members": df_program_members},
                {"program_funding": df_program_funding},
                {"project_members": df_project_members},
                {"project_data": df_project_data},
            ],
        }
    else:
        print("No root directory for NCDrive in config.yaml")
        if input("Would you like to set a root directory? (y/n) ") == "y" or False:
            config_root_path()
            confirm_root_path()
            print("\nIf folder path is correct, please re-run sync command.")

        return None
