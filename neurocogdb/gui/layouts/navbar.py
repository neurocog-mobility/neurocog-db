# gui/layouts/navbar.py
import dash_bootstrap_components as dbc

def layout():
    return dbc.NavbarSimple(
        brand="NeuroCog Lab Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Projects", href="/projects")),
            dbc.NavItem(dbc.NavLink("Participants", href="/participants")),
        ],
    )
