# gui/layouts/home.py
import dash
from neurocogdb.gui.layouts import home

dash.register_page(__name__, path="/")

layout = home.layout()