import dash_bootstrap_components as dbc
from dash import html, dcc

filter_sidebar = dbc.Card(
    [
        dbc.CardHeader("Filters", className="fw-bold text-light bg-primary"),
        dbc.CardBody(
            [
                html.Label("Status", className="text-light small"),
                dbc.Checklist(
                    id="filter-status",
                    options=[
                        {"label": "Ongoing", "value": "ongoing"},
                        {"label": "Completed", "value": "completed"},
                        {"label": "Upcoming", "value": "upcoming"},
                    ],
                    value=["ongoing", "completed", "upcoming"],
                    inline=False,
                    switch=True,
                    className="status-checklist",
                ),
                html.Label("Program", className="text-light small"),
                dcc.Dropdown(
                    id="filter-program",
                    options=[],
                    multi=True,
                    placeholder="Select program...",
                    className="dark-dropdown",
                ),
                html.Br(),
                html.Label("Funding", className="text-light small"),
                dcc.Dropdown(
                    id="filter-funding",
                    options=[],
                    multi=True,
                    placeholder="Select funding...",
                    className="dark-dropdown",
                ),
                html.Br(),
                html.Label("Participant Groups", className="text-light small"),
                dcc.Dropdown(
                    id="filter-participant",
                    options=[],
                    multi=True,
                    placeholder="Select participants...",
                    className="dark-dropdown",
                ),
                html.Br(),
                html.Label("Data Modalities", className="text-light small"),
                dcc.Dropdown(
                    id="filter-data",
                    options=[],
                    multi=True,
                    placeholder="Select data modalities...",
                    className="dark-dropdown",
                ),
                html.Br(),
                html.Label("Output Date Range", className="text-light small"),
                dcc.DatePickerRange(
                    id="date-range-filter",
                    start_date_placeholder_text="Start Date",
                    end_date_placeholder_text="End Date",
                    display_format="YYYY-MM-DD",
                    clearable=True,
                    style={"width": "100%"},
                    className='dark-date-picker'
                ),
            ]
        ),
    ],
    className="shadow-sm bg-primary text-light rounded-3 p-2",
    style={"height": "80vh", "overflowY": "auto"},
)
