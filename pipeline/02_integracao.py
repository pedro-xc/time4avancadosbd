import os
import pandas as pd

# Configurações

RAW_DIR       = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Funções

def ler_csv_prf(nome: str) -> pd.DataFrame:
    """Lê um CSV da PRF detectando o separador automaticamente."""
    caminho = os.path.join(RAW_DIR, nome)

    with open(caminho, encoding="latin1") as f:
        amostra = f.read(2048)
    sep = ";" if amostra.count(";") > amostra.count(",") else ","

    df = pd.read_csv(caminho, sep=sep, encoding="latin1", low_memory=False)
    print(f"[LER]  {nome}: {len(df):,} registros, {df.shape[1]} colunas (sep='{sep}')")
    return df


def ler_ibge() -> pd.DataFrame:
    """Lê o CSV do IBGE gerado pelo crawler."""
    caminho = os.path.join(RAW_DIR, "ibge_populacao.csv")

    if not os.path.exists(caminho):
        raise FileNotFoundError("ibge_populacao.csv não encontrado. Rode o 01_aquisicao.py primeiro.")

    df = pd.read_csv(caminho, encoding="utf-8-sig", sep=",")
    df = df[["uf_nome", "populacao"]].drop_duplicates(subset="uf_nome")
    df = df.rename(columns={"uf_nome": "uf_nome_ibge"})
    print(f"[LER]  ibge_populacao.csv: {len(df)} estados carregados")
    return df


def adicionar_ano(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """Adiciona coluna de ano ao DataFrame."""
    df = df.copy()
    df["ano"] = 2024
    print(f"[ANO] {label}: {len(df):,} registros")
    return df


def merge_ocorrencias_pessoas(df_ocorrencias: pd.DataFrame, df_pessoas: pd.DataFrame) -> pd.DataFrame:
    """
    Merge entre ocorrências e pessoas pelo id do acidente (1:N).
    """
    chave = "id"
    if chave not in df_ocorrencias.columns:
        raise KeyError(f"Coluna '{chave}' não encontrada em ocorrências.")
    if chave not in df_pessoas.columns:
        raise KeyError(f"Coluna '{chave}' não encontrada em pessoas.")

    # Evita colunas duplicadas renomeando as de pessoas
    colunas_ocorrencias = set(df_ocorrencias.columns)
    colunas_pessoas     = set(df_pessoas.columns)
    duplicadas          = colunas_ocorrencias & colunas_pessoas - {chave, "ano"}

    df_pessoas = df_pessoas.rename(
        columns={col: f"{col}_pessoa" for col in duplicadas if col != chave}
    )

    df_merged = pd.merge(df_ocorrencias, df_pessoas, on=[chave, "ano"], how="left")
    print(f"[MERGE] PRF: {len(df_merged):,} registros, {df_merged.shape[1]} colunas")
    return df_merged


def merge_ibge(df: pd.DataFrame, df_ibge: pd.DataFrame) -> pd.DataFrame:
    """
    Merge com dados do IBGE pelo estado.
    Adiciona coluna de população por UF.
    """
    # Padroniza nome do estado para maiúsculo para fazer o join
    df["uf_upper"] = df["uf"].str.upper().str.strip()
    df_ibge["uf_upper"] = df_ibge["uf_nome_ibge"].str.upper().str.strip()

    df = pd.merge(df, df_ibge[["uf_upper", "populacao"]], on="uf_upper", how="left")
    df = df.drop(columns=["uf_upper"])

    matched = df["populacao"].notna().sum()
    print(f"[MERGE] IBGE: {matched:,} registros com população linkada")
    return df


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("ETAPA 2 — INTEGRAÇÃO DE DADOS\n")

    # Leitura PRF
    print("Lendo arquivos da PRF")
    oc_2024 = ler_csv_prf("datatran2024.csv")
    pe_2024 = ler_csv_prf("acidentes2024.csv")

    # Leitura IBGE
    print("\nLendo dados do IBGE")
    df_ibge = ler_ibge()

    # Adiciona ano
    print("\nAdicionando coluna de ano")
    df_ocorrencias = adicionar_ano(oc_2024, "Ocorrências")
    df_pessoas     = adicionar_ano(pe_2024, "Pessoas")

    # Merge PRF: ocorrências x pessoas
    print("\nMerge 1: ocorrências x pessoas (PRF)")
    df_merged = merge_ocorrencias_pessoas(df_ocorrencias, df_pessoas)

    # Merge com IBGE
    print("\nMerge 2: PRF x IBGE (população por estado)")
    df_merged = merge_ibge(df_merged, df_ibge)

    # Salvando
    print("\nSalvando arquivos processados")
    caminho_merged = os.path.join(PROCESSED_DIR, "acidentes_merged.csv")
    df_merged.to_csv(caminho_merged, index=False, encoding="utf-8-sig", sep=";")

    print(f"[OK]  acidentes_merged.csv ({len(df_merged):,} linhas, {df_merged.shape[1]} colunas)")
    print("\n[CONCLUÍDO] Arquivos salvos em data/processed/")


if __name__ == "__main__":
    main()