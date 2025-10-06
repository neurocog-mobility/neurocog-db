# gui/callbacks/home_callbacks.py
from dash import Input, Output
from neurocogdb.gui.layouts import home  # reference to layouts/home if needed

def register_callbacks(app):
    # Example: button to refresh project counts
    @app.callback(
        Output("projects-card", "children"),
        Input("refresh-button", "n_clicks"),
        prevent_initial_call=True
    )
    def refresh_projects(_):
        project_count, _, _ = home.fetch_status()
        return f"{project_count} total"
