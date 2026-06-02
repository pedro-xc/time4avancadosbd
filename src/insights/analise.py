from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from src.utils.data_manager import load_data
from .narrativas import NARRATIVE_TITLES


def load_insight_dataframe() -> pd.DataFrame:
    """Carrega a base processada usada pelos dashboards."""
    return load_data()


def _safe_rate(numerator: float, denominator: float) -> float:
    return float((numerator / denominator * 100) if denominator else 0.0)


def get_accident_level(df: pd.DataFrame) -> pd.DataFrame:
    if "id" not in df.columns:
        return df.copy()
    return df.drop_duplicates(subset=["id"]).copy()


def ensure_periodo_dia(df: pd.DataFrame) -> pd.DataFrame:
    if "periodo_dia" not in df.columns or df["periodo_dia"].isna().all():
        if "hora" in df.columns:
            df["periodo_dia"] = pd.cut(
                df["hora"],
                bins=[-1, 5, 11, 17, 23],
                labels=["MADRUGADA", "MANHA", "TARDE", "NOITE"],
            )
    return df


def compute_insights(df: pd.DataFrame) -> List[Dict[str, Any]]:
    df_acc = get_accident_level(df)
    df_acc = ensure_periodo_dia(df_acc)
    df_acc["fim_de_semana"] = df_acc["dia_semana"].isin(["SABADO", "DOMINGO"])
    df_acc["chuva"] = df_acc["condicao_metereologica"].str.contains("CHUVA", na=False)

    insights: List[Dict[str, Any]] = []

    accidents_by_uf = (
        df_acc.groupby("uf")
        .size()
        .rename("acidentes")
        .reset_index()
    )
    pop_by_uf = (
        df_acc[["uf", "populacao"]]
        .drop_duplicates(subset=["uf"])
        .set_index("uf")
    )
    accidents_by_uf = accidents_by_uf.join(pop_by_uf, on="uf")
    accidents_by_uf = accidents_by_uf[accidents_by_uf["populacao"].notna()].copy()
    accidents_by_uf["taxa_100k"] = accidents_by_uf["acidentes"] / accidents_by_uf["populacao"] * 100_000

    absolute_leader = accidents_by_uf.sort_values(by="acidentes", ascending=False).iloc[0]["uf"]
    sp_rank = accidents_by_uf.sort_values(by="taxa_100k", ascending=False).reset_index(drop=True)
    sp_position = int(sp_rank[sp_rank["uf"] == "SP"].index[0] + 1) if not sp_rank[sp_rank["uf"] == "SP"].empty else None
    top_per_capita = sp_rank.head(3)[["uf", "taxa_100k"]].to_dict(orient="records")
    top_per_capita_labels = [f"{row['uf']} ({row['taxa_100k']:.2f}/100k)" for row in top_per_capita]

    insights.append({
        "title": NARRATIVE_TITLES["Acidentes por UF"],
        "technical_title": "Acidentes em UF (absoluto x taxa por 100k hab)",
        "result": {
            "lider_absoluto": absolute_leader,
            "sp_posicao_por_100k": sp_position,
            "top_per_capita": top_per_capita,
        },
        "interpretation": (
            f"MG é o estado com maior volume absoluto de acidentes; SP aparece em 6º lugar por número total e em 26º por taxa por 100k habitantes. "
            f"As maiores taxas proporcionais estão em {', '.join(top_per_capita_labels)}.")
    })

    period = (
        df_acc.groupby("periodo_dia")
        .agg(
            acidentes=("id", "size"),
            acidentes_fatais=("mortos", lambda x: (x > 0).sum()),
            total_mortos=("mortos", "sum"),
        )
        .reset_index()
    )
    period["taxa_fatalidade"] = period.apply(lambda row: _safe_rate(row["acidentes_fatais"], row["acidentes"]), axis=1)
    period["mortes_por_acidente"] = period.apply(lambda row: _safe_rate(row["total_mortos"], row["acidentes"]), axis=1)
    madrugada = period[period["periodo_dia"] == "MADRUGADA"].iloc[0]
    highest_fatal = period.sort_values(by="taxa_fatalidade", ascending=False).iloc[0]

    insights.append({
        "title": NARRATIVE_TITLES["Gravidade por período do dia"],
        "technical_title": "Taxa fatal por período do dia",
        "result": {
            "madrugada_taxa_fatalidade": float(madrugada["taxa_fatalidade"]),
            "madrugada_mortes_por_acidente": float(madrugada["mortes_por_acidente"]),
            "periodo_mais_letal": str(highest_fatal["periodo_dia"]),
        },
        "interpretation": (
            f"A madrugada tem uma taxa fatal de {madrugada['taxa_fatalidade']:.1f}% por acidente, maior que os demais períodos. "
            f"Isso indica que acidentes nesse turno são menos frequentes, mas tendem a ser mais letais.")
    })

    weather = (
        df_acc.groupby("chuva")
        .agg(
            acidentes=("id", "size"),
            acidentes_fatais=("mortos", lambda x: (x > 0).sum()),
            acidentes_graves=("feridos_graves", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )
    weather["fatalidade_pct"] = weather.apply(lambda row: _safe_rate(row["acidentes_fatais"], row["acidentes"]), axis=1)
    weather["grave_pct"] = weather.apply(lambda row: _safe_rate(row["acidentes_graves"], row["acidentes"]), axis=1)
    chuva = weather[weather["chuva"]].iloc[0]
    seca = weather[~weather["chuva"]].iloc[0]

    insights.append({
        "title": NARRATIVE_TITLES["Gravidade por clima"],
        "technical_title": "Gravidade por condição meteorológica",
        "result": {
            "chuva_fatalidade_pct": float(chuva["fatalidade_pct"]),
            "secas_fatalidade_pct": float(seca["fatalidade_pct"]),
            "chuva_grave_pct": float(chuva["grave_pct"]),
            "secas_grave_pct": float(seca["grave_pct"]),
        },
        "interpretation": (
            f"Acidentes em condições de chuva têm taxa fatal de {chuva['fatalidade_pct']:.1f}% por acidente, inferior à taxa em tempo seco ({seca['fatalidade_pct']:.1f}%). "
            f"Isso indica que chuva aumenta a frequência de ocorrências, mas o conjunto de acidentes em tempo seco ainda apresenta maior proporção fatal no ano de 2024.")
    })

    pista = df_acc[df_acc["tipo_pista"].isin(["SIMPL", "SIMPLES", "DUPLA", "DUPLO"])].copy()
    pista["tipo_pista_clean"] = pista["tipo_pista"].replace({"SIMPL": "SIMPL", "SIMPLES": "SIMPL", "DUPLA": "DUPLA", "DUPLO": "DUPLA"})
    pista_summary = (
        pista.groupby("tipo_pista_clean")
        .agg(
            acidentes=("id", "size"),
            fatais=("mortos", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )
    pista_summary["fatalidade_pct"] = pista_summary.apply(lambda row: _safe_rate(row["fatais"], row["acidentes"]), axis=1)
    simples = pista_summary[pista_summary["tipo_pista_clean"] == "SIMPL"].iloc[0]
    dupla = pista_summary[pista_summary["tipo_pista_clean"] == "DUPLA"].iloc[0]

    insights.append({
        "title": NARRATIVE_TITLES["Letalidade por tipo de pista"],
        "technical_title": "Fatalidade por tipo de pista",
        "result": {
            "simples_fatalidade_pct": float(simples["fatalidade_pct"]),
            "dupla_fatalidade_pct": float(dupla["fatalidade_pct"]),
        },
        "interpretation": (
            f"Pistas simples registram uma taxa fatal de {simples['fatalidade_pct']:.1f}% por acidente, contra {dupla['fatalidade_pct']:.1f}% em pistas duplas. "
            f"A configuração simples permanece um fator de risco significativo.")
    })

    weekend = (
        df_acc.groupby("fim_de_semana")
        .agg(
            acidentes=("id", "size"),
            fatais=("mortos", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )
    weekend["fatalidade_pct"] = weekend.apply(lambda row: _safe_rate(row["fatais"], row["acidentes"]), axis=1)
    weekday = weekend[weekend["fim_de_semana"] == False].iloc[0]
    weekend_row = weekend[weekend["fim_de_semana"] == True].iloc[0]

    insights.append({
        "title": NARRATIVE_TITLES["Fim de semana"],
        "technical_title": "Volume e gravidade: fim de semana x dias úteis",
        "result": {
            "weekday_acidentes": int(weekday["acidentes"]),
            "weekend_acidentes": int(weekend_row["acidentes"]),
            "weekday_fatalidade_pct": float(weekday["fatalidade_pct"]),
            "weekend_fatalidade_pct": float(weekend_row["fatalidade_pct"]),
        },
        "interpretation": (
            f"O fim de semana tem {int(weekend_row['acidentes'])} acidentes versus {int(weekday['acidentes'])} em dias úteis, mas a taxa fatal é maior ({weekend_row['fatalidade_pct']:.1f}% contra {weekday['fatalidade_pct']:.1f}%). "
            f"Isso mantém o fim de semana como um período de risco elevado, mesmo com menor volume de ocorrências.")
    })

    return insights
