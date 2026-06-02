from __future__ import annotations

from typing import Dict

NARRATIVE_TITLES: Dict[str, str] = {
    "Acidentes por UF": "MG e SC lideram o volume; SP está em 6º no total e 26º por taxa proporcional",
    "Gravidade por período do dia": "Madrugada: menor volume e maior letalidade",
    "Gravidade por clima": "Chuva aparece com muitos acidentes, mas o seco tem taxa fatal proporcionalmente maior",
    "Letalidade por tipo de pista": "Pista simples preserva maior risco fatal do que pista dupla",
    "Fim de semana": "Fim de semana registra menos acidentes, mas cada um é mais perigoso",
}

DASHBOARD_PARAGRAPHS: Dict[str, str] = {
    "Acidentes por UF": (
        "MG aparece com o maior volume absoluto de acidentes, mas SP não é o líder proporcional. "
        "A métrica por 100 mil habitantes revela que estados como SC, RO e MT têm risco relativo mais elevado."
    ),
    "Gravidade por período do dia": (
        "A madrugada concentra menos acidentes, mas aqueles que ocorrem têm uma taxa fatal mais alta. "
        "Isso sugere que o perfil noturno exige atenção especial em fiscalizações e ações preventivas."
    ),
    "Gravidade por clima": (
        "A chuva aumenta o número total de ocorrências, porém a taxa fatal por acidente é maior em condições secas. "
        "Isso mostra que o risco não depende apenas do volume, mas do contexto de exposição e visibilidade." 
    ),
    "Letalidade por tipo de pista": (
        "Pistas simples têm quase o dobro da taxa fatal de pistas duplas, indicando maior vulnerabilidade. "
        "Essa diferença reforça a importância de duplicação e melhorias de infraestrutura em trechos críticos."
    ),
    "Fim de semana": (
        "O fim de semana apresenta menos acidentes no total, mas cada ocorrência tem chance maior de ser fatal. "
        "Portanto, esse período deve ser tratado como de risco elevado, não apenas de maior volume."
    ),
}


def get_narrative_titles() -> Dict[str, str]:
    return NARRATIVE_TITLES.copy()


def get_dashboard_paragraphs() -> Dict[str, str]:
    return DASHBOARD_PARAGRAPHS.copy()
