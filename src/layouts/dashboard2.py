from dash import dcc, html
import dash_bootstrap_components as dbc

def create_dashboard2_layout(ufs_disponiveis, climas_disponiveis):
    return html.Div([

        html.Div([
            html.H3("Exploração Interativa", className="text-primary fw-bold mb-1"),
            html.P("Filtre e cruze variáveis para descobrir padrões ocultos nos acidentes da PRF.", className="text-muted mb-4"),
        ], className="mb-4"),

        dbc.Card([
            dbc.CardBody([
                html.H5("Filtros de Análise", className="card-title mb-3 fw-bold"),
                dbc.Row([
                    dbc.Col([
                        html.Label("ESTADO (UF)", className="fw-bold text-secondary text-uppercase small mb-1"),
                        dcc.Dropdown(
                            id='filtro-uf',
                            options=[{'label': uf, 'value': uf} for uf in ufs_disponiveis],
                            value=[],
                            multi=True,
                            placeholder="Selecione um ou mais estados...",
                            className="text-dark shadow-sm"
                        )
                    ], md=6, className="mb-3 mb-md-0"),

                    dbc.Col([
                        html.Label("CONDIÇÃO METEOROLÓGICA", className="fw-bold text-secondary text-uppercase small mb-1"),
                        dcc.Dropdown(
                            id='filtro-clima',
                            options=[{'label': c, 'value': c} for c in climas_disponiveis],
                            value=[],
                            multi=True,
                            placeholder="Selecione o clima...",
                            className="text-dark shadow-sm"
                        )
                    ], md=6),
                ]),
            ])
        ], className="mb-5 shadow-sm border-0 rounded-4 bg-light"),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-hora', config={'displayModeBar': False})
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                ),
                md=6
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-gravidade', config={'displayModeBar': False})
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                ),
                md=6
            ),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-dispersao-pop', config={'displayModeBar': False})
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                ),
                md=6
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-dia-semana', config={'displayModeBar': False})
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                ),
                md=6
            ),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-radar-via', config={'displayModeBar': False})
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                ),
                md=8, className="mx-auto"
            ),
        ])
    ], className="py-3 fade-in")
