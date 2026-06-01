import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
from datetime import datetime, timedelta
from src.utils.data_manager import load_data

df_master = load_data()
def register_dashboard1_callbacks():
    @callback(
        Output('grafico-temporal', 'figure'),
        Input('dropdown-estado', 'value')
    )
    def update_temporal_chart(estado):
        df = df_master.copy()
        if estado and estado != 'Todos':
            df = df[df['estado'] == estado]
        df['data'] = pd.to_datetime(df['data'])
        date_range = pd.date_range(start=df['data'].min(), end=df['data'].max(), freq='D')
        daily = df.groupby(df['data'].dt.date).size().reset_index(name='acidentes')
        daily['data'] = pd.to_datetime(daily['data'])
        daily = daily.set_index('data').reindex(date_range, fill_value=0).reset_index()
        daily.columns = ['data', 'acidentes']
        max_y = daily['acidentes'].max() * 1.1 if daily['acidentes'].max() > 0 else 1
        fig = px.bar(daily, x='data', y='acidentes', title='Acidentes por Data')
        fig.update_yaxes(range=[0, max_y])
        return fig

    @callback(
        Output('kpi-total-acidentes', 'children'),
        Output('kpi-acidentes-com-vitimas', 'children'),
        Output('kpi-vitimas-fatais', 'children'),
        Input('dropdown-estado', 'value')
    )
    def update_kpis(estado):
        df = df_master.copy()
        if estado and estado != 'Todos':
            df = df[df['estado'] == estado]
        total = len(df)
        com_vitimas = df['com_vitimas'].sum() if 'com_vitimas' in df else 0
        vitimas_fatais = df['vitimas_fatais'].sum() if 'vitimas_fatais' in df else 0
        return total, com_vitimas, vitimas_fatais