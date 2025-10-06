import dash_bootstrap_components as dbc
from dash import html, dcc

filter_sidebar = dbc.Card(
    [
        dbc.CardHeader("Filters", className="fw-bold text-light bg-primary"),
        dbc.CardBody(
            [
                dbc.Checklist(
                    id="node-type-filter",
                    options=[
                        {"label": "Programs", "value": "program"},
                        {"label": "Projects", "value": "project"},
                        {"label": "Members", "value": "member"},
                        {"label": "Collaborators", "value": "collaborator"},
                        {"label": "Funding", "value": "funding"},
                    ],
                    value=[
                        "program",
                        "project",
                        "member",
                        "collaborator",
                        "funding",
                    ],
                    inline=False,
                    switch=True,
                    className="status-checklist",
                ),
                html.Br(),
                dbc.Label("Project Status", className="text-light small"),
                dbc.Checklist(
                    id="filter-status",
                    options=[
                        {
                            "label": html.Span(
                                [
                                    # 1. The Orange Marker (a colored dot or square)
                                    html.Span(
                                        "▣\u00a0",
                                        style={
                                            "color": "#ff7f0e",
                                            "font-size": "1.2rem",
                                        },
                                    ),
                                    # 2. The Label Text (white for contrast)
                                    html.Span(
                                        "Ongoing", className="text-white fw-bold"
                                    ),
                                ],
                                # Container style to ensure white text is dominant
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "color": "white",
                                },
                            ),
                            "value": "ongoing",
                        },
                        {
                            "label": html.Span(
                                [
                                    # 1. The Orange Marker (a colored dot or square)
                                    html.Span(
                                        "▣\u00a0",
                                        style={
                                            "color": "#55d655",
                                            "font-size": "1.2rem",
                                        },
                                    ),
                                    # 2. The Label Text (white for contrast)
                                    html.Span(
                                        "Completed", className="text-white fw-bold"
                                    ),
                                ],
                                # Container style to ensure white text is dominant
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "color": "white",
                                },
                            ),
                            "value": "completed",
                        },
                        {
                            "label": html.Span(
                                [
                                    html.Span(
                                        "▣\u00a0",
                                        style={
                                            "color": "#ffffff",
                                            "font-size": "1.2rem",
                                        },
                                    ),
                                    html.Span(
                                        "Upcoming", className="text-white fw-bold"
                                    ),
                                ],
                                # Container style to ensure white text is dominant
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "color": "white",
                                },
                            ),
                            "value": "upcoming",
                        },
                    ],
                    value=["ongoing", "completed", "upcoming"],  # show all by default
                    switch=True,
                    inline=False,
                    className="mb-3 status-checklist",
                ),
            ]
        ),
    ],
    className="shadow-sm bg-primary text-light rounded-3 p-2",
    style={"height": "80vh", "overflowY": "auto"},
)
