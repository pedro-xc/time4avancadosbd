import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.insights import compute_insights, load_insight_dataframe, save_insights_summary


def main() -> None:
    df = load_insight_dataframe()
    if df.empty:
        print("Nenhum dado carregado. Verifique se data/processed/acidentes_final.csv existe e está correto.")
        return

    insights = compute_insights(df)
    save_insights_summary(insights, ROOT / "insights_summary.md")
    print("Análise concluída. Use insights_summary.md para apresentar os resultados.")


if __name__ == "__main__":
    main()
