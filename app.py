import streamlit as st

from classe_gerenciador import GerenciadorLog
from autenticacao import logout
from telas import (
    tela_login,
    tela_processo,
    tela_banco_dados,
    tela_graficos,
    tela_monitoramento,
    tela_cadastro_usuarios
)


# =====================================
# OBJETO DE LOG (AWS CLOUDWATCH)
# =====================================

log = GerenciadorLog()


# =====================================
# VARIÁVEIS DA SESSÃO
# =====================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "perfil" not in st.session_state:
    st.session_state.perfil = None

if "motor_ligado" not in st.session_state:
    st.session_state.motor_ligado = False

if "velocidade" not in st.session_state:
    st.session_state.velocidade = 0

if "velocidade_slider" not in st.session_state:
    st.session_state.velocidade_slider = 0

if "leituras" not in st.session_state:
    st.session_state.leituras = []


# =====================================
# CONTROLE DO SUPERVISÓRIO
# =====================================

if not st.session_state.logado:

    tela_login(log)

else:

    perfil = str(st.session_state.perfil).strip().lower()

    # =================================
    # MENU LATERAL
    # =================================

    st.sidebar.write(
        f"👤 {st.session_state.usuario}"
    )

    st.sidebar.write(
        f"Perfil: {perfil}"
    )

    st.sidebar.divider()

    if perfil == "admin":

        opcoes = [
            "Processo",
            "Acesso ao Banco de Dados",
            "Gráficos",
            "Monitoramento",
            "Cadastro de Usuários"
        ]

    elif perfil == "engenheiro":

        opcoes = [
            "Processo",
            "Acesso ao Banco de Dados",
            "Gráficos",
            "Monitoramento"
        ]

    elif perfil == "operador":

        opcoes = [
            "Processo",
            "Gráficos"
        ]

    else:

        st.error("Perfil de usuário não reconhecido.")
        st.stop()

    tela = st.sidebar.radio(
        "Navegação",
        opcoes
    )

    st.sidebar.divider()

    if st.sidebar.button("Sair"):
        logout(log)

    # =================================
    # TELAS DO PROJETO
    # =================================

    if tela == "Processo":

        tela_processo(log)

    elif tela == "Acesso ao Banco de Dados":

        tela_banco_dados()

    elif tela == "Gráficos":

        tela_graficos()

    elif tela == "Monitoramento":

        tela_monitoramento(log)

    elif tela == "Cadastro de Usuários":

        tela_cadastro_usuarios(log)