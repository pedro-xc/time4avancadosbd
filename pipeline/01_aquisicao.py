import os
import requests
import pandas as pd
from urllib.request import urlopen, Request
import json
import gzip

# Configurações

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# Arquivos PRF esperados em data/raw/
ARQUIVOS_PRF = [
    "datatran2024.csv",
    "acidentes2024.csv",
]

# Endpoint IBGE — Estimativa populacional por UF
# Tabela 6579 | Variável 9324 (população estimada) | N3 = estados
IBGE_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"
IBGE_ANOS = ["2024"]

# Funções

def verificar_arquivos_prf() -> None:
    """Verifica se os CSVs da PRF estão presentes em data/raw/."""
    print("Verificando arquivos da PRF")
    todos_ok = True
    for nome in ARQUIVOS_PRF:
        caminho = os.path.join(RAW_DIR, nome)
        if os.path.exists(caminho):
            tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
            print(f"[OK]   {nome} ({tamanho_mb:.1f} MB)")
        else:
            print(f"[FALTA] {nome}")
            todos_ok = False

    if not todos_ok:
        print("\n[AVISO] Baixe os arquivos faltantes em:")
        print("        https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf")
        print("        e coloque em data/raw/ antes de rodar o 02_integracao.py")
    else:
        print("\n[OK] Todos os arquivos da PRF estão presentes!")


def coletar_populacao_ibge(ano: str) -> list:
    """
    Faz requisição à API do IBGE e retorna lista de dicts com
    uf, ano e população estimada para todos os estados.
    """
    url = (
        f"{IBGE_BASE}/6579"
        f"/periodos/{ano}/variaveis/9324"
        f"?localidades=N3[all]"
    )

    headers = {"User-Agent": "Mozilla/5.0 (projeto acadêmico PUC-Campinas)"}

    print(f"[GET]  {url}")
    # urllib preserva os colchetes sem encoding, exigido pela API do IBGE
    requisicao = Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "Mozilla/5.0"})
    resposta = urlopen(requisicao, timeout=30)
    conteudo = resposta.read()
    # Descomprime gzip se necessário
    if resposta.info().get("Content-Encoding") == "gzip" or conteudo[:2] == b'\x1f\x8b':
        conteudo = gzip.decompress(conteudo)
    dados = json.loads(conteudo.decode("utf-8"))

    # Estrutura real da resposta:
    # [{ "id": "9324", "resultados": [{ "series": [{ "localidade": {"id":"11","nome":"Rondônia"}, "serie": {"2024": "1746227"} }] }] }]
    registros = []
    for variavel in dados:
        for resultado in variavel.get("resultados", []):
            for item in resultado.get("series", []):
                localidade = item.get("localidade", {})
                serie      = item.get("serie", {})

                codigo = localidade.get("id", "")
                nome   = localidade.get("nome", "")
                valor  = serie.get(ano)

                registros.append({
                    "uf_codigo": codigo,
                    "uf_nome":   nome,
                    "uf":        nome.upper(),
                    "ano":       int(ano),
                    "populacao": int(valor) if valor and valor != "-" else None,
                })

    return registros


def coletar_ibge() -> None:
    destino = os.path.join(RAW_DIR, "ibge_populacao.csv")

    if os.path.exists(destino):
        print("[SKIP] ibge_populacao.csv já existe, pulando coleta.")
        return

    print("Coletando população por estado via API do IBGE")

    todos_registros = []
    for ano in IBGE_ANOS:
        registros = coletar_populacao_ibge(ano)
        todos_registros.extend(registros)
        print(f"[OK]  {ano}: {len(registros)} estados coletados")

    df = pd.DataFrame(todos_registros)
    df = df[df["populacao"].notna()]
    df = df.sort_values(["ano", "uf"]).reset_index(drop=True)

    df.to_csv(destino, index=False, encoding="utf-8-sig", sep=",")

    print(f"\n[OK]  ibge_populacao.csv salvo ({len(df)} registros)")
    print("\nPreview:")
    print(df.head(8).to_string(index=False))


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    print("ETAPA 1 — AQUISIÇÃO DE DADOS\n")

    # PRF: verifica arquivos manuais
    verificar_arquivos_prf()

    print()

    # IBGE: coleta automática via API
    print("Iniciando crawler — API pública do IBGE")
    coletar_ibge()

    print("\n[CONCLUÍDO] Etapa 1 finalizada.")
    print("Próximo passo: rodar 02_integracao.py")


if __name__ == "__main__":
    main()