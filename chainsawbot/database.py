import json
from loguru import logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "arquivo.json"
TAG = "DATABASE: "

def write(data):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"{TAG}Erro ao salvar arquivo: {e}")

def read():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"{TAG}Arquivo '{FILE_PATH}' não encontrado. Retornando lista vazia.")
        return []
    except Exception as e:
        logger.error(f"{TAG}Erro ao ler arquivo: {e}")
        return []