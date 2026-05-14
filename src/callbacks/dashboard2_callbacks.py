from dash import Input, Output
import plotly.express as px

def register_dashboard2_callbacks(app, df):
    @app.callback(
        [Output('grafico-hora', 'figure'),
         Output('grafico-gravidade', 'figure'),
         Output('grafico-dispersao-pop', 'figure'),
         Output('grafico-dia-semana', 'figure')],
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
            vazio = px.scatter(title="Nenhum dado encontrado para este filtro", template="plotly_white")
            return vazio, vazio, vazio, vazio

        template = "plotly_white"

        coluna_x = 'hora_int' if 'hora_int' in dff.columns else 'periodo_dia'
        fig_hora = px.histogram(
            dff,
            x=coluna_x,
            title="Acidentes por Hora do Dia",
            color_discrete_sequence=['#3498db'],
            template=template,
            nbins=24
        )

        fig_hora.update_traces(
            marker=dict(line=dict(width=1.5, color='white')),
            hovertemplate="<b>Hora:</b> %{x}h<br><b>Acidentes:</b> %{y}<extra></extra>"
        )
        fig_hora.update_layout(xaxis_title="Hora do Dia", yaxis_title="Total de Acidentes", bargap=0.05)

        top_tipos = dff['tipo_acidente'].value_counts().nlargest(10).index
        dff_tipos = dff[dff['tipo_acidente'].isin(top_tipos)]

        fig_gravidade = px.histogram(
            dff_tipos,
            y="tipo_acidente",
            color="gravidade",
            title="Gravidade por Tipo de Acidente (Top 10)",
            orientation='h',
            barmode='stack',
            template=template,
            labels={"tipo_acidente": "Tipo", "gravidade": "Gravidade"},
            color_discrete_map={
                "Fatal": "#e74c3c",
                "Grave": "#f39c12",
                "Leve": "#f1c40f",
                "Sem vítimas": "#3498db"
            }
        )

        fig_gravidade.update_traces(hovertemplate="<b>%{y}</b><br>Acidentes: %{x}<extra></extra>")
        fig_gravidade.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title="", xaxis_title="Total de Acidentes")

        if 'populacao' in dff.columns:

            dff_uf = dff.groupby('uf').agg(
                populacao=('populacao', 'first'),
                total_acidentes=('uf', 'size')
            ).reset_index()

            fig_dispersao = px.scatter(
                dff_uf,
                x='populacao',
                y='total_acidentes',
                text='uf',
                title="População vs Volume Absoluto de Acidentes",
                template=template,
                labels={"populacao": "População", "total_acidentes": "Total de Acidentes"},
                color_discrete_sequence=['#e83e8c']
            )
            fig_dispersao.update_traces(
                textposition='top center',
                marker=dict(size=14, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')),
                hovertemplate="<b>Estado: %{text}</b><br>População: %{x}<br>Acidentes: %{y}<extra></extra>"
            )
        else:
            fig_dispersao = px.scatter(title="Dados de população não disponíveis", template=template)

        if 'fim_de_semana' in dff.columns:
            dff_fds = dff['fim_de_semana'].value_counts().reset_index()
            dff_fds.columns = ['is_fim_de_semana', 'total']
            dff_fds['Tipo de Dia'] = dff_fds['is_fim_de_semana'].map({True: 'Fim de Semana (Sáb/Dom)', False: 'Dia Útil (Seg-Sex)'})

            fig_dia_semana = px.pie(
                dff_fds,
                names='Tipo de Dia',
                values='total',
                title="Proporção: Dia Útil vs Fim de Semana",
                template=template,
                color='Tipo de Dia',
                color_discrete_map={'Fim de Semana (Sáb/Dom)': '#e74c3c', 'Dia Útil (Seg-Sex)': '#3498db'},
                hole=0.4
            )
            fig_dia_semana.update_traces(
                hovertemplate="<b>%{label}</b><br>Acidentes: %{value}<br>Proporção: %{percent}<extra></extra>"
            )
        else:
            fig_dia_semana = px.bar(title="Dados de dia da semana não disponíveis", template=template)

        return fig_hora, fig_gravidade, fig_dispersao, fig_dia_semana
