# gui/app.py
import dash
import dash_bootstrap_components as dbc
import webbrowser, threading

def create_app():
    # Initialize Dash with multipage support
    app = dash.Dash(
        __name__,
        use_pages=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.SANDSTONE],
    )

    # Navbar (static across all pages)
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Projects", href="/projects")),
            dbc.NavItem(dbc.NavLink("Explore", href="/explore")),
        ],
        brand="NeuroCog Dashboard",
        color="primary",
        dark=True,
    )

    # Layout = Navbar + page container
    app.layout = dbc.Container(
        [
            navbar,
            dash.page_container,  # this auto-switches content
        ],
        fluid=True,
    )

    return app


def run_app(host="127.0.0.1", port="8050", debug=True):
    app = create_app()

    # def open_browser():
    #     webbrowser.open_new(f"http://{host}:{port}/")

    # # Run browser opener in background so it doesn’t block server
    # threading.Timer(1, open_browser).start()

    # # Start server
    app.run(debug=debug, port=port)


# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
