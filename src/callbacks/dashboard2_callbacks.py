from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go


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
)

# ── Paletas ────────────────────────────────────────────────────
GREEN_SCALE = ['#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20']

GRAVIDADE_COLORS = {
    "Fatal": "#DC2626",
    "Grave": "#F59E0B",
    "Leve": "#3B82F6",
    "Sem vítimas": "#4CAF50",
}


def register_dashboard2_callbacks(app, df):
    @app.callback(
        [Output('grafico-hora', 'figure'),
         Output('grafico-gravidade', 'figure'),
         Output('grafico-dispersao-pop', 'figure'),
         Output('grafico-dia-semana', 'figure'),
         Output('grafico-radar-via', 'figure')],
        [Input('filtro-uf', 'value'),
         Input('filtro-clima', 'value')]
    )
    def atualizar_graficos(ufs_selecionadas, climas_selecionados):

        dff = df.copy()
        if ufs_selecionadas:
            dff = dff[dff['uf'].isin(ufs_selecionadas)]
        if climas_selecionados:
            dff = dff[dff['condicao_metereologica'].isin(climas_selecionados)]

        if dff.empty:
            vazio = go.Figure()
            vazio.add_annotation(
                text="Nenhum dado encontrado para este filtro",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="#9CA3AF", family="Inter, sans-serif")
            )
            vazio.update_layout(**PLOT_LAYOUT, height=350)
            return vazio, vazio, vazio, vazio, vazio

        # ── 1. Acidentes por Hora ─────────────────────────────
        coluna_x = 'hora_int' if 'hora_int' in dff.columns else 'periodo_dia'

        if coluna_x == 'hora_int':
            hora_counts = dff.groupby('hora_int').size().reset_index(name='total')
            fig_hora = go.Figure()
            fig_hora.add_trace(go.Bar(
                x=hora_counts['hora_int'],
                y=hora_counts['total'],
                marker=dict(
                    color=hora_counts['total'],
                    colorscale=[[0, '#C8E6C9'], [0.5, '#4CAF50'], [1, '#1B5E20']],
                    cornerradius=4,
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{x}h</b><br>Acidentes: %{y:,.0f}<extra></extra>",
            ))
        else:
            hora_counts = dff[coluna_x].value_counts().reset_index()
            hora_counts.columns = [coluna_x, 'total']
            fig_hora = go.Figure()
            fig_hora.add_trace(go.Bar(
                x=hora_counts[coluna_x],
                y=hora_counts['total'],
                marker=dict(color='#2E7D32', cornerradius=4),
                hovertemplate="<b>%{x}</b><br>Acidentes: %{y:,.0f}<extra></extra>",
            ))

        fig_hora.update_layout(
            **PLOT_LAYOUT,
            height=350,
            xaxis=dict(title="Hora do Dia", showgrid=False, tickfont=dict(size=10, color="#6B7280"),
                        title_font=dict(size=11, color="#9CA3AF")),
            yaxis=dict(title="Total", showgrid=True, gridcolor="rgba(0,0,0,0.04)",
                        tickfont=dict(size=10, color="#6B7280"), title_font=dict(size=11, color="#9CA3AF"),
                        tickformat=","),
            bargap=0.15,
            showlegend=False,
        )

        # ── 2. Gravidade por Tipo ─────────────────────────────
        top_tipos = dff['tipo_acidente'].value_counts().nlargest(10).index
        dff_tipos = dff[dff['tipo_acidente'].isin(top_tipos)]

        fig_gravidade = px.histogram(
            dff_tipos,
            y="tipo_acidente",
            color="gravidade",
            orientation='h',
            barmode='stack',
            labels={"tipo_acidente": "", "gravidade": "Gravidade", "count": "Total"},
            color_discrete_map=GRAVIDADE_COLORS,
        )

        fig_gravidade.update_traces(
            hovertemplate="<b>%{y}</b><br>Acidentes: %{x:,.0f}<extra></extra>",
            marker_line_width=0,
        )
        fig_gravidade.update_layout(
            **PLOT_LAYOUT,
            height=350,
            yaxis={'categoryorder': 'total ascending'},
            xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)", tickfont=dict(size=10, color="#6B7280"),
                        tickformat=","),
            yaxis_tickfont=dict(size=10),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10, color="#6B7280"),
                bgcolor="rgba(0,0,0,0)",
            ),
            bargap=0.25,
        )

        # ── 3. Dispersão: População vs Acidentes ──────────────
        if 'populacao' in dff.columns:
            dff_uf = dff.groupby('uf').agg(
                populacao=('populacao', 'first'),
                total_acidentes=('uf', 'size')
            ).reset_index()

            fig_dispersao = go.Figure()
            fig_dispersao.add_trace(go.Scatter(
                x=dff_uf['populacao'],
                y=dff_uf['total_acidentes'],
                mode='markers+text',
                text=dff_uf['uf'],
                textposition='top center',
                textfont=dict(size=9, color="#6B7280"),
                marker=dict(
                    size=14,
                    color=dff_uf['total_acidentes'],
                    colorscale=[[0, '#C8E6C9'], [0.5, '#4CAF50'], [1, '#1B5E20']],
                    opacity=0.85,
                    line=dict(width=1.5, color='white'),
                ),
                hovertemplate="<b>%{text}</b><br>População: %{x:,.0f}<br>Acidentes: %{y:,.0f}<extra></extra>",
            ))
            fig_dispersao.update_layout(
                **PLOT_LAYOUT,
                height=350,
                xaxis=dict(title="População", showgrid=True, gridcolor="rgba(0,0,0,0.04)",
                            tickfont=dict(size=10, color="#6B7280"), title_font=dict(size=11, color="#9CA3AF"),
                            tickformat=","),
                yaxis=dict(title="Total de Acidentes", showgrid=True, gridcolor="rgba(0,0,0,0.04)",
                            tickfont=dict(size=10, color="#6B7280"), title_font=dict(size=11, color="#9CA3AF"),
                            tickformat=","),
                showlegend=False,
            )
        else:
            fig_dispersao = go.Figure()
            fig_dispersao.add_annotation(text="Dados de população não disponíveis",
                                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            fig_dispersao.update_layout(**PLOT_LAYOUT, height=350)

        # ── 4. Dia Útil vs Fim de Semana ──────────────────────
        if 'fim_de_semana' in dff.columns:
            dff_fds = dff['fim_de_semana'].value_counts().reset_index()
            dff_fds.columns = ['is_fim_de_semana', 'total']
            dff_fds['Tipo de Dia'] = dff_fds['is_fim_de_semana'].map({
                True: 'Fim de Semana',
                False: 'Dia Útil',
            })

            cores_dia = ['#1B5E20', '#81C784']

            fig_dia_semana = go.Figure()
            fig_dia_semana.add_trace(go.Pie(
                labels=dff_fds['Tipo de Dia'],
                values=dff_fds['total'],
                hole=0.55,
                marker=dict(colors=cores_dia, line=dict(color='white', width=3)),
                textinfo='percent+label',
                textfont=dict(size=11, color="white", family="Inter, sans-serif"),
                hovertemplate="<b>%{label}</b><br>Acidentes: %{value:,.0f}<br>%{percent}<extra></extra>",
            ))
            fig_dia_semana.update_layout(
                **PLOT_LAYOUT,
                height=350,
                showlegend=False,
            )
        else:
            fig_dia_semana = go.Figure()
            fig_dia_semana.update_layout(**PLOT_LAYOUT, height=350)

        # ── 5. Treemap: Mortalidade ───────────────────────────
        if 'tracado_via' in dff.columns and 'tipo_pista' in dff.columns and 'mortos' in dff.columns:
            dff_tree = dff.groupby(['tipo_pista', 'tracado_via'], as_index=False)['mortos'].sum()
            dff_tree = dff_tree[dff_tree['mortos'] > 0]
            dff_tree['Raiz'] = 'Vítimas Fatais'

            fig_treemap = px.treemap(
                dff_tree,
                path=['Raiz', 'tipo_pista', 'tracado_via'],
                values='mortos',
                color='mortos',
                color_continuous_scale=[
                    [0, '#E8F5E9'],
                    [0.3, '#81C784'],
                    [0.6, '#F59E0B'],
                    [0.8, '#EF4444'],
                    [1, '#991B1B'],
                ],
            )
            fig_treemap.update_traces(
                hovertemplate="<b>%{label}</b><br>Mortos: %{value:,.0f}<extra></extra>",
                textfont=dict(family="Inter, sans-serif"),
            )
            fig_treemap.update_layout(
                **PLOT_LAYOUT,
                height=500,
                coloraxis_showscale=False,
            )
            fig_treemap.update_layout(margin=dict(t=8, l=8, r=8, b=8))
        else:
            fig_treemap = go.Figure()
            fig_treemap.update_layout(**PLOT_LAYOUT, height=500)

        return fig_hora, fig_gravidade, fig_dispersao, fig_dia_semana, fig_treemap
