"""
CO2 Emissions
This change is for me : Karan
"""
import pandas as pd

import dash
from dash import html, dcc, Input, Output, callback, clientside_callback, State
import dash_bootstrap_components as dbc

import pydeck as pdk
import dash_deck

# register this page in dash
dash.register_page(
    __name__,
    path='/co2-graph/',
    name="CO2 Emission Levels around Switzerland",
    title='CO2 Emissions',
)

# data preprocessing
mapbox_api_token = "pk.eyJ1Ijoia2FyYW4tcy1taXR0YWwiLCJhIjoiY2s4bHRhb3RlMDUyMjNubjh5N3R1dmNydSJ9.e6Y_UslQeahIikTwsRny3w"

# ----------------------------------------------------------------
# Old Code
# ----------------------------------------------------------------
# re_cash = pd.read_csv("./data/co2_landscape.csv")
# re_cash.info()
# re_cash.head()

# re_cash_columns = re_cash.iloc[
#     :, [7, 8, 14, 15, 23]
# ]  # select column 14 und 15 (canton, community,  Longtitude, Latitude)
# re_cash_columns.info()
# re_cash_columns.head()

# # Daten für Kanton und Gemeinde
# re_cash_columns_canton = re_cash_columns.loc[re_cash_columns["GDEKT"] == "AG"]
# re_cash_columns_community = re_cash_columns.loc[
#     re_cash_columns["GDENAME"] == "Windisch"
# ]
# re_cash_columns_community.info()
# re_cash_columns_community.head()

# re_cash_columns_random = re_cash_columns.sample(frac=0.10, random_state=12)
# re_cash_columns_random.info()
# re_cash_columns_random.head()

# re_cash_columns.to_csv("re_cash_columns_random.csv", index=False)
# ----------------------------------------------------------------

# filter_list = ["GDEKT", "GDENAME", "Latitude", "Longitude", "co2_m2", "co2"]
# filtered_df = new_df[filter_list]
# filtered_df.to_parquet("filtered_df.parquet")

# main_df = pd.read_parquet("./data/re_cash_columns.parquet")
data_url = "https://github.com/Karan-S-Mittal/recash-dashdeck/blob/main/data/filtered_df.parquet?raw=true"
filtered_df = pd.read_parquet(data_url)
# tooltip = {
#     "html": "<b>Elevation Value:</b> {elevationValue}",
#     "style": {"backgroundColor": "steelblue", "color": "white"},
# }

# layer = pdk.Layer(
#     "HexagonLayer",  # `type` positional argument is here
#     main_df,
#     get_position=["Longitude", "Latitude"],
#     auto_highlight=True,
#     elevation_scale=20,
#     pickable=True,
#     elevation_range=[0, 3000],
#     extruded=True,
#     coverage=1,
# )

# view_state = pdk.ViewState(
#     longitude=8.1355,
#     latitude=46.7,
#     zoom=7,
#     min_zoom=6,
#     max_zoom=15,
#     pitch=40.5,
#     bearing=-20.36,
# )

# TOOLTIP_TEXT = {
#     "html": "<b>Elevation Value:</b> {elevationValue}",
#     "style": {
#         "backgroundColor": "steelblue",
#         "color": "white",
#     },
# }

# # Combined all of it and render a viewport
# r = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     tooltip=TOOLTIP_TEXT,
#     api_keys={"mapbox": mapbox_api_token},  # new line
#     map_provider="mapbox",
#     map_style=pdk.map_styles.ROAD,  # new line
# )

# Dash Code

tab_style = {"height": "calc(100vh - 230px)", "padding": "15px"}

gde_name_list = list(filtered_df["GDENAME"].unique())

controls = html.Div([
    html.H4("Select Community Name(GDE Name)"),
    dcc.Dropdown(
        id="map-controls-gde",
        options=gde_name_list + ["All Communities"],
        value=gde_name_list[0],
        multi=True,
        clearable=False,
    ),
    html.Hr(),
    html.H4("Select Map Type"),
    dcc.Dropdown(
        id="map-controls-type",
        options=[
            {"label": "ROAD", "value": "ROAD"},
            {"label": "SATELLITE", "value": "SATELLITE"},
            {"label": "DARK", "value": "DARK"},
            {"label": "LIGHT", "value": "LIGHT"},
        ],
        value="DARK",
        clearable=False,
    ),
    html.Hr(),
    html.H4("Select Area Radius"),
    dcc.Input(id="map-controls-radius", type="number",
              value=200, min=50, max=1_000),
], style=tab_style)

