import dash
from dash import Input, Output, callback
from neurocogdb.ddb.queries import load_projects
from neurocogdb.gui.components import project_cards
from neurocogdb.gui.layouts import projects
import pandas as pd

# Register the page with the router
dash.register_page(__name__, path="/projects", name="Projects")

layout = projects.layout()


@callback(
    Output("project-list", "children"),
    Output("filter-program", "options"),
    Output("filter-funding", "options"),
    Output("filter-participant", "options"),
    Output("filter-data", "options"),
    Input("filter-status", "value"),
    Input("filter-program", "value"),
    Input("filter-funding", "value"),
    Input("filter-participant", "value"),
    Input("filter-data", "value"),
    Input("date-range-filter", "start_date"),
    Input("date-range-filter", "end_date"),
)
def update_projects(
    selected_status,
    selected_programs,
    selected_funding,
    selected_participants,
    selected_data,
    start_date,
    end_date,
):
    # Load projects
    df = load_projects()

    # Build filter options
    all_programs = [f["name"] for lst in df["program"] for f in lst]
    program_opts = sorted(set(all_programs))
    # program_opts = sorted(df["program"].dropna().unique())

    # Funding
    all_funders = [f["organization"] for lst in df["funding"] for f in lst]
    all_funders = [funder if funder else "NA" for funder in all_funders]
    funding_opts = sorted(set(all_funders))

    # Participants
    all_participants = [p["label"] for lst in df["participant_groups"] for p in lst]
    participant_opts = sorted(set(all_participants))

    # Data modalities
    all_modalities = [d["modality"] for lst in df["data_sources"] for d in lst]
    data_opts = sorted(set(all_modalities))

    # Filter dataframe
    filtered = df.copy()

    # Filter by status
    if selected_status:
        filtered = df[df["status"].isin(selected_status)]

    if selected_programs:
        # filtered = filtered[filtered["program"].isin(selected_programs)]
        filtered = filtered[
            filtered["program"].apply(
                lambda lst: any(f["name"] in selected_programs for f in lst)
            )
        ]

    if selected_funding:
        filtered = filtered[
            filtered["funding"].apply(
                lambda lst: any(f["organization"] in selected_funding for f in lst)
            )
        ]

    if selected_participants:
        filtered = filtered[
            filtered["participant_groups"].apply(
                lambda lst: any(p["label"] in selected_participants for p in lst)
            )
        ]

    if selected_data:
        filtered = filtered[
            filtered["data_sources"].apply(
                lambda lst: any(d["modality"] in selected_data for d in lst)
            )
        ]

    if start_date:
        filtered = filtered[
            filtered["outputs"].apply(
                lambda lst: any(
                    pd.to_datetime(o["date"]) >= pd.to_datetime(start_date) for o in lst
                )
            )
        ]
    if end_date:
        filtered = filtered[
            filtered["outputs"].apply(
                lambda lst: any(
                    pd.to_datetime(o["date"]) <= pd.to_datetime(end_date) for o in lst
                )
            )
        ]

    # Generate cards
    cards = [project_cards.make_project_card(row) for _, row in filtered.iterrows()]

    return cards, program_opts, funding_opts, participant_opts, data_opts
