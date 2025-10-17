import dash
from dash import dcc, html, Input, Output, State, callback_context
from neurocogdb.ddb.network import load_network_elements
from neurocogdb.gui.layouts import explore
from neurocogdb.gui.assets.cyto_style import STYLESHEET
from collections import defaultdict, deque

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


@dash.callback(
    Output("network-graph", "stylesheet"),
    Input("network-graph", "tapNodeData"),
    Input("reset-highlight", "n_clicks"),
    State("network-graph", "stylesheet"),
)
def update_highlight(data, reset_clicks, current_styles):
    ctx = callback_context
    if not ctx.triggered:
        return STYLESHEET

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Reset button clicked
    if triggered_id == "reset-highlight":
        return STYLESHEET
    
    node_id = data["id"]
    # Build adjacency list
    adj = defaultdict(set)
    for e in edges:
        s, t = e["data"]["source"], e["data"]["target"]
        adj[s].add(t)
        adj[t].add(s)

    # BFS up to depth=2
    depth = 2
    levels = {node_id: 0}
    queue = deque([(node_id, 0)])
    while queue:
        node, d = queue.popleft()
        if d >= depth:
            continue
        for nbr in adj[node]:
            if nbr not in levels:
                levels[nbr] = d + 1
                queue.append((nbr, d + 1))

    # Define gradient colors for each level
    level_colors = {
        0: "#FF3300",
        1: "#FFA970",
        2: "#FFF8C6",
    }

    # Generate highlight styles
    highlight_styles = []

    # Dim everything else
    highlight_styles.append({
        "selector": "node",
        "style": {"opacity": 0.25},  # dim all nodes first
    })
    highlight_styles.append({
        "selector": "edge",
        "style": {"opacity": 0.1},  # dim all edges
    })

    # Highlight selected + neighbor nodes
    for n_id, d in levels.items():
        color = level_colors.get(d, "#FFF8C6")
        highlight_styles.append({
            "selector": f'node[id = "{n_id}"]',
            "style": {
                "color": "black",
                "background-color": color,
                "border-color": color,
                "border-width": 4 - d,
                "opacity": 1.0,
            },
        })

    # Highlight connecting edges
    for e in edges:
        s, t = e["data"]["source"], e["data"]["target"]
        if s in levels and t in levels:
            c = level_colors.get(max(levels[s], levels[t]), "#FFF8C6")
            highlight_styles.append({
                "selector": f'edge[source = "{s}"][target = "{t}"]',
                "style": {"line-color": c, "width": 3 - 0.5 * max(levels[s], levels[t]), "opacity": 1.0},
            })

    return STYLESHEET + highlight_styles

# @dash.callback(
#     Output("network-graph", "stylesheet"),
#     Input("reset-highlight", "n_clicks"),
# )
# def reset_highlight(n_clicks):
#     return STYLESHEET