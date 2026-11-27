
import bcrypt
from conexao_banco import conectar_banco


usuarios = [
    ("admin", "admin123", "admin"),
    ("operador", "operador123", "operador")
]

conexao = conectar_banco()
cursor = conexao.cursor()

for usuario, senha, perfil in usuarios:

    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    )

    sql = """
        INSERT INTO usuarios (usuario, senha_hash, perfil)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        sql,
        (usuario, senha_hash.decode("utf-8"), perfil)
    )

conexao.commit()

print("Usuários cadastrados com sucesso!")

cursor.close()
conexao.close()
