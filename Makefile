# Makefile para gerenciar o projeto Dashboard de Acidentes PRF 2024

.PHONY: help install pipeline run clean

# Target padrão que exibe as opções do Makefile
help:
	@echo "Comandos disponíveis:"
	@echo "  make install   - Instala as dependências do projeto no ambiente virtual (.venv)"
	@echo "  make pipeline  - Executa todas as etapas do pipeline de dados em ordem"
	@echo "  make run       - Inicia o servidor do Dashboard (Dash)"
	@echo "  make clean     - Limpa os arquivos temporários e de cache do Python"

# Instala as dependências utilizando o pip da venv criada
install:
	@echo "Instalando dependências no ambiente virtual (.venv)..."
	.venv/bin/pip install -U pip
	.venv/bin/pip install -r requirements.txt
	@echo "Dependências instaladas com sucesso!"

# Executa todos os passos do pipeline sequencialmente
pipeline:
	@echo "Iniciando a execução do pipeline de dados..."
	@echo ">> [1/4] Coletando/verificando dados brutos..."
	.venv/bin/python pipeline/01_aquisicao.py
	@echo "\n>> [2/4] Integrando dados..."
	.venv/bin/python pipeline/02_integracao.py
	@echo "\n>> [3/4] Limpando dados..."
	.venv/bin/python pipeline/03_limpeza.py
	@echo "\n>> [4/4] Transformando dados e gerando arquivo final..."
	.venv/bin/python pipeline/04_transformacao.py
	@echo "\nPipeline concluído com sucesso!"

# Executa o servidor Dash
run:
	@echo "Iniciando o servidor Dash..."
	.venv/bin/python app.py

# Limpeza de arquivos temporários do python
clean:
	@echo "Limpando arquivos temporários do Python..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Limpeza concluída!"
