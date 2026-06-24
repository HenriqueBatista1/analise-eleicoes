import os

## =================================================================
## CONSTANTES PARA EXTRAÇÃO - DADOS DO TSE (PRESIDENTE 2018 E 2022)
## =================================================================

# 1. URLs dos arquivos ZIP originais do repositório de Dados Abertos do TSE
URL_TSE_PRESIDENCIA_2018 = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2018.zip"
URL_TSE_PRESIDENCIA_2022 = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip"
URL_TSE_ELEITORADO_2018 = "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_2018.zip"
URL_TSE_ELEITORADO_2022 = "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_2022.zip"

# 2. Arquivos Alvo dentro do ZIP (Focando na abrangência Nacional/Presidente)
# Isso garante que não vamos carregar os dados de governadores, senadores, etc.
TARGET_CSV_PRESIDENCIA_2018 = "votacao_candidato_munzona_2018_BR.csv"
TARGET_CSV_PRESIDENCIA_2022 = "votacao_candidato_munzona_2022_BR.csv"
TARGET_CSV_ELEITORADO_2018 = "perfil_eleitorado_2018_BR.csv"
TARGET_CSV_ELEITORADO_2022 = "perfil_eleitorado_2022_BR.csv"

# 3. Configurações de Leitura (Conforme o documento leiame.pdf)
CSV_ENCODING = "latin-1"
CSV_SEPARATOR = ";"

# 4. Estrutura de Diretórios Local
# Utiliza caminhos relativos para funcionar no computador de qualquer um do grupo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# Lista de colunas úteis para focar na extração/leitura (Opcional, mas ajuda a otimizar a RAM)
# Vocês podem ajustar caso precise de mais colunas
COLUNAS_INTERESSE = [
    "ANO_ELEICAO",
    "NR_TURNO",
    "SG_UF",
    "NM_MUNICIPIO",
    "DS_CARGO",
    "NR_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "SG_PARTIDO",
    "QT_VOTOS_NOMINAIS"
]