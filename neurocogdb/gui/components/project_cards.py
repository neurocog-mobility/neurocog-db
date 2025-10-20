import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import json


def make_project_card(row):
    # Parse JSON arrays
    participants = row["participant_groups"] or []
    data_sources = row["data_sources"] or "[]"
    outputs = row["outputs"] or "[]"
    members = row["members"] or "[]"

    # Build participant table
    if participants:
        dfp = pd.DataFrame(participants)
        dfp.loc[len(dfp)] = {
            "label": "All",
            "collected": dfp["collected"].sum(),
            "total": dfp["total"].sum(),
        }
        dfp.columns = ["Group", "Collected", "Target"]
        tbl_participants = dbc.Table.from_dataframe(
            dfp, striped=True, bordered=True, hover=True, color="dark", size="sm"
        )
    else:
        tbl_participants = {}

    # Status color mapping
    status_color = {
        "ongoing": "warning",
        "completed": "success",
        "upcoming": "info",
    }.get(row["status"], "secondary")

    # Program label
    program_label = [
        (
            program["name"] + " ✅"
            if not program["source"] == ""
            else program["name"] + " ❗"
        )
        for program in row["program"]
    ]
    # Funding label
    funding_label = [funder["organization"] if funder["organization"] else "NA" for funder in row["funding"]]

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5(row["name"], className="mb-0"),
                    html.Span(
                        row["status"].capitalize(),
                        className=f"badge bg-{status_color} ms-2",
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Small(
                                        f"Program: {", ".join(program_label) or '—'}",
                                        className="text-light d-block",
                                    ),
                                    html.Small(
                                        f"Funding: {", ".join(funding_label) or '—'}",
                                        className="text-light d-block mb-2",
                                    ),
                                    html.Small(
                                        f"Dates: {row['start_date']} → {row['end_date'] or 'ongoing'}",
                                        className="d-block mb-2 text-light",
                                    ),
                                    html.Details(
                                        [
                                            html.Summary("Outputs"),
                                            html.Ul(
                                                [
                                                    html.Li(format_output(o))
                                                    for o in outputs
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Details(
                                        [
                                            html.Summary("Members"),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        [
                                                            html.Span(m["name"]),
                                                            html.Span(
                                                                f" ({m['role']})",
                                                                style={
                                                                    "font-style": "italic",
                                                                    "color": "#777",
                                                                },
                                                            ),
                                                            (
                                                                html.Span(
                                                                    " ✅",
                                                                )
                                                                if m["valid"]
                                                                else " ❗"
                                                            ),
                                                        ]
                                                    )
                                                    for m in members
                                                ]
                                            ),
                                        ],
                                        open=False,
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    tbl_participants,
                                    html.Details(
                                        [
                                            html.Summary("Data sources"),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        f"{d['modality']} – {d['device']}"
                                                    )
                                                    for d in data_sources
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Details(
                                        [
                                            html.Summary("Folder path"),
                                            html.Small(
                                                f"{row['source_path']}",
                                                className="d-block mb-2 text-light",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ],
        className="shadow-sm bg-dark text-light rounded-3 p-2",
        style={"margin-bottom": "16px"},
    )


def status_color(status):
    return {"ongoing": "warning", "completed": "success", "upcoming": "info"}.get(
        status, "secondary"
    )


def make_participant_bar(project):
    import plotly.express as px

    df = project["participant_breakdown"]
    fig = px.bar(df, x="group", y="count", color="status", barmode="stack")
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False
    )
    return fig


def format_output(o):
    if o["url"]=="":
        return [
            html.Span(
                f" {o['name']}",
                style={
                    "color": "#fff",
                },
            ),
            html.Span(
                f" ({o['type']})",
                style={
                    "font-style": "italic",
                    "color": "#777",
                },
            ),
            (
                html.Span(
                    f": {o['date']}",
                    style={"color": "#999"},
                )
            ),
        ]
    else:
        return [
            html.A(
                f" {o['name']}",
                href=o["url"],
                target="_blank",
            ),
            html.Span(
                f" ({o['type']})",
                style={
                    "font-style": "italic",
                    "color": "#777",
                },
            ),
            (
                html.Span(
                    f": {o['date']}",
                    style={"color": "#999"},
                )
            ),
        ]
