import dash
import dash_bootstrap_components as dbc
from dash import html

from src.utils.data_manager import load_data, get_filter_options
from src.layouts.dashboard1 import create_dashboard1_layout
from src.layouts.dashboard2 import create_dashboard2_layout
from src.callbacks.dashboard2_callbacks import register_dashboard2_callbacks

df = load_data()
ufs_disponiveis, climas_disponiveis = get_filter_options(df)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    html.Div([
        html.H1("Painel PRF 2024", className="display-4 text-center text-primary mt-4"),
        html.P("Análise Inteligente de Acidentes nas Rodovias Federais", className="lead text-center mb-4 text-secondary"),
    ]),

    dbc.Tabs([
        dbc.Tab(create_dashboard1_layout(), label="Dashboard 1 (Visão Geral)", tab_id="tab-1"),
        dbc.Tab(create_dashboard2_layout(ufs_disponiveis, climas_disponiveis), label="Dashboard 2 (Exploração)", tab_id="tab-2"),
    ], id="tabs", active_tab="tab-2")

], fluid=True, className="p-4", style={'backgroundColor': '#f4f6f9', 'minHeight': '100vh'})

register_dashboard2_callbacks(app, df)

if __name__ == '__main__':
    print("Iniciando o servidor Dash... Acesse http://127.0.0.1:8050 no navegador.")
    app.run(debug=True, port=8050)
