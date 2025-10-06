from neurocogdb.gui.assets.cyto_style import STYLESHEET
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import html
from neurocogdb.gui.components import explore_filter


def layout(elements):
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [explore_filter.filter_sidebar],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            cyto.Cytoscape(
                                id="network-graph",
                                elements=elements,
                                layout={"name": "cose"},
                                style={"width": "100%", "height": "75vh"},
                                stylesheet=STYLESHEET,
                            ),
                        ],
                        width=9,
                    ),
                ],
                className="pt-3",
            )
        ],
        fluid=True,
    )
