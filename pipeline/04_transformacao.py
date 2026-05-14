import os
import pandas as pd
import numpy as np

# Configurações

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

ENTRADA = os.path.join(PROCESSED_DIR, "acidentes_limpos.csv")
SAIDA   = os.path.join(PROCESSED_DIR, "acidentes_final.csv")

# Funções para carregar e transformar os dados

def carregar(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, low_memory=False, sep=";", encoding="utf-8-sig", parse_dates=["data_inversa"])
    print(f"[LER]  {len(df):,} registros carregados")
    return df


def criar_periodo_dia(hora: pd.Series) -> pd.Series:
    bins   = [-1, 5, 11, 17, 23]
    labels = ["Madrugada (0-5h)", "Manhã (6-11h)", "Tarde (12-17h)", "Noite (18-23h)"]
    return pd.cut(hora, bins=bins, labels=labels)


def classificar_gravidade(df: pd.DataFrame) -> pd.Series:
    """
    Fatal        (mortos > 0)
    Grave        (feridos_graves > 0, sem mortos)
    Leve         (apenas feridos leves)
    Sem vítimas
    """
    condicoes = [
        df["mortos"] > 0,
        (df["mortos"] == 0) & (df["feridos_graves"] > 0),
        (df["mortos"] == 0) & (df["feridos_graves"] == 0) & (df["feridos_leves"] > 0),
    ]
    valores = ["Fatal", "Grave", "Leve"]
    return np.select(condicoes, valores, default="Sem vítimas")


def adicionar_colunas_temporais(df: pd.DataFrame) -> pd.DataFrame:
    df["mes"]           = df["data_inversa"].dt.month
    df["mes_nome"]      = df["data_inversa"].dt.strftime("%b")
    df["trimestre"]     = df["data_inversa"].dt.quarter
    df["semana_do_ano"] = df["data_inversa"].dt.isocalendar().week.astype(int)
    print("[TRANSF] Colunas criadas: mes, mes_nome, trimestre, semana_do_ano")
    return df


def adicionar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    if "hora" in df.columns:
        df["periodo_dia"] = criar_periodo_dia(df["hora"])
        print("[TRANSF] Coluna criada: periodo_dia")

    df["gravidade"] = classificar_gravidade(df)
    print("[TRANSF] Coluna criada: gravidade (Fatal / Grave / Leve / Sem vítimas)")

    df["total_envolvidos"] = (
        df[["mortos", "feridos_leves", "feridos_graves", "ilesos"]]
        .sum(axis=1)
    )
    print("[TRANSF] Coluna criada: total_envolvidos")

    df["fim_de_semana"] = df["dia_semana"].isin(["SÁBADO", "DOMINGO", "SABADO"])
    print("[TRANSF] Coluna criada: fim_de_semana")

    return df


def main():
    print("ETAPA 4 — TRANSFORMAÇÃO\n")

    df = carregar(ENTRADA)

    print("\nAdicionando colunas temporais")
    df = adicionar_colunas_temporais(df)

    print("\nAdicionando colunas derivadas")
    df = adicionar_colunas_derivadas(df)

    df.to_csv(SAIDA, index=False, encoding="utf-8-sig", sep=";")
    print(f"\n[OK] acidentes_final.csv salvo ({len(df):,} linhas, {df.shape[1]} colunas)")
    print("[CONCLUÍDO]")


if __name__ == "__main__":
    main()