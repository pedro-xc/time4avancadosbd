import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from src.layouts.dashboard1 import create_dashboard1_layout
from src.utils.data_manager import load_data, get_filter_options
from src.layouts.dashboard2 import create_dashboard2_layout
from src.callbacks.dashboard1_callbacks import register_dashboard1_callbacks
from src.callbacks.dashboard2_callbacks import register_dashboard2_callbacks

# -- Carregar Dados ---------------------------------------------------------
df = load_data()
ufs_disponiveis, climas_disponiveis = get_filter_options(df)

# -- App Dash ---------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="PRF 2024 - Painel de Acidentes",
    update_title="Carregando...",
)
server = app.server

# -- Sidebar ----------------------------------------------------------------
sidebar = html.Nav([
    # Logo
    html.Div([
        html.Div("PR", className="logo-icon"),
        html.Div([
            html.Div("PRF 2024", className="logo-text"),
            html.Div("Rodovias Federais", className="logo-sub"),
        ]),
    ], className="sidebar-logo"),

    # Menu principal
    html.Div("MENU", className="sidebar-section-label"),
    html.Ul([
        html.Li(
            dcc.Link([
                html.Span("Visão Geral"),
            ], href="/", className="sidebar-nav-link", id="nav-dashboard"),
            className="sidebar-nav-item"
        ),
        html.Li(
            dcc.Link([
                html.Span("Exploração"),
            ], href="/exploracao", className="sidebar-nav-link", id="nav-exploracao"),
            className="sidebar-nav-item"
        ),
    ], className="sidebar-nav"),

    # Secao dados
    html.Div("DADOS", className="sidebar-section-label"),
    html.Ul([
        html.Li(
            dcc.Link([
                html.Span("Visualizar Dados"),
            ], href="/dados", className="sidebar-nav-link", id="nav-dados"),
            className="sidebar-nav-item"
        ),
    ], className="sidebar-nav"),

    # Footer
    html.Div([
        html.Div([
            html.P("PUCC - Banco de Dados"),
            html.Div("Time 4", className="team-name"),
        ], className="sidebar-footer-card"),
    ], className="sidebar-footer"),

], className="sidebar")


# -- Header -----------------------------------------------------------------
header = html.Header([
    html.Div([
        html.Span("Q", className="header-search-icon"),
        dcc.Input(placeholder="Buscar informacoes...", type="text", style={
            'border': 'none', 'background': 'transparent', 'fontFamily': 'Inter, sans-serif',
            'fontSize': '13px', 'color': '#1A1A1A', 'outline': 'none', 'width': '100%',
        }),
    ], className="header-search"),

    html.Div([
        html.Div([
            html.Div("T4", className="header-team-avatar"),
            html.Div([
                html.Span("Time 4", className="header-team-name"),
                html.Span("Estudos Avancados BD", className="header-team-role"),
            ], className="header-team-info"),
        ], className="header-team"),
    ], className="header-right"),
], className="header-bar")


# -- Dashboard 1 Placeholder ------------------------------------------------
dashboard1_page = html.Div([
html.Div([
    html.Div([
        html.H1("Visão Geral", className="page-title"),
        html.P("Visão geral dos acidentes nas rodovias federais em 2024.", className="page-subtitle"),
    ]),
], className="page-header"),

create_dashboard1_layout()
], id="page-dashboard1")


# -- Dashboard 2 Page -------------------------------------------------------
dashboard2_page = html.Div([
    html.Div([
        html.Div([
            html.H1("Exploração Interativa", className="page-title"),
            html.P("Filtre e cruze variaveis para descobrir padroes ocultos nos acidentes.", className="page-subtitle"),
        ]),
    ], className="page-header"),

    create_dashboard2_layout(ufs_disponiveis, climas_disponiveis),
], id="page-dashboard2")


# -- Dados Page -------------------------------------------------------------
cols_preferidas = ['id', 'data_inversa', 'dia_semana', 'horario', 'uf', 'municipio', 'causa_acidente', 'tipo_acidente', 'classificacao_acidente', 'mortos', 'feridos']
cols = [c for c in cols_preferidas if c in df.columns]
if not cols:
    cols = list(df.columns[:8])

header_html = html.Thead(
    html.Tr([html.Th(c.replace('_', ' ').upper()) for c in cols])
)
rows_html = []
for _, row in df.head(20).iterrows():
    rows_html.append(html.Tr([
        html.Td(str(row[c])) for c in cols
    ]))
body_html = html.Tbody(rows_html)
tabela_estatica = html.Table([header_html, body_html], className="premium-table")

dados_page = html.Div([
    html.Div([
        html.Div([
            html.H1("Visualização dos Dados", className="page-title"),
            html.P("Amostra encurtada com as primeiras 20 linhas do conjunto de dados de acidentes da PRF 2024.", className="page-subtitle"),
        ]),
    ], className="page-header"),

    html.Div([
        html.Div([
            html.Div("Registros do Banco de Dados", className="chart-card-title"),
            html.Div("Exibindo as primeiras 20 linhas do dataset principal", className="chart-card-subtitle"),
            html.Div(tabela_estatica, className="table-container", style={'marginTop': '16px'}),
        ], className="chart-card")
    ], className="chart-grid chart-grid--1col")
], id="page-dados")


# -- Layout Principal -------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div([
        header,
        html.Div([
            dashboard1_page,
            dashboard2_page,
            dados_page,
        ], className="content-area"),
    ], className="main-content"),
], className="app-container")


# -- Callback de Navegacao --------------------------------------------------
@app.callback(
    [Output('page-dashboard1', 'style'),
     Output('page-dashboard2', 'style'),
     Output('page-dados', 'style'),
     Output('nav-dashboard', 'className'),
     Output('nav-exploracao', 'className'),
     Output('nav-dados', 'className')],
    [Input('url', 'pathname')]
)
def render_page(pathname):
    base_class = "sidebar-nav-link"
    active_class = "sidebar-nav-link active"
    show = {'display': 'block'}
    hide = {'display': 'none'}

    if pathname == '/exploracao':
        return hide, show, hide, base_class, active_class, base_class
    elif pathname == '/dados':
        return hide, hide, show, base_class, base_class, active_class

    # Default: Dashboard 1
    return show, hide, hide, active_class, base_class, base_class


# -- Registrar Callbacks ----------------------------------------------------
register_dashboard1_callbacks()
register_dashboard2_callbacks(app, df)

# -- Executar ---------------------------------------------------------------
if __name__ == '__main__':
    print("Iniciando o servidor Dash... Acesse http://127.0.0.1:8050 no navegador.")
    app.run(debug=True, port=8050)
