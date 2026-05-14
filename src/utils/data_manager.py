import pandas as pd
import os

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "acidentes_final.csv")
    print("Carregando dados... Isso pode levar alguns segundos.")
    try:
        df = pd.read_csv(data_path, sep=";", low_memory=False)
        print(f"✅ Dados carregados: {len(df):,} registros.")

        if 'hora' in df.columns:
            df['hora_int'] = pd.to_numeric(df['hora'], errors='coerce')

        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

def get_filter_options(df):
    ufs = sorted(df['uf'].dropna().unique()) if not df.empty and 'uf' in df.columns else []
    climas = sorted(df['condicao_metereologica'].dropna().unique()) if not df.empty and 'condicao_metereologica' in df.columns else []
    return ufs, climas
