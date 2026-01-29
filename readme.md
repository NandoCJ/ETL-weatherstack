# README — Script ETL de Dados Meteorológicos

## Requisitos

- Python 3.10 ou superior
- PostgreSQL em execução
- Bibliotecas Python:
  ```bash
  pip install requests psycopg2-binary python-dotenv

# Como executar o script

1. Criar a tabela no PostgreSQL utilizando o arquivo script_sql.sql.

2. Criar e configurar o arquivo .env.

    O arquivo .env deve estar na mesma pasta do codigo.py e conter as seguintes variáveis:

    ```bash
        WEATHERSTACK_API_KEY=SUA_CHAVE_DA_API 
        DB_HOST=localhost
        DB_NAME=clima_db
        DB_USER=postgres
        DB_PASSWORD=SUA_SENHA
        DB_PORT=5432
    
    A chave da API Weatherstack deve ser obtida no site oficial da Weatherstack.

3. Executar o script 
    
    python codigo.py

    O script pode ser executado via terminal (CMD/PowerShell) ou por um editor de código de sua preferência.

# Premissas adotadas no desenvolvimento:
    
    1. A lógica inicial foi prototipada utilizando a plataforma Make. No entanto, essa abordagem exigia o uso de um banco de dados em nuvem. Para simplificar a execução e permitir testes locais, optou-se pela implementação em Python com PostgreSQL local.

    2. Durante o desenvolvimento, foi identificado um limite de requisições da API Weatherstack (erro Too Many Requests). Para contornar essa limitação, foi implementado um atraso (delay) entre as requisições, garantindo a coleta dos dados de todas as capitais.

    3. Embora não fosse obrigatório, o script utiliza dados de clima atual e simula uma previsão de 7 dias com pequenas variações, atendendo ao requisito lógico de processamento por múltiplos dias.