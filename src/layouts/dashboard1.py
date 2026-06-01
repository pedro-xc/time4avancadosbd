import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
import numpy as np
from datetime import datetime

def _load_data():
    try:
        acidentes = pd.read_csv('acidentes2024.csv', sep=None, engine='python')
        print("SUCESSO: acidentes2024.csv carregado")
    except FileNotFoundError:
        print("ERRO: acidentes2024.csv não encontrado, usando dados de exemplo")
        acidentes = pd.DataFrame({
            'uf': np.random.choice(['SP', 'MG', 'RJ', 'RS', 'PR', 'BA', 'SC', 'GO'], 500),
            'causa_acidente': np.random.choice(['Velocidade', 'Embriaguez', 'Desatenção', 'Chuva', 'Animal', 'Sinalização', 'Mecânica'], 500),
            'data_inversa': pd.date_range('2024-01-01', '2024-12-31', periods=500).strftime('%Y-%m-%d'),
            'mortos': np.random.randint(0, 5, 500),
            'feridos_leves': np.random.randint(0, 10, 500),
            'feridos_graves': np.random.randint(0, 5, 500)
        })
    try:
        datatran = pd.read_csv('datatran2024.csv', sep=None, engine='python')
        print("SUCESSO: datatran2024.csv carregado")
    except FileNotFoundError:
        print("ERRO: datatran2024.csv não encontrado, usando dados de exemplo")
        datatran = pd.DataFrame({
            'uf': np.random.choice(['SP', 'MG', 'RJ', 'RS', 'PR', 'BA', 'SC', 'GO'], 500),
            'data_inversa': pd.date_range('2024-01-01', '2024-12-31', periods=500).strftime('%Y-%m-%d'),
            'tipo_acidente': np.random.choice(['Colisão', 'Capotamento', 'Atropelamento', 'Queda'], 500),
            'latitude': np.random.uniform(-30, -15, 500),
            'longitude': np.random.uniform(-55, -40, 500)
        })
    return acidentes, datatran

def _process_data(acidentes, datatran):
    required_acidentes = ['uf', 'causa_acidente', 'data_inversa']
    required_datatran = ['uf', 'data_inversa']
    uf_data = None
    if all(col in acidentes.columns for col in ['uf']):
        uf_data = acidentes['uf'].value_counts().reset_index()
        uf_data.columns = ['uf', 'acidentes']
    elif all(col in datatran.columns for col in ['uf']):
        uf_data = datatran['uf'].value_counts().reset_index()
        uf_data.columns = ['uf', 'acidentes']
    else:
        print("ERRO: Nenhuma coluna 'uf' encontrada")
        uf_data = pd.DataFrame({'uf': [], 'acidentes': []})
    uf_data = uf_data.sort_values('acidentes', ascending=False)
    
    time_data = None
    if all(col in acidentes.columns for col in ['data_inversa']):
        try:
            acidentes['data_inversa'] = pd.to_datetime(acidentes['data_inversa'])
            time_data = acidentes['data_inversa'].dt.month.value_counts().reset_index().sort_values('data_inversa')
            time_data.columns = ['mes', 'acidentes']
            mes_map = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',5:'Mai',6:'Jun',7:'Jul',8:'Ago',9:'Set',10:'Out',11:'Nov',12:'Dez'}
            time_data['mes_nome'] = time_data['mes'].map(mes_map)
        except:
            print("ERRO: Falha ao processar data_inversa para time_data")
    if time_data is None:
        time_data = pd.DataFrame({'mes': range(1,13), 'acidentes': [0]*12, 'mes_nome': ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']})
    
    cause_data = None
    if 'causa_acidente' in acidentes.columns:
        cause_data = acidentes['causa_acidente'].value_counts().head(6).reset_index()
        cause_data.columns = ['causa', 'acidentes']
    else:
        print("ERRO: coluna 'causa_acidente' não encontrada")
        cause_data = pd.DataFrame({'causa': [], 'acidentes': []})
    
    return uf_data, time_data, cause_data

def _calculate_kpis(acidentes):
    total = int(acidentes.shape[0])
    uf_mean = total / acidentes['uf'].nunique() if 'uf' in acidentes.columns and acidentes['uf'].nunique() > 0 else 0
    most_frequent_cause = acidentes['causa_acidente'].mode().iloc[0] if 'causa_acidente' in acidentes.columns and not acidentes.empty else 'N/A'
    return total, round(uf_mean, 1), most_frequent_cause

def _create_figures(uf_data, time_data, cause_data):
  
    fig1 = px.bar(uf_data, x='uf', y='acidentes', 
                  title='Acidentes por UF (2024)',
                  color='uf', color_discrete_sequence=px.colors.qualitative.Set3,
                  labels={'uf': 'UF', 'acidentes': 'Total de Acidentes'})
    fig1.update_layout(showlegend=False, xaxis={'categoryorder':'total descending'})
    
    fig2 = px.line(time_data, x='mes_nome', y='acidentes', 
                   title='Acidentes por Mês (2024)',
                   markers=True,
                   labels={'mes_nome': 'Mês', 'acidentes': 'Acidentes'})
    fig2.update_traces(line_color='#ff7f0e', marker=dict(size=8))
   
    fig2.update_xaxes(categoryorder='array', categoryarray=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'])

    fig3 = px.bar(cause_data, x='causa', y='acidentes',
                  title='Causas Mais Frequentes (Top 6)',
                  color='causa', color_discrete_sequence=px.colors.qualitative.Pastel2,
                  labels={'causa': 'Causa', 'acidentes': 'Acidentes'})
    fig3.update_layout(showlegend=False, xaxis={'categoryorder':'total descending'})
    
    return fig1, fig2, fig3

def create_dashboard1_layout():
    """Return Bootstrap layout for dashboard 1."""
    acidentes, datatran = _load_data()
    uf_data, time_data, cause_data = _process_data(acidentes, datatran)
    total_acidentes, media_estado, causa_top = _calculate_kpis(acidentes)
    fig1, fig2, fig3 = _create_figures(uf_data, time_data, cause_data)
    
    kpi_card = dbc.Card([
        dbc.CardBody([
            html.H5("KPIs", className="card-title"),
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Total de Acidentes", className="kpi-label"),
                        html.H3(f"{total_acidentes:,}", className="kpi-value text-primary")
                    ]), width=4),
                    dbc.Col(html.Div([
                        html.H6("Média por Estado", className="kpi-label"),
                        html.H3(f"{media_estado:.1f}", className="kpi-value text-success")
                    ]), width=4),
                    dbc.Col(html.Div([
                        html.H6("Causa Mais Frequente", className="kpi-label"),
                        html.H3(causa_top, className="kpi-value text-warning")
                    ]), width=4)
                ], className="text-center")
            ])
        ])
    ], className="mb-4 shadow-sm")
    
    graph_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                dcc.Graph(figure=fig1, config={'displayModeBar': False})
            ])
        ], className="mb-4 shadow-sm"), width=12, lg=6),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                dcc.Graph(figure=fig2, config={'displayModeBar': False})
            ])
        ], className="mb-4 shadow-sm"), width=12, lg=6),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                dcc.Graph(figure=fig3, config={'displayModeBar': False})
            ])
        ], className="mb-4 shadow-sm"), width=12, lg=6)
    ], className="g-4")
    
    layout = dbc.Container([
        html.H1("Dashboard Nacional de Acidentes 2024", className="mb-4 text-center"),
        kpi_card,
        graph_cards
    ], fluid=True)
    
    return layout