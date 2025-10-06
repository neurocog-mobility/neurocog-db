from neurocogdb.gui.components import project_filter
import dash_bootstrap_components as dbc
from dash import html


def layout():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(project_filter.filter_sidebar, width=3),
                    dbc.Col(
                        html.Div(
                            id="project-list",
                            style={
                                "height": "90vh",
                                "overflowY": "scroll",
                                "paddingRight": "1rem",
                            },
                        ),
                        width=9,
                    ),
                ],
                className="pt-3",
            )
        ],
        fluid=True,
    )
