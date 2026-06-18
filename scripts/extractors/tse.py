import os
import requests
import zipfile
import tempfile
import sys

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_PAI = os.path.dirname(DIRETORIO_ATUAL)

sys.path.append(DIRETORIO_PAI)

from constants_tse import (
    URL_TSE_2018, 
    URL_TSE_2022, 
    TARGET_CSV_2018, 
    TARGET_CSV_2022, 
    RAW_DATA_DIR
)

def baixar_e_extrair_tse(url_zip, nome_arquivo_alvo):
    """
    Faz o download do ZIP do TSE via stream e extrai apenas o arquivo de interesse.
    """
    # 1. Garante que a pasta data/raw/ existe
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    caminho_final_csv = os.path.join(RAW_DATA_DIR, nome_arquivo_alvo)
    
    # Pula a extração se o arquivo já existir na pasta (evita retrabalho)
    if os.path.exists(caminho_final_csv):
        print(f"O arquivo {nome_arquivo_alvo} já existe em {RAW_DATA_DIR}. Pulando extração.")
        return

    print(f"Iniciando download de: {url_zip}")
    
    # 2. Cria um arquivo temporário no sistema para não lotar a RAM
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
        # Faz a requisição em modo stream (baixa em pedaços)
        resposta = requests.get(url_zip, stream=True)
        resposta.raise_for_status() # Verifica se deu erro no download
        
        # Escreve os pedaços (chunks) de 8MB no disco
        for chunk in resposta.iter_content(chunk_size=8192 * 1024): 
            if chunk:
                tmp_zip.write(chunk)
                
        caminho_tmp_zip = tmp_zip.name

    print("Download concluído. Iniciando extração do CSV alvo...")

    # 3. Abre o ZIP temporário e extrai apenas o arquivo BR.csv
    try:
        with zipfile.ZipFile(caminho_tmp_zip, 'r') as zip_ref:
            if nome_arquivo_alvo in zip_ref.namelist():
                # Extrai especificamente o CSV nacional para a pasta raw
                zip_ref.extract(nome_arquivo_alvo, path=RAW_DATA_DIR)
                print(f"Sucesso: {nome_arquivo_alvo} extraído para {RAW_DATA_DIR}")
            else:
                print(f"Erro: O arquivo {nome_arquivo_alvo} não foi encontrado no ZIP.")
    finally:
        # 4. Limpeza: apaga o arquivo ZIP gigante temporário do seu computador
        os.remove(caminho_tmp_zip)
        print("Arquivo ZIP temporário removido para liberar espaço.")

def main():
    print("--- Iniciando Pipeline de Extração: TSE ---")
    
    # Executa a extração para 2018
    baixar_e_extrair_tse(URL_TSE_2018, TARGET_CSV_2018)
    
    # Executa a extração para 2022
    baixar_e_extrair_tse(URL_TSE_2022, TARGET_CSV_2022)
    
    print("--- Extração Finalizada com Sucesso! ---")

if __name__ == "__main__":
    main()