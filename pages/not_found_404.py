import dash
from dash import html, dcc

dash.register_page(__name__, title="404")

layout = html.Div("No Resource can be found at this URL")
