import os
import pandas as pd
import numpy as np

# Configurações

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

ENTRADA = os.path.join(PROCESSED_DIR, "acidentes_merged.csv")
SAIDA   = os.path.join(PROCESSED_DIR, "acidentes_limpos.csv")

# Colunas numéricas que representam contagens de vítimas
COLUNAS_VITIMAS = ["mortos", "feridos_leves", "feridos_graves", "ilesos", "feridos", "veiculos"]

# Colunas categóricas para padronizar as strings e tratar nulos
COLUNAS_CATEGORICAS = [
    "uf", "dia_semana", "causa_acidente", "tipo_acidente",
    "classificacao_acidente", "fase_dia", "sentido_via",
    "condicao_metereologica", "tipo_pista", "tracado_via",
]

# Funções

def carregar(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, low_memory=False, sep=";", encoding="utf-8-sig")
    print(f"[LER]  {len(df):,} registros carregados")
    return df


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.drop_duplicates()
    depois = len(df)
    print(f"[DUPL] Removidas {antes - depois:,} linhas duplicadas")
    return df


def relatorio_nulos(df: pd.DataFrame) -> None:
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0].sort_values(ascending=False)
    if nulos.empty:
        print("[NULO] Nenhum valor nulo encontrado.")
        return
    print("[NULO] Colunas com valores ausentes:")
    for col, qtd in nulos.items():
        pct = qtd / len(df) * 100
        print(f"       {col:<40} {qtd:>7,}  ({pct:.1f}%)")


def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    # Colunas de vítimas: nulo vira 0
    for col in COLUNAS_VITIMAS:
        if col in df.columns:
            nulos = df[col].isnull().sum()
            df[col] = df[col].fillna(0)
            if nulos > 0:
                print(f"[NULO] {col}: {nulos:,} nulos → 0")

    # Colunas categóricas: nulo vira "Não informado"
    for col in COLUNAS_CATEGORICAS:
        if col in df.columns:
            nulos = df[col].isnull().sum()
            df[col] = df[col].fillna("Não informado")
            if nulos > 0:
                print(f"[NULO] {col}: {nulos:,} nulos → 'Não informado'")

    for col in ["municipio", "br"]:
        if col in df.columns:
            df[col] = df[col].fillna("Não informado")

    return df


def converter_datas(df: pd.DataFrame) -> pd.DataFrame:
    if "data_inversa" in df.columns:
        df["data_inversa"] = pd.to_datetime(df["data_inversa"], errors="coerce")
        nulos = df["data_inversa"].isnull().sum()
        print(f"[DATA] data_inversa convertida. Datas inválidas: {nulos:,}")

    if "horario" in df.columns:
        df["hora"] = pd.to_datetime(df["horario"], format="%H:%M:%S", errors="coerce").dt.hour
        print(f"[DATA] Coluna 'hora' criada a partir de 'horario'")

    return df


def converter_numericos(df: pd.DataFrame) -> pd.DataFrame:
    for col in COLUNAS_VITIMAS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    if "km" in df.columns:
        df["km"] = df["km"].astype(str).str.replace(",", ".").pipe(pd.to_numeric, errors="coerce")

    return df


def padronizar_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in COLUNAS_CATEGORICAS:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.upper()
            )

    # UF deve ter sempre 2 caracteres maiúsculos
    if "uf" in df.columns:
        df = df[df["uf"].str.len() == 2]

    return df


def remover_inconsistencias(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)

    # Remove registros sem data válida
    if "data_inversa" in df.columns:
        df = df[df["data_inversa"].notna()]

    # Remove registros com total de vítimas negativo
    for col in COLUNAS_VITIMAS:
        if col in df.columns:
            df = df[df[col] >= 0]

    # Remove registros fora do período esperado (2024)
    if "data_inversa" in df.columns:
        df = df[df["data_inversa"].dt.year == 2024]

    depois = len(df)
    print(f"[INCO] Removidos {antes - depois:,} registros inconsistentes")
    return df


def main():
    print("ETAPA 3 — LIMPEZA E TRATAMENTO\n")

    df = carregar(ENTRADA)

    print("\nRelatório de nulos ANTES da limpeza")
    relatorio_nulos(df)

    print("\nRemovendo duplicatas")
    df = remover_duplicatas(df)

    print("\nConvertendo datas")
    df = converter_datas(df)

    print("\nConvertendo numéricos")
    df = converter_numericos(df)

    print("\nPadronizando strings")
    df = padronizar_strings(df)

    print("\nTratando valores ausentes")
    df = tratar_nulos(df)

    print("\nRemovendo inconsistências")
    df = remover_inconsistencias(df)

    print("\nRelatório de nulos APÓS limpeza")
    relatorio_nulos(df)

    print(f"\nDataset final: {len(df):,} registros, {df.shape[1]} colunas")

    df.to_csv(SAIDA, index=False, encoding="utf-8-sig", sep=";")
    print(f"\n[OK] acidentes_limpos.csv salvo em data/processed/")
    print("[CONCLUÍDO]")


if __name__ == "__main__":
    main()