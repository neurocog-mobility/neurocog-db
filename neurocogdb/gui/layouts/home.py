# gui/layouts/home.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from neurocogdb.ddb import queries
import plotly.express as px


def format_plot(fig):
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )


def layout():
    # --- Queries ---
    project_status = queries.get_project_status_counts()
    participants = queries.get_participants_per_project()
    timeline = queries.get_project_timeline().sort_values(by="start_date")
    locations = queries.get_locations_summary()
    funding = queries.get_funding_summary()

    # --- Charts ---
    # Top: project status card
    active_count = int(
        project_status.loc[project_status["status"] == "active", "count"].sum()
    )
    completed_count = int(
        project_status.loc[project_status["status"] == "completed", "count"].sum()
    )
    upcoming_count = int(
        project_status.loc[project_status["status"] == "upcoming", "count"].sum()
    )

    # Top: participants per project bar
    part_chart = px.bar(
        participants,
        x="project",
        y=["collected", "target"],
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
    )
    part_chart.update_layout(
        yaxis_title="# Participants",
        xaxis_title="Project",
        legend_title_text="",
    )
    part_chart.update_layout(template="plotly_dark")
    part_chart.update_layout(barcornerradius=15)
    format_plot(part_chart)

    # Middle: Gantt-style timeline
    gantt_chart = px.timeline(
        timeline,
        x_start="start_date",
        x_end="end_date",
        y="name",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
    )
    gantt_chart.update_layout(
        yaxis_title="",
    )
    gantt_chart.update_yaxes(autorange="reversed")
    gantt_chart.update_layout(barcornerradius=15)
    format_plot(gantt_chart)

    # Bottom: tables
    loc_table = dbc.Table.from_dataframe(
        locations,
        striped=True,
        bordered=True,
        hover=True,
        color="primary",
    )
    fund_table = dbc.Table.from_dataframe(
        funding, striped=True, bordered=True, hover=True, color="primary"
    )

    # --- Layout ---
    return dbc.Container(
        [
            # Top row
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Projects"),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.H3(
                                                    [
                                                        html.Span(
                                                            "Active: ",
                                                            style={
                                                                "fontWeight": "bold"
                                                            },
                                                        ),
                                                        html.Span(
                                                            f"{active_count}",
                                                            style={
                                                                "fontWeight": "normal"
                                                            },
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="text-center",
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    [
                                                        html.Span(
                                                            "Completed: ",
                                                            style={
                                                                "fontWeight": "bold"
                                                            },
                                                        ),
                                                        html.Span(
                                                            f"{completed_count}",
                                                            style={
                                                                "fontWeight": "normal"
                                                            },
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="text-center",
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    [
                                                        html.Span(
                                                            "Upcoming: ",
                                                            style={
                                                                "fontWeight": "bold"
                                                            },
                                                        ),
                                                        html.Span(
                                                            f"{upcoming_count}",
                                                            style={
                                                                "fontWeight": "normal"
                                                            },
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="text-center",
                                        ),
                                    ],
                                ),
                            ],
                            color="primary",
                            inverse=True,
                            style={"width": "100%", "height": "100%"},
                            className="shadow-sm rounded-3",
                        ),
                        className="d-flex align-items-center justify-content-center",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Active projects per location"),
                                dbc.CardBody(
                                    html.Div(
                                        loc_table,
                                        style={
                                            "overflowY": "scroll",
                                            "overflowX": "scroll",
                                            "border": "1px solid #dee2e6",
                                        },
                                        className="rounded",
                                    )
                                ),
                            ],
                            color="primary",
                            inverse=True,
                            style={"width": "100%", "height": "100%"},
                            className="shadow-sm rounded-3",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Funding sources"),
                                dbc.CardBody(
                                    html.Div(
                                        fund_table,
                                        style={
                                            "overflowY": "scroll",
                                            "overflowX": "scroll",
                                            "border": "1px solid #dee2e6",
                                        },
                                        className="rounded",
                                    )
                                ),
                            ],
                            color="primary",
                            inverse=True,
                            style={"width": "100%", "height": "100%"},
                            className="shadow-sm rounded-3",
                        )
                    ),
                ],
                justify="center",
                className="mb-4",
                style={"padding": "24px", "height": "300px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Project timelines"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        figure=gantt_chart,
                                        style={"width": "100%", "height": "300px"},
                                        config={
                                            "displayModeBar": False,
                                        },
                                    ),
                                ),
                            ],
                            color="primary",
                            inverse=True,
                            style={"width": "100%"},
                            className="shadow-sm rounded-3",
                        ),
                        className="d-flex align-items-center justify-content-center",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Participants per active project"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        figure=part_chart,
                                        style={"width": "100%", "height": "300px"},
                                        config={
                                            "displayModeBar": False,
                                        },
                                    ),
                                ),
                            ],
                            color="primary",
                            inverse=True,
                            className="shadow-sm rounded-3",
                            style={"width": "100%"},
                        ),
                        className="d-flex align-items-center justify-content-center",
                    ),
                ],
                justify="center",
                className="mb-4",
            ),
        ],
        fluid=True,
        style={"width": "80vw"},
    )
