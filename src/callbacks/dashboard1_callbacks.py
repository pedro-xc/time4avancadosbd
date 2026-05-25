from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_manager import get_monthly_data, get_periodo_dia_data, get_weekly_trend


# ── Plotly Layout Base ─────────────────────────────────────────
PLOT_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color="#1A1A1A"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=8, b=16),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E5E7EB",
        font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#1A1A1A"
        )
    ),
    showlegend=False,
)

# Paleta verde
GREENS = ['#1B5E20', '#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9']
PERIODO_COLORS = {
    'Madrugada (0-5h)': '#1A237E',
    'Manhã (6-11h)': '#F59E0B',
    'Tarde (12-17h)': '#E65100',
    'Noite (18-23h)': '#1B5E20',
}


def register_dashboard1_callbacks(app, df):
    """Registra os callbacks para os gráficos do Dashboard 1."""

    @app.callback(
        [Output('grafico-mensal-d1', 'figure'),
         Output('grafico-periodo-d1', 'figure'),
         Output('grafico-semanal-d1', 'figure')],
        [Input('url', 'pathname')]
    )
    def render_dashboard1_charts(_pathname):
        # ── Gráfico de Barras: Acidentes por Mês ──────────────
        mensal = get_monthly_data(df)

        if not mensal.empty:
            fig_mensal = go.Figure()
            fig_mensal.add_trace(go.Bar(
                x=mensal['mes_nome'],
                y=mensal['total'],
                marker=dict(
                    color=mensal['total'],
                    colorscale=[[0, '#C8E6C9'], [0.5, '#4CAF50'], [1, '#1B5E20']],
                    cornerradius=6,
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{x}</b><br>Acidentes: %{y:,.0f}<extra></extra>",
            ))
            fig_mensal.update_layout(
                **PLOT_LAYOUT,
                height=320,
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=11, color="#6B7280"),
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.04)",
                    gridwidth=1,
                    tickfont=dict(size=11, color="#6B7280"),
                    tickformat=",",
                ),
                bargap=0.3,
            )
        else:
            fig_mensal = go.Figure()
            fig_mensal.update_layout(**PLOT_LAYOUT, height=320)

        # ── Gráfico de Rosca: Período do Dia ──────────────────
        periodo = get_periodo_dia_data(df)

        if not periodo.empty:
            cores = [PERIODO_COLORS.get(p, '#4CAF50') for p in periodo['periodo_dia']]

            fig_periodo = go.Figure()
            fig_periodo.add_trace(go.Pie(
                labels=periodo['periodo_dia'],
                values=periodo['total'],
                hole=0.55,
                marker=dict(colors=cores, line=dict(color='white', width=3)),
                textinfo='percent',
                textfont=dict(size=12, color="white", family="Inter, sans-serif"),
                hovertemplate="<b>%{label}</b><br>Acidentes: %{value:,.0f}<br>%{percent}<extra></extra>",
                direction='clockwise',
                sort=False,
            ))
            fig_periodo.update_layout(
                **PLOT_LAYOUT,
                height=320,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11, color="#6B7280"),
                ),
                showlegend=True,
            )
        else:
            fig_periodo = go.Figure()
            fig_periodo.update_layout(**PLOT_LAYOUT, height=320)

        # ── Gráfico de Linha: Tendência Semanal ───────────────
        semanal = get_weekly_trend(df)

        if not semanal.empty:
            fig_semanal = go.Figure()
            fig_semanal.add_trace(go.Scatter(
                x=semanal['semana_do_ano'],
                y=semanal['total'],
                mode='lines',
                line=dict(color='#2E7D32', width=2.5, shape='spline', smoothing=1.3),
                fill='tozeroy',
                fillcolor='rgba(76,175,80,0.08)',
                hovertemplate="<b>Semana %{x}</b><br>Acidentes: %{y:,.0f}<extra></extra>",
            ))
            # Adicionar linha de média
            media = semanal['total'].mean()
            fig_semanal.add_hline(
                y=media,
                line_dash="dot",
                line_color="#9CA3AF",
                line_width=1.5,
                annotation_text=f"Média: {media:,.0f}",
                annotation_position="top right",
                annotation_font=dict(size=10, color="#9CA3AF"),
            )
            fig_semanal.update_layout(
                **PLOT_LAYOUT,
                height=320,
                xaxis=dict(
                    title="Semana do Ano",
                    showgrid=False,
                    tickfont=dict(size=11, color="#6B7280"),
                    title_font=dict(size=11, color="#9CA3AF"),
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.04)",
                    gridwidth=1,
                    tickfont=dict(size=11, color="#6B7280"),
                    tickformat=",",
                ),
            )
        else:
            fig_semanal = go.Figure()
            fig_semanal.update_layout(**PLOT_LAYOUT, height=320)

        return fig_mensal, fig_periodo, fig_semanal
