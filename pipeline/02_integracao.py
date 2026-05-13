import os
import pandas as pd

# Configurações

RAW_DIR       = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Funções

def ler_csv_prf(nome: str) -> pd.DataFrame:
    """Lê um CSV da PRF com encoding e separador corretos."""
    caminho = os.path.join(RAW_DIR, nome)
    df = pd.read_csv(caminho, sep=";", encoding="latin1", low_memory=False)
    print(f"[LER]  {nome}: {len(df):,} registros, {df.shape[1]} colunas")
    return df


def concatenar_anos(df_2023: pd.DataFrame, df_2024: pd.DataFrame, label: str) -> pd.DataFrame:
    """Concatena dois DataFrames do mesmo tipo e adiciona coluna de ano."""
    df_2023 = df_2023.copy()
    df_2024 = df_2024.copy()
    df_2023["ano"] = 2023
    df_2024["ano"] = 2024

    df = pd.concat([df_2023, df_2024], ignore_index=True)
    print(f"[CONCAT] {label}: {len(df):,} registros totais após concatenação")
    return df


def fazer_merge(df_ocorrencias: pd.DataFrame, df_pessoas: pd.DataFrame) -> pd.DataFrame:
    """
    Merge entre ocorrências e pessoas pelo id do acidente.
    Cada ocorrência pode ter múltiplas pessoas envolvidas (1:N).
    """
    chave = "id"
    if chave not in df_ocorrencias.columns:
        raise KeyError(f"Coluna '{chave}' não encontrada em ocorrências. Colunas: {df_ocorrencias.columns.tolist()}")
    if chave not in df_pessoas.columns:
        raise KeyError(f"Coluna '{chave}' não encontrada em pessoas. Colunas: {df_pessoas.columns.tolist()}")

    # Evita colunas duplicadas renomeando as de pessoas (exceto a chave)
    colunas_ocorrencias = set(df_ocorrencias.columns)
    colunas_pessoas     = set(df_pessoas.columns)
    duplicadas          = colunas_ocorrencias & colunas_pessoas - {chave, "ano"}

    df_pessoas = df_pessoas.rename(
        columns={col: f"{col}_pessoa" for col in duplicadas if col != chave}
    )

    df_merged = pd.merge(df_ocorrencias, df_pessoas, on=[chave, "ano"], how="left")
    print(f"[MERGE] Resultado: {len(df_merged):,} registros, {df_merged.shape[1]} colunas")

    pessoas_matched = df_merged[chave].nunique()
    print(f"[MERGE] Acidentes com pelo menos uma pessoa linkada: {pessoas_matched:,} / {df_ocorrencias[chave].nunique():,}")

    return df_merged


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("=== ETAPA 2 — INTEGRAÇÃO DE DADOS ===\n")

    # Leitura
    print("Lendo arquivos de ocorrências")
    oc_2023 = ler_csv_prf("acidentes_2023_ocorrencias.csv")
    oc_2024 = ler_csv_prf("acidentes_2024_ocorrencias.csv")

    print("\nLendo arquivos de pessoas")
    pe_2023 = ler_csv_prf("acidentes_2023_pessoas.csv")
    pe_2024 = ler_csv_prf("acidentes_2024_pessoas.csv")

    # Concatenação por ano
    print("\n Concatenando anos --")
    df_ocorrencias = concatenar_anos(oc_2023, oc_2024, "Ocorrências")
    df_pessoas     = concatenar_anos(pe_2023, pe_2024, "Pessoas")

    # Merge ocorrências + pessoas
    print("\nFazendo merge ocorrências x pessoas")
    df_merged = fazer_merge(df_ocorrencias, df_pessoas)

    # Salvando
    print("\n Salvando arquivos processados")

    caminho_ocorrencias = os.path.join(PROCESSED_DIR, "ocorrencias_concat.csv")
    caminho_pessoas     = os.path.join(PROCESSED_DIR, "pessoas_concat.csv")
    caminho_merged      = os.path.join(PROCESSED_DIR, "acidentes_merged.csv")

    df_ocorrencias.to_csv(caminho_ocorrencias, index=False, encoding="utf-8-sig", sep=",")
    df_pessoas.to_csv(caminho_pessoas, index=False, encoding="utf-8-sig", sep=",")
    df_merged.to_csv(caminho_merged, index=False, encoding="utf-8-sig", sep=",")

    print(f"[OK]  ocorrencias_concat.csv  ({len(df_ocorrencias):,} linhas)")
    print(f"[OK]  pessoas_concat.csv      ({len(df_pessoas):,} linhas)")
    print(f"[OK]  acidentes_merged.csv    ({len(df_merged):,} linhas)")
    print("\n[CONCLUÍDO] Arquivos salvos em data/processed/")


if __name__ == "__main__":
    main()