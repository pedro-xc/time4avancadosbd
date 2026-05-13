import os
import requests

# Configurações

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# IDs dos arquivos no Google Drive da PRF
ARQUIVOS = {
    "acidentes_2023_ocorrencias.csv": "1-WO3SfNrwwZ5_l7fRTiwBKRw7mi1-HUq",
    "acidentes_2023_pessoas.csv":     "1-Yk6TV00CH3PixTkKmkoUJQsNiUc5xLm",
    "acidentes_2024_ocorrencias.csv": "14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO",
    "acidentes_2024_pessoas.csv":     "14lVfqdoE2gxDliaKZu7K9Mx6847maPtl",
}

# Funções 

def montar_url_drive(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"


def baixar_arquivo(nome: str, file_id: str) -> None:
    destino = os.path.join(RAW_DIR, nome)

    if os.path.exists(destino):
        print(f"[SKIP] {nome} já existe, pulando download.")
        return

    print(f"[DOWN] Baixando {nome}...")
    url = montar_url_drive(file_id)

    session = requests.Session()
    resposta = session.get(url, stream=True, timeout=120)

    # Google Drive exige confirmação para arquivos grandes
    for chave, valor in resposta.cookies.items():
        if "download_warning" in chave:
            resposta = session.get(url, params={"confirm": valor}, stream=True, timeout=120)
            break

    resposta.raise_for_status()

    with open(destino, "wb") as f:
        for chunk in resposta.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

    tamanho_mb = os.path.getsize(destino) / (1024 * 1024)
    print(f"[OK]   {nome} salvo ({tamanho_mb:.1f} MB)")


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    print("=== ETAPA 1 — AQUISIÇÃO DE DADOS ===\n")

    for nome, file_id in ARQUIVOS.items():
        baixar_arquivo(nome, file_id)

    print("\n[CONCLUÍDO] Todos os arquivos estão em data/raw/")


if __name__ == "__main__":
    main()