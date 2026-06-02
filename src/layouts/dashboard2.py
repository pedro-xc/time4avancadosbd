from dash import dcc, html
import dash_bootstrap_components as dbc
from src.insights.narrativas import get_dashboard_paragraphs


def create_dashboard2_layout(ufs_disponiveis, climas_disponiveis):
    """Cria o layout do Dashboard 2 — Exploração Interativa com design premium."""

    # ── Card de Filtros ────────────────────────────────────────
    filtros = html.Div([
        html.Div([
            html.Span("Filtros de Analise"),
        ], className="filter-card-title"),

        html.Div([
            html.Div([
                html.Div([
                    html.Label("ESTADO (UF)", style={
                        'fontSize': '11px', 'fontWeight': '600', 'color': '#6B7280',
                        'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                        'marginBottom': '6px', 'display': 'block',
                    }),
                    dcc.Dropdown(
                        id='filtro-uf',
                        options=[{'label': uf, 'value': uf} for uf in ufs_disponiveis],
                        value=[],
                        multi=True,
                        placeholder="Selecione um ou mais estados...",
                    )
                ], style={'flex': '1', 'minWidth': '260px'}),

                html.Div([
                    html.Label("CONDIÇÃO METEOROLÓGICA", style={
                        'fontSize': '11px', 'fontWeight': '600', 'color': '#6B7280',
                        'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                        'marginBottom': '6px', 'display': 'block',
                    }),
                    dcc.Dropdown(
                        id='filtro-clima',
                        options=[{'label': c, 'value': c} for c in climas_disponiveis],
                        value=[],
                        multi=True,
                        placeholder="Selecione o clima...",
                    )
                ], style={'flex': '1', 'minWidth': '260px'}),
            ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),
        ]),
    ], className="filter-card")

    # ── Gráficos ───────────────────────────────────────────────
    paragraphs = get_dashboard_paragraphs()

    chart_hora = html.Div([
        html.Div("Acidentes por Hora", className="chart-card-title"),
        html.Div("Distribuição ao longo das 24 horas", className="chart-card-subtitle"),
        dcc.Graph(id='grafico-hora', config={'displayModeBar': False}),
        html.P(paragraphs["Gravidade por período do dia"], className="insight-text"),
    ], className="chart-card")

    chart_gravidade = html.Div([
        html.Div("Gravidade por Tipo", className="chart-card-title"),
        html.Div("Top 10 tipos de acidente por gravidade", className="chart-card-subtitle"),
        dcc.Graph(id='grafico-gravidade', config={'displayModeBar': False}),
        html.P(paragraphs["Gravidade por clima"], className="insight-text"),
    ], className="chart-card")

    chart_dispersao = html.Div([
        html.Div("População vs Acidentes", className="chart-card-title"),
        html.Div("Correlação entre população estadual e volume", className="chart-card-subtitle"),
        dcc.Graph(id='grafico-dispersao-pop', config={'displayModeBar': False}),
        html.P(paragraphs["Acidentes por UF"], className="insight-text"),
    ], className="chart-card")

    chart_dia = html.Div([
        html.Div("Dia Útil vs Fim de Semana", className="chart-card-title"),
        html.Div("Proporção por tipo de dia", className="chart-card-subtitle"),
        dcc.Graph(id='grafico-dia-semana', config={'displayModeBar': False}),
        html.P(paragraphs["Fim de semana"], className="insight-text"),
    ], className="chart-card")

    chart_treemap = html.Div([
        html.Div("Mortalidade: Pista × Traçado", className="chart-card-title"),
        html.Div("Vítimas fatais por tipo de pista e traçado da via", className="chart-card-subtitle"),
        dcc.Graph(id='grafico-radar-via', config={'displayModeBar': False}),
        html.P(paragraphs["Letalidade por tipo de pista"], className="insight-text"),
    ], className="chart-card")

    # ── Layout Final ───────────────────────────────────────────
    return html.Div([
        filtros,

        html.Div([chart_hora, chart_gravidade], className="chart-grid chart-grid--2col"),

        html.Div([chart_dispersao, chart_dia], className="chart-grid chart-grid--2col"),

        html.Div([chart_treemap], className="chart-grid chart-grid--1col"),

    ], className="animate-fade-in")
