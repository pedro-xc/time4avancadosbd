# Dashboard de Acidentes em Rodovias Federais — PRF

**Disciplina:** Análise Prática de Dados  
**Professor:** José Guilherme Picolo  
**Time:** 4  
**Integrantes:**
- Gabriel Flores
- João Gabriel
- Pedro Daou
- Pedro Ximenes
- Yuri Balieiro

---

## Sobre o Projeto

Este projeto tem como objetivo analisar os acidentes registrados nas rodovias federais brasileiras em 2024, utilizando dados públicos da Polícia Rodoviária Federal (PRF) cruzados com estimativas populacionais do IBGE.

A análise busca identificar padrões de risco, comparar o comportamento dos acidentes entre estados, períodos do dia, condições climáticas e causas mais frequentes, comunicando os resultados por meio de dois dashboards interativos construídos com Python e Dash.

---

## Fontes de Dados

| Arquivo | Fonte | Coleta | Descrição |
|---|---|---|---|
| `datatran2024.csv` | PRF — Dados Abertos | Manual | Um registro por acidente em 2024 |
| `acidentes2024.csv` | PRF — Dados Abertos | Manual | Um registro por pessoa envolvida em 2024 |
| `ibge_populacao.csv` | IBGE — API Pública | **Automática (crawler)** | Estimativa populacional por estado (2024) |

Portal PRF: https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf  
API IBGE: https://servicodados.ibge.gov.br/api/docs/agregados

---

## Estrutura do Projeto

```
projeto-acidentes-prf/
│
├── data/
│   ├── raw/                          # Arquivos originais (PRF manual + IBGE via API)
│   └── processed/                    # Dados tratados prontos para o dashboard
│
├── pipeline/
│   ├── 01_aquisicao.py               # Verifica CSVs da PRF + crawler API do IBGE
│   ├── 02_integracao.py              # Merge entre ocorrências e pessoas
│   ├── 03_limpeza.py                 # Limpeza e padronização
│   └── 04_transformacao.py           # Novas variáveis e geração do arquivo final
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
- Verifica se os 2 CSVs da PRF estão presentes em `data/raw/` e avisa caso falte algum
- Coleta automaticamente a estimativa populacional dos 27 estados via API pública do IBGE e salva como `ibge_populacao.csv`

### 02 — Integração
- Lê os dois CSVs da PRF (ocorrências e pessoas)
- Faz merge entre os dois pelo `id` do acidente (relação 1:N)
- Salva resultado em `data/processed/acidentes_merged.csv`

### 03 — Limpeza
- Remoção de linhas duplicadas
- Tratamento de valores ausentes (contagens de vítimas → 0, categorias → "Não informado")
- Conversão de datas e horários para tipos corretos
- Padronização de strings (maiúsculas, sem espaços extras)
- Remoção de registros com datas inválidas ou fora de 2024

### 04 — Transformação
Novas colunas criadas:

| Coluna | Descrição |
|---|---|
| `mes`, `mes_nome` | Mês numérico e abreviado |
| `trimestre` | Trimestre do ano |
| `semana_do_ano` | Semana do ano |
| `hora` | Hora do acidente (0–23) |
| `periodo_dia` | Madrugada / Manhã / Tarde / Noite |
| `gravidade` | Fatal / Grave / Leve / Sem vítimas |
| `total_envolvidos` | Soma de mortos + feridos + ilesos |
| `fim_de_semana` | True se sábado ou domingo |

Arquivo gerado: `acidentes_final.csv` — base completa usada pelos dashboards.