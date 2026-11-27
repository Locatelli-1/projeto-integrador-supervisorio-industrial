import os
from pathlib import Path

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# =====================================
# CARREGAR VARIÁVEIS DO ARQUIVO .ENV
# =====================================

def carregar_variaveis_env():
    caminho_env = Path(__file__).resolve().parent / ".env"

    if not caminho_env.exists():
        return

    with caminho_env.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue

            if "=" not in linha:
                continue

            chave, valor = linha.split("=", 1)

            chave = chave.strip()
            valor = valor.strip()

            if (
                len(valor) >= 2
                and valor[0] == valor[-1]
                and valor[0] in ("'", '"')
            ):
                valor = valor[1:-1]

            if chave:
                os.environ.setdefault(chave, valor)


carregar_variaveis_env()


# =====================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# =====================================

HOST = os.getenv("DB_HOST", "localhost")
USUARIO = os.getenv("DB_USER", "root")
SENHA = os.getenv("DB_PASSWORD", "")
BANCO = os.getenv("DB_NAME", "teste_professor")

try:
    PORTA = int(os.getenv("DB_PORT", "3306"))
except ValueError as erro:
    raise ValueError("DB_PORT deve conter um número válido.") from erro


# =====================================
# VALIDAR CONFIGURAÇÕES
# =====================================

def validar_configuracao():
    if not SENHA:
        raise RuntimeError(
            "Senha do MySQL não configurada. "
            "Configure DB_PASSWORD no arquivo .env."
        )

    if not HOST or not USUARIO or not BANCO:
        raise RuntimeError(
            "Configuração incompleta do MySQL. "
            "Verifique DB_HOST, DB_USER e DB_NAME no .env."
        )


# =====================================
# CONEXÃO MYSQL CONNECTOR
# =====================================

def conectar_banco():
    validar_configuracao()

    conexao = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
        port=PORTA,
    )

    return conexao


# =====================================
# CONEXÃO SQLALCHEMY
# =====================================

def criar_engine():
    validar_configuracao()

    url = URL.create(
        drivername="mysql+pymysql",
        username=USUARIO,
        password=SENHA,
        host=HOST,
        port=PORTA,
        database=BANCO,
    )

    engine = create_engine(url)

    return engine