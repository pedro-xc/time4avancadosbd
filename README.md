# time4avancadosbd# Dashboard de Acidentes em Rodovias Federais — PRF

**Disciplina:** Estudo Avançados de Banco de Dados
**Time:** 4  
**Integrantes:**
- Gabriel Flores
- João Gabriel
- Pedro Daou
- Pedro Ximenes
- Yuri Balieiro

---

## Sobre o Projeto

Este projeto tem como objetivo analisar os acidentes registrados nas rodovias federais brasileiras nos anos de 2023 e 2024, utilizando dados públicos da Polícia Rodoviária Federal (PRF).

A análise busca identificar padrões de risco, comparar o comportamento dos acidentes entre estados, períodos do dia, condições climáticas e causas mais frequentes, comunicando os resultados por meio de dois dashboards interativos construídos com Python e Dash.

---

## Fontes de Dados

| Arquivo | Fonte | Descrição |
|---|---|---|
| `acidentes_2023_ocorrencias.csv` | PRF — Dados Abertos | Um registro por acidente em 2023 |
| `acidentes_2023_pessoas.csv` | PRF — Dados Abertos | Um registro por pessoa envolvida em 2023 |
| `acidentes_2024_ocorrencias.csv` | PRF — Dados Abertos | Um registro por acidente em 2024 |
| `acidentes_2024_pessoas.csv` | PRF — Dados Abertos | Um registro por pessoa envolvida em 2024 |

Portal oficial: https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf

---

## Estrutura do Projeto

```
projeto-acidentes-prf/
│
├── data/
│   ├── raw/                          # CSVs originais baixados da PRF
│   └── processed/                    # Dados tratados e agregados
│
├── pipeline/
│   ├── 01_aquisicao.py               # Download dos CSVs do Google Drive
│   ├── 02_integracao.py              # Concatenação e merge dos dados
│   ├── 03_limpeza.py                 # Limpeza e padronização
│   └── 04_transformacao.py           # Novas variáveis e agregações
│
├── dashboards/
│   ├── dashboard1_visao_geral.py     # Painel executivo
│   ├── dashboard2_exploratorio.py    # Exploração interativa
│   └── components/
│       ├── graficos.py               # Funções reutilizáveis de gráficos
│       └── layout.py                 # Componentes de layout Dash
│
├── app.py                            # Ponto de entrada da aplicação
├── requirements.txt                  # Dependências do projeto
└── README.md
```

---

## Pipeline de Dados

### 01 — Aquisição
Download automático dos 4 arquivos CSV diretamente do Google Drive da PRF. O script verifica se o arquivo já existe antes de baixar, evitando downloads duplicados.

### 02 — Integração
- Concatenação dos dados de 2023 e 2024 para cada tipo (ocorrências e pessoas)
- Merge entre o dataset de ocorrências e o de pessoas pelo `id` do acidente (relação 1:N)
- Geração de 3 arquivos intermediários em `data/processed/`

### 03 — Limpeza
- Remoção de linhas duplicadas
- Tratamento de valores ausentes (contagens de vítimas → 0, categorias → "Não informado")
- Conversão de datas e horários para tipos corretos
- Padronização de strings (maiúsculas, sem espaços extras)
- Remoção de registros com datas inválidas ou fora do período 2023–2024

### 04 — Transformação
Novas colunas criadas:

| Coluna | Descrição |
|---|---|
| `mes`, `mes_nome` | Mês numérico e abreviado |
| `trimestre` | Trimestre do ano |
| `semana_do_ano` | Semana epidemiológica |
| `hora` | Hora do acidente (0–23) |
| `periodo_dia` | Madrugada / Manhã / Tarde / Noite |
| `faixa_horaria` | Agrupamento em blocos de 6h |
| `gravidade` | Fatal / Grave / Leve / Sem vítimas |
| `total_envolvidos` | Soma de mortos + feridos + ilesos |
| `fim_de_semana` | True se sábado ou domingo |

Agregações geradas para o dashboard:

| Arquivo | Conteúdo |
|---|---|
| `acidentes_final.csv` | Base completa transformada |
| `agg_por_estado.csv` | Totais e taxa de mortalidade por UF |
| `agg_por_mes.csv` | Evolução mensal de acidentes e vítimas |
| `agg_por_causa.csv` | Ranking de causas de acidente |
| `agg_por_tipo.csv` | Ranking de tipos de acidente |
| `agg_por_hora.csv` | Distribuição horária |
| `agg_por_clima_gravidade.csv` | Cruzamento clima × gravidade |