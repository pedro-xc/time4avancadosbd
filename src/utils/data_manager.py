import pandas as pd
import os

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "acidentes_final.csv")
    print("Carregando dados... Isso pode levar alguns segundos.")
    try:
        df = pd.read_csv(data_path, sep=";", low_memory=False)
        print(f"[OK] Dados carregados: {len(df):,} registros.")

        if 'hora' in df.columns:
            df['hora_int'] = pd.to_numeric(df['hora'], errors='coerce')

        return df
    except Exception as e:
        print(f"[ERRO] Erro ao carregar dados: {e}")
        return pd.DataFrame()

def get_filter_options(df):
    ufs = sorted(df['uf'].dropna().unique()) if not df.empty and 'uf' in df.columns else []
    climas = sorted(df['condicao_metereologica'].dropna().unique()) if not df.empty and 'condicao_metereologica' in df.columns else []
    return ufs, climas


def get_kpi_data(df):
    """Calcula os indicadores-chave (KPIs) a partir do DataFrame."""
    if df.empty:
        return {
            'total_acidentes': 0,
            'total_fatais': 0,
            'total_graves': 0,
            'total_leves': 0,
            'total_mortos': 0,
            'total_feridos': 0,
            'total_ilesos': 0,
            'estados_afetados': 0,
        }

    # Contar acidentes únicos (cada 'id' é um acidente)
    total_acidentes = df['id'].nunique() if 'id' in df.columns else len(df)

    # Gravidade
    if 'gravidade' in df.columns:
        grav = df.drop_duplicates(subset='id') if 'id' in df.columns else df
        contagens = grav['gravidade'].value_counts()
        total_fatais = int(contagens.get('Fatal', 0))
        total_graves = int(contagens.get('Grave', 0))
        total_leves = int(contagens.get('Leve', 0))
    else:
        total_fatais = total_graves = total_leves = 0

    # Vítimas
    if 'id' in df.columns:
        acid_unico = df.drop_duplicates(subset='id')
        total_mortos = int(acid_unico['mortos'].sum()) if 'mortos' in df.columns else 0
        total_feridos = int(acid_unico['feridos'].sum()) if 'feridos' in df.columns else 0
        total_ilesos = int(acid_unico['ilesos'].sum()) if 'ilesos' in df.columns else 0
    else:
        total_mortos = int(df['mortos'].sum()) if 'mortos' in df.columns else 0
        total_feridos = int(df['feridos'].sum()) if 'feridos' in df.columns else 0
        total_ilesos = int(df['ilesos'].sum()) if 'ilesos' in df.columns else 0

    # Estados
    estados_afetados = df['uf'].nunique() if 'uf' in df.columns else 0

    return {
        'total_acidentes': total_acidentes,
        'total_fatais': total_fatais,
        'total_graves': total_graves,
        'total_leves': total_leves,
        'total_mortos': total_mortos,
        'total_feridos': total_feridos,
        'total_ilesos': total_ilesos,
        'estados_afetados': estados_afetados,
    }


def get_top_states(df, n=5):
    """Retorna os top N estados por número de acidentes."""
    if df.empty or 'uf' not in df.columns:
        return pd.DataFrame(columns=['uf', 'total'])

    if 'id' in df.columns:
        top = df.groupby('uf')['id'].nunique().reset_index()
        top.columns = ['uf', 'total']
    else:
        top = df['uf'].value_counts().reset_index()
        top.columns = ['uf', 'total']

    return top.sort_values('total', ascending=False).head(n)


def get_monthly_data(df):
    """Retorna acidentes agrupados por mês."""
    if df.empty or 'mes' not in df.columns:
        return pd.DataFrame(columns=['mes', 'mes_nome', 'total'])

    if 'id' in df.columns:
        mensal = df.groupby(['mes', 'mes_nome'])['id'].nunique().reset_index()
        mensal.columns = ['mes', 'mes_nome', 'total']
    else:
        mensal = df.groupby(['mes', 'mes_nome']).size().reset_index(name='total')

    return mensal.sort_values('mes')


def get_periodo_dia_data(df):
    """Retorna distribuição por período do dia."""
    if df.empty or 'periodo_dia' not in df.columns:
        return pd.DataFrame(columns=['periodo_dia', 'total'])

    if 'id' in df.columns:
        periodo = df.groupby('periodo_dia')['id'].nunique().reset_index()
        periodo.columns = ['periodo_dia', 'total']
    else:
        periodo = df['periodo_dia'].value_counts().reset_index()
        periodo.columns = ['periodo_dia', 'total']

    return periodo


def get_weekly_trend(df):
    """Retorna tendência semanal de acidentes."""
    if df.empty or 'semana_do_ano' not in df.columns:
        return pd.DataFrame(columns=['semana_do_ano', 'total'])

    if 'id' in df.columns:
        semanal = df.groupby('semana_do_ano')['id'].nunique().reset_index()
        semanal.columns = ['semana_do_ano', 'total']
    else:
        semanal = df.groupby('semana_do_ano').size().reset_index(name='total')

    return semanal.sort_values('semana_do_ano')