tabs = dbc.Tabs(
    [
        # Description
        dbc.Tab(
            dcc.Markdown([
                """
            ## Data Description

            this is the data dscriptions

            | Tables        | Col Description |
            | ------------- |:---------------:|
            | col 3 is      | right-aligned   |
            | col 2 is      | centered        |
            | zebra stripes | are neat        |

            table 
            EGID                                     number in country cadastre

BAUJ,                                   year of construction      

FLAE                                      building area

GES,

GKAT                                    Building category                           

n_eingange                       number of entries to the building

GDEKT                                  community category

GDENAME                          community name

GDENR                                 community number

STRNAME                           street name

DEINR                                   street number                 

PLZ4                                      zip code                             

PLZNAME                           community name (redundant to GDENAME)

Latitude                               latitude

Longitude                           longitude

CH_BEZ_D                          zone

BAUJK_qual                       Quality Index related to year of construction

FLAE_qual                          Quality Index related to area

GES_qual,                           Quality Index related to year of construction

EBF                                        energy consumption area

Nutzung                              usage

HGT                                       heating degree days

co2_m2                               co2 emmisions / quare meter building area

co2                                        co2 emmission absolut value

kwh_m2                              kilowatt / square meter building area

kwh                                       kilowatt absolute value
            """
            ],
                id="description", style=tab_style
            ),
            label="Description"),
        # Controls if any
        dbc.Tab(
            controls,
            label="Controls"),
    ]
)


layout = dbc.Row([
    dbc.Col(
        dbc.Card(
            html.H1("Loading..."),
            id="deck-card",
            body=True
        ),
        md=8,
    ),
    dbc.Col([tabs], md=4),
    # dcc.Store stores the intermediate value
    # dcc.Store(id='store-data', storage_type='memory'),
])


map_view = pdk.View("MapView", controller=True)


@callback(
    Output('deck-card', 'children'),
    [
        Input('map-controls-gde', "value"),
        Input('map-controls-type', 'value'),
        Input("map-controls-radius", "value")
    ],
)
def update_graph(gde_list, map_type, map_radius=200):  # , data):
    # convert the json data to pandas dataframe
    # df = pd.read_json(data, orient='split')
    # print(df)
    # filter the dataframe by the selected value
    # df = main_df.loc[main_df["GDENAME"].isin(value)]
    # convert the dataframe to json format and store the data in dcc.store
    print(gde_list)
    if gde_list == "All Communities" or gde_list == ["All Communities"]:
        df = filtered_df
    elif type(gde_list) == list:
        df = filtered_df[filtered_df["GDENAME"].isin(gde_list)]
    else:
        df = filtered_df[filtered_df["GDENAME"].isin([gde_name_list[0]])]
    # print(gde_list)

    TOOLTIP_TEXT = {
        "html": "<b>CO2 M2 Emissions:</b> {co2_m2}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
        },
    }

    if not map_radius or type(map_radius) != "int":
        map_radius = 200

    layer = pdk.Layer(
        "ColumnLayer",  # `type` positional argument is here
        df,
        get_position=["Longitude", "Latitude"],
        get_elevation="co2_m2",
        auto_highlight=True,
        elevation_scale=500,
        pickable=True,
        elevation_range=[0, 3_000],
        extruded=True,
        coverage=1,
        radius=int(map_radius),
        get_fill_color=["co2_m2 * 5", "co2_m2 * 10", 0],  # r, G, b
    )

    view_state = pdk.ViewState(
        longitude=8.1355,
        latitude=46.7,
        zoom=7,
        min_zoom=6,
        max_zoom=15,
        pitch=40.5,
        bearing=-20.36,
    )

    # Combined all of it and render a viewport
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        api_keys={"mapbox": mapbox_api_token},  # new line
        map_provider="mapbox",
        map_style=map_type.lower(),  # new line
        views=[map_view],
    )

    result = dash_deck.DeckGL(
        data=r.to_json(),
        tooltip=TOOLTIP_TEXT,
        mapboxKey=mapbox_api_token,
        style={"height": "calc(100vh - 110px)"}
    ),

    return result
