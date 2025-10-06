import dash
from dash import dcc, html, Input, Output, State
from neurocogdb.ddb.network import load_network_elements
from neurocogdb.gui.layouts import explore

dash.register_page(__name__, path="/explore")

nodes, edges = load_network_elements()
ALL_ELEMENTS = nodes + edges
layout = explore.layout(ALL_ELEMENTS)

@dash.callback(
    Output("network-graph", "elements"),
    Input("node-type-filter", "value"),
    Input("filter-status", "value"),  # NEW
)
def filter_nodes(selected_types, selected_statuses):
    # Filter nodes based on both type and status
    filtered_nodes = [
        n
        for n in nodes
        if n["data"]["type"] in selected_types
        and not n["data"]["type"]=="project"#n["data"].get("status") in selected_statuses
    ]
    filtered_nodes_project = [
        n
        for n in nodes
        if n["data"]["type"] in ["project"]
        and n["data"].get("status") in selected_statuses
    ]
    if "project" in selected_types:
        filtered_nodes += filtered_nodes_project

    # Keep only edges that connect visible nodes
    keep_ids = {n["data"]["id"] for n in filtered_nodes}
    filtered_edges = [
        e
        for e in edges
        if e["data"]["source"] in keep_ids and e["data"]["target"] in keep_ids
    ]

    return filtered_nodes + filtered_edges

# @dash.callback(
#     Output("network-graph", "elements"),
#     Input("node-type-filter", "value"),
# )
# def filter_nodes(selected_types):
#     # Keep only nodes of selected types and edges that connect them
#     filtered_nodes = [n for n in nodes if n["data"]["type"] in selected_types]
#     keep_ids = {n["data"]["id"] for n in filtered_nodes}
#     filtered_edges = [
#         e
#         for e in edges
#         if e["data"]["source"] in keep_ids and e["data"]["target"] in keep_ids
#     ]
#     return filtered_nodes + filtered_edges
