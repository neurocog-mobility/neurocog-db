# %%
from neurocogdb.config.paths import config_root_path, confirm_root_path
from neurocogdb.extract.finder import load_discovery_config
from neurocogdb.transform.base import (
    data,
    programs,
    projects,
    members,
    funding,
    outputs,
    locations,
    collaborators,
)
from neurocogdb.transform.linked import (
    program_members,
    program_funding,
    program_collaborators,
    project_data,
    project_members,
    project_locations,
    project_outputs,
    project_participants,
)


def build_dataframes():
    config = load_discovery_config()

    if config["rootpath"]:
        # build base
        print("Building base tables... \n")
        print("programs")
        df_programs, program_lookup = programs.build_programs(config)
        print("projects")
        df_projects, project_lookup, df_programs, program_lookup = projects.build_projects(config, df_programs, program_lookup)
        print("members")
        df_members, member_lookup = members.build_members(config)
        print("funding")
        df_funding, funding_lookup = funding.build_funding(config)
        print("data sources")
        df_data, data_lookup = data.build_data(config)
        print("outputs")
        df_outputs, output_lookup = outputs.build_outputs(config)
        print("locations")
        df_locations, location_lookup = locations.build_locations(config)
        print("collaborators")
        df_collaborators, collaborator_lookup = collaborators.build_collaborators(
            config
        )

        # build linked
        print("\n")
        print("Building link tables... \n")
        print("program members")
        df_program_members, df_members, member_lookup = (
            program_members.build_program_members(
                config, program_lookup, df_members, member_lookup
            )
        )
        print("program funding")
        df_program_funding = program_funding.build_program_funding(
            config, program_lookup, funding_lookup
        )
        print("program collaborators")
        df_program_collaborators = program_collaborators.build_program_collaborators(
            config, program_lookup, collaborator_lookup
        )
        print("project members")
        df_project_members, df_members, member_lookup = (
            project_members.build_project_members(
                config, project_lookup, df_members, member_lookup
            )
        )
        print("project participants")
        df_project_participants = project_participants.build_project_participants(
            config, project_lookup
        )
        print("project data sources")
        df_project_data = project_data.build_project_data(
            config, project_lookup, data_lookup
        )
        print("project outputs")
        df_project_outputs = project_outputs.build_project_outputs(
            config, project_lookup, output_lookup
        )
        print("project locations")
        df_project_locations = project_locations.build_project_locations(
            config, project_lookup, location_lookup
        )
        print("\n")

        return {
            "base": [
                {"programs": df_programs},
                {"projects": df_projects},
                {"members": df_members},
                {"data": df_data},
                {"funding": df_funding},
                {"outputs": df_outputs},
                {"locations": df_locations},
                {"collaborators": df_collaborators},
            ],
            "linked": [
                {"program_members": df_program_members},
                {"program_funding": df_program_funding},
                {"program_collaborators": df_program_collaborators},
                {"project_members": df_project_members},
                {"project_data": df_project_data},
                {"project_participants": df_project_participants},
                {"project_outputs": df_project_outputs},
                {"project_locations": df_project_locations},
            ],
        }
    else:
        print("No root directory for NCDrive in config.yaml")
        if input("Would you like to set a root directory? (y/n) ") == "y" or False:
            config_root_path()
            confirm_root_path()
            print("\nIf folder path is correct, please re-run sync command.")

        return None
