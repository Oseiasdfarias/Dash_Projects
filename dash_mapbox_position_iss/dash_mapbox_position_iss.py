from dash import Dash
from dash.html import Div, H1
from dash.dcc import Graph, Interval
from dash.dependencies import Input, Output
import requests as re
import json
import plotly.express as px
import pandas as pd
import numpy as np

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def get_position():
    global df_geoloc
    try:
        satelite = re.get(
            "https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=VUBYSF-UDEB2E-A44UCK-4WK8"
        )

        satelite_json = json.loads(str(satelite.text))

        info = satelite_json["info"]
        position = satelite_json["positions"]

        nam = info["satname"]
        lat = position[1]["satlatitude"]
        lon = position[1]["satlongitude"]
        alt = position[1]["sataltitude"]
        print(f"Nome: {nam}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        print(f"Altitude: {alt}")

        data = np.array([
            [nam, alt, lat, lon],
        ])

        df_geoloc = pd.DataFrame(data, columns=["Nome", "Altitude",
                                            "Latitude", "Longitude"])
    except re.exceptions.Timeout as error:
        print(error)

# Instanciando um Obj
external_stylesheets = [
    'https://unpkg.com/terminal.css@0.7.2/dist/terminal.min.css',
]

app = Dash(__name__, external_scripts=external_stylesheets)

app.layout = Div(
    style={'backgroundColor': colors['background']},
    children=[
        H1(
        children='Posição em Tempo Real da Estação Espacial (ISS)',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        Interval(interval=4000, id="interval"),
        Graph(
            id="meu_grafico",
            config= {"displayModeBar": False}, 
        ),
    ]
)

@app.callback( 
   Output("meu_grafico", "figure"),
   [
        Input("interval", "n_intervals"),
   ]
)
def my_callback(n_intervals):
    get_position()
    figure= px.scatter_mapbox(df_geoloc, lat="Latitude", lon="Longitude",
            hover_name="Nome", hover_data=["Altitude",], 
            color_discrete_sequence=["fuchsia"],
            zoom=1, height=570)
    figure.update_layout(mapbox_style="carto-positron")
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
