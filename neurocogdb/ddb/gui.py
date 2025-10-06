# gui.py
from flask import Flask, render_template, redirect, url_for
import dash
from dash import html, dcc
import threading, webbrowser

PORT = 8050


def run_gui():
    # Create base Flask app
    server = Flask(__name__)

    # Example route (for login/auth pages if you want later)
    @server.route("/")
    def index():
        return redirect("/dashboard")

    # Attach Dash
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/dashboard/",
    )

    dash_app.layout = html.Div(
        [
            html.H1("NeuroCogDB Dashboard"),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Participants",
                        children=[html.Div("Participants table here")],
                    ),
                    dcc.Tab(label="Studies", children=[html.Div("Studies table here")]),
                    dcc.Tab(label="Data", children=[html.Div("Data cards here")]),
                ]
            ),
        ]
    )

    # Function to open browser
    def open_browser():
        webbrowser.open_new(f"http://127.0.0.1:{PORT}/")

    # Run browser opener in background so it doesn’t block server
    threading.Timer(1, open_browser).start()

    # Start server
    server.run(debug=False, port=PORT)
