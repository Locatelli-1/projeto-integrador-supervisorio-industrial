import bcrypt
import streamlit as st

from conexao_banco import conectar_banco


# =====================================
# AUTENTICAÇÃO DE USUÁRIOS
# =====================================

def autenticar(usuario, senha, log):

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
            SELECT senha_hash, perfil, status
            FROM usuarios
            WHERE usuario = %s
        """

        cursor.execute(sql, (usuario,))
        dados_usuario = cursor.fetchone()

        if dados_usuario is None:
            log.registrar(
                "WARNING",
                f"Tentativa de login inválida - usuário: {usuario}"
            )
            return False

        senha_hash = dados_usuario[0].encode("utf-8")
        perfil = dados_usuario[1]
        status = dados_usuario[2]

        # Verifica se a conta está ativa
        if status != 1:
            log.registrar(
                "WARNING",
                f"Tentativa de login em conta desativada - usuário: {usuario}"
            )
            return False

        # Verifica a senha utilizando bcrypt
        if bcrypt.checkpw(senha.encode("utf-8"), senha_hash):

            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.perfil = perfil

            log.registrar(
                "INFO",
                f"Login realizado - usuário: {usuario}"
            )

            return True

        else:
            log.registrar(
                "WARNING",
                f"Tentativa de login inválida - usuário: {usuario}"
            )

            return False

    except Exception as erro:

        log.registrar(
            "ERROR",
            f"Erro na autenticação com MySQL: {erro}"
        )

        st.error("Não foi possível consultar o banco de dados.")

        return False

    finally:

        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# =====================================
# ENCERRAR SESSÃO
# =====================================

def logout(log):

    log.registrar(
        "INFO",
        f"Logout realizado - usuário: {st.session_state.usuario}"
    )

    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None

    st.rerun()