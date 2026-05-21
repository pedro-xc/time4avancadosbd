from pathlib import Path
from typing import Dict, Iterable, List


def save_insights_summary(insights: List[Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Insights não óbvios — Acidentes PRF 2024\n\n")
        for index, insight in enumerate(insights, start=1):
            f.write(f"## Insight {index}: {insight['title']}\n\n")
            f.write(f"**Título técnico**: {insight['technical_title']}\n\n")
            f.write(f"**Interpretação**: {insight['interpretation']}\n\n")
            f.write("**Resultados**:\n")
            for key, value in insight["result"].items():
                f.write(f"- {key}: {value}\n")
            f.write("\n")
        f.write("---\n")
        f.write("Títulos narrativos sugeridos para gráficos:\n")
        for insight in insights:
            f.write(f"- {insight['technical_title']} → {insight['title']}\n")
