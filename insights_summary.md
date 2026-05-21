# Insights não óbvios — Acidentes PRF 2024

## Insight 1: MG e SC lideram o volume; SP está em 6º no total e 26º por taxa proporcional

**Título técnico**: Acidentes em UF (absoluto x taxa por 100k hab)

**Interpretação**: MG é o estado com maior volume absoluto de acidentes; SP aparece em 6º lugar por número total e em 26º por taxa por 100k habitantes. As maiores taxas proporcionais estão em SC (104.00/100k), RO (84.93/100k), MT (66.57/100k).

**Resultados**:
- lider_absoluto: MG
- sp_posicao_por_100k: 26
- top_per_capita: [{'uf': 'SC', 'taxa_100k': 104.0027469333088}, {'uf': 'RO', 'taxa_100k': 84.92595750724276}, {'uf': 'MT', 'taxa_100k': 66.57284604651393}]

## Insight 2: Madrugada: menor volume e maior letalidade

**Título técnico**: Taxa fatal por período do dia

**Interpretação**: A madrugada tem uma taxa fatal de 11.3% por acidente, maior que os demais períodos. Isso indica que acidentes nesse turno são menos frequentes, mas tendem a ser mais letais.

**Resultados**:
- madrugada_taxa_fatalidade: 11.304062909567497
- madrugada_mortes_por_acidente: 13.488422892092617
- periodo_mais_letal: MADRUGADA

## Insight 3: Chuva aparece com muitos acidentes, mas o seco tem taxa fatal proporcionalmente maior

**Título técnico**: Gravidade por condição meteorológica

**Interpretação**: Acidentes em condições de chuva têm taxa fatal de 6.3% por acidente, inferior à taxa em tempo seco (7.2%). Isso indica que chuva aumenta a frequência de ocorrências, mas o conjunto de acidentes em tempo seco ainda apresenta maior proporção fatal no ano de 2024.

**Resultados**:
- chuva_fatalidade_pct: 6.253369272237197
- secas_fatalidade_pct: 7.238043081416576
- chuva_grave_pct: 19.460916442048518
- secas_grave_pct: 22.99044663502495

## Insight 4: Pista simples preserva maior risco fatal do que pista dupla

**Título técnico**: Fatalidade por tipo de pista

**Interpretação**: Pistas simples registram uma taxa fatal de 9.9% por acidente, contra 4.7% em pistas duplas. A configuração simples permanece um fator de risco significativo.

**Resultados**:
- simples_fatalidade_pct: 9.924334740839402
- dupla_fatalidade_pct: 4.685974617637488

## Insight 5: Fim de semana registra menos acidentes, mas cada um é mais perigoso

**Título técnico**: Volume e gravidade: fim de semana x dias úteis

**Interpretação**: O fim de semana tem 23382 acidentes versus 49774 em dias úteis, mas a taxa fatal é maior (8.4% contra 6.6%). Isso mantém o fim de semana como um período de risco elevado, mesmo com menor volume de ocorrências.

**Resultados**:
- weekday_acidentes: 49774
- weekend_acidentes: 23382
- weekday_fatalidade_pct: 6.551613292080202
- weekend_fatalidade_pct: 8.386793259772475

---
Títulos narrativos sugeridos para gráficos:
- Acidentes em UF (absoluto x taxa por 100k hab) → MG e SC lideram o volume; SP está em 6º no total e 26º por taxa proporcional
- Taxa fatal por período do dia → Madrugada: menor volume e maior letalidade
- Gravidade por condição meteorológica → Chuva aparece com muitos acidentes, mas o seco tem taxa fatal proporcionalmente maior
- Fatalidade por tipo de pista → Pista simples preserva maior risco fatal do que pista dupla
- Volume e gravidade: fim de semana x dias úteis → Fim de semana registra menos acidentes, mas cada um é mais perigoso
