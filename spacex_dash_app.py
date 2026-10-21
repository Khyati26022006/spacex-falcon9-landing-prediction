"""Plotly Dash dashboard: SpaceX launch records.
Run:  python spacex_dash_app.py   then open http://127.0.0.1:8050
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("data/spacex_launch_dash.csv")
max_payload, min_payload = df["Payload Mass (kg)"].max(), df["Payload Mass (kg)"].min()
sites = sorted(df["Launch Site"].unique())

app = Dash(__name__)
app.layout = html.Div(
    style={"fontFamily": "Calibri, Arial", "padding": "20px"},
    children=[
        html.H1("SpaceX Launch Records Dashboard", style={"color": "#0B49CB"}),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in sites],
            value="ALL", placeholder="Select a launch site", searchable=True,
        ),
        dcc.Graph(id="success-pie-chart"),
        html.P("Payload range (kg):"),
        dcc.RangeSlider(
            id="payload-slider", min=0, max=10000, step=1000,
            marks={i: str(i) for i in range(0, 10001, 2500)},
            value=[min_payload, max_payload],
        ),
        dcc.Graph(id="success-payload-scatter-chart"),
    ],
)

@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_pie(site):
    if site == "ALL":
        return px.pie(df, values="class", names="Launch Site", title="Total successful launches by site")
    sub = df[df["Launch Site"] == site]["class"].value_counts().rename_axis("outcome").reset_index(name="count")
    sub["outcome"] = sub["outcome"].map({1: "Success", 0: "Failure"})
    return px.pie(sub, values="count", names="outcome", title=f"Success vs failure: {site}",
                  color="outcome", color_discrete_map={"Success": "#1E9E5A", "Failure": "#D64545"})

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_scatter(site, payload):
    lo, hi = payload
    sub = df[df["Payload Mass (kg)"].between(lo, hi)]
    if site != "ALL":
        sub = sub[sub["Launch Site"] == site]
    return px.scatter(sub, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title="Payload vs launch outcome")

if __name__ == "__main__":
    app.run(debug=False)
