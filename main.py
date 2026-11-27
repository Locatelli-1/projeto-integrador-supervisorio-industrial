import pandas as pd

from conexao_banco import criar_engine


def main():
    engine = None

    try:
        engine = criar_engine()

        # Executar consulta SQL e criar DataFrame.
        with engine.connect() as conexao:
            df = pd.read_sql(
                "SELECT * FROM teste_professor",
                con=conexao,
            )

        print(df)

    except Exception as erro:
        print(f"Erro ao consultar o banco de dados: {erro}")

    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()