import os
import requests
import random
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import time


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# configuração
API_KEY = os.getenv("WEATHERSTACK_API_KEY")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 5432))
}
CAPITAIS_BRASIL = [
    "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador", "Fortaleza",
    "Brasília", "Vitória", "Goiânia", "São Luís", "Cuiabá", "Campo Grande",
    "Belo Horizonte", "Belém", "João Pessoa", "Curitiba", "Recife",
    "Teresina", "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho",
    "Boa Vista", "Florianópolis", "São Paulo", "Aracaju", "Palmas"
]

RAIN_KEYWORDS = ["rain", "drizzle", "thunderstorm"]

# funções

def obter_clima_atual(cidade):
    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": API_KEY,
        "query": cidade,
        "units": "m"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def classificar_conforto(temp):
    if temp < 15:
        return "Frio"
    elif 15 <= temp <= 25:
        return "Agradável"
    return "Quente"


def verificar_chuva(descricao):
    descricao = descricao.lower()
    return any(palavra in descricao for palavra in RAIN_KEYWORDS)


def simular_previsao_7_dias(temp_base):
    previsoes = []
    for i in range(7):
        variacao = random.uniform(-2, 2)
        previsoes.append(round(temp_base + variacao, 2))
    return previsoes


def salvar_dados(conn, registros):
    with conn.cursor() as cur:
        for r in registros:
            cur.execute("""
                INSERT INTO previsao_tempo
                (cidade, data_previsao, temp_media, tem_chuva, indice_conforto, criado_em)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, r)
    conn.commit()

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    registros = []

    for cidade in CAPITAIS_BRASIL:
        print(f"Processando cidade: {cidade}")
        dados = obter_clima_atual(cidade)

        time.sleep(1.5) # delay para evitar erro de too many

        temp_atual = dados["current"]["temperature"]
        descricao = dados["current"]["weather_descriptions"][0]

        previsoes = simular_previsao_7_dias(temp_atual)

        for i, temp in enumerate(previsoes):
            data_previsao = datetime.now().date() + timedelta(days=i + 1)
            registros.append((
                cidade,
                data_previsao,
                temp,
                verificar_chuva(descricao),
                classificar_conforto(temp),
                datetime.now()
            ))

    salvar_dados(conn, registros)
    conn.close()


if __name__ == "__main__":
    main()