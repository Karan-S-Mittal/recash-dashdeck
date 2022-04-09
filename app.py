import os
from importlib import import_module

from tqdm import tqdm

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

import pages_plugin

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MORPH],
    suppress_callback_exceptions=True,
    plugins=[pages_plugin],
)

server = app.server


def Header(name, app):
    title = html.H1(name, style={"marginTop": 5})
    logo = html.Img(
        src=app.get_asset_url("images/pom-logo.png"), style={"float": "right", "height": 40, "marginTop": 20, "marginRight": 40}
    )
    link = html.A(
        logo,
        href="https://www.pom.ch/en/about-us/"
    )

    result = dbc.Row([
        dbc.Col(title, md=6, align="center"),
        dbc.Col(link, md=6, align="center", style={"textAlign": "center"}),
    ],
        align="center",
        className="alert border border-info"
    )
    return result


def format_graph_name(graph_name):
    """
    Formats Graph Name
    """
    return graph_name.replace("graph_", "").replace("_", " ").title()


# ------------------------------------------------------------------------------
# Add the pages/graphs to this list to ignore them while loading
# ------------------------------------------------------------------------------
ignored_graphs = ["graph_name.py", ]

graph_list = [
    n.replace(".py", "")
    for n in sorted(os.listdir("./pages"))
    if n.endswith(".py") and n not in ignored_graphs
]

graph_modules = {
    graph: import_module(f"pages." + graph)
    for graph in tqdm(graph_list)
}

print(f"Loading Demos: {graph_list}")


app_selection = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(page["name"], href=page["path"])
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    ],
    # className="btn btn-outline-success",
    toggleClassName="btn btn-outline-success",
    label="Reports",
    direction="end",
    style={
        "text-align": "center",
    },
)

layout = [
    Header("Pollution & CO2 Emissions Report", app),
    dbc.Row([
        dbc.Col(app_selection, md=10),
    ], justify="center", align="center", style={"marginBottom": 20}),
    dbc.Row(pages_plugin.page_container,  align="center")
]

app.layout = dbc.Container(layout, fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
