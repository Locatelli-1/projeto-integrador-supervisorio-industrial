import json
import os
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from sqlalchemy import text

from autenticacao import autenticar
from conexao_banco import conectar_banco, criar_engine
from Classe_OPC import Conexao_Opc


# =====================================
# IDENTIDADE VISUAL INDUSTRIAL
# =====================================

def aplicar_estilo():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }

        html, body, .stApp,
        [data-testid="stAppViewContainer"] {
            background: #07111f !important;
            color: #e7eef8 !important;
        }

        [data-testid="stHeader"] {
            background: rgba(7, 17, 31, 0.95) !important;
        }

        [data-testid="stMainBlockContainer"],
        .main .block-container {
            max-width: 1500px;
            padding: 2.5rem 4rem 3rem;
        }

        h1, h2, h3, h4 {
            color: #f4f7fc !important;
            letter-spacing: -0.5px;
        }

        .stApp p, .stApp label, .stApp span {
            color: #dce6f2;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0c1b2d, #081422) !important;
            border-right: 1px solid #20354c;
        }

        [data-testid="stSidebar"] * {
            color: #dce6f2 !important;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(145deg, #10243a, #0b1a2b) !important;
            border: 1px solid #263f59 !important;
            border-radius: 13px;
            padding: 20px;
        }

        [data-testid="stMetricLabel"] {
            color: #91a9c2 !important;
            font-size: 13px !important;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #25d8cd !important;
            font-size: 30px !important;
            font-weight: 750;
        }

        [data-baseweb="input"],
        [data-baseweb="textarea"] {
            background: #0a1929 !important;
            border: 1px solid #29435d !important;
            border-radius: 9px !important;
        }

        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea {
            background: transparent !important;
            color: #f1f5f9 !important;
        }

        [data-baseweb="select"] > div {
            background: #0a1929 !important;
            border-color: #29435d !important;
            color: #f1f5f9 !important;
        }

        .stButton > button {
            background: #12263c !important;
            color: #e8f2fc !important;
            border: 1px solid #31506c !important;
            border-radius: 9px !important;
            min-height: 43px;
            font-weight: 650;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #20d8ce !important;
            color: #20d8ce !important;
            background: #17334b !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(110deg, #00bdb3, #13d7cc) !important;
            border: none !important;
            color: #061721 !important;
            font-weight: 800;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #0c1b2b !important;
            border: 1px solid #263c53 !important;
            border-radius: 14px !important;
        }

        [data-testid="stExpander"] {
            background: #0c1b2b !important;
            border: 1px solid #29435d !important;
            border-radius: 10px !important;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #263c53;
            border-radius: 10px;
            overflow: hidden;
        }

        hr {
            border-color: #253b52 !important;
        }

        .hero {
            background: linear-gradient(115deg, #10243a 0%, #153a55 60%, #075b60 100%);
            border: 1px solid #28526a;
            border-radius: 16px;
            padding: 30px 32px;
            margin-bottom: 27px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
        }

        .hero-label {
            color: #46d8d0;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2.5px;
            margin-bottom: 12px;
        }

        .hero-title {
            color: #ffffff;
            font-size: 31px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .hero-description {
            color: #bdcede;
            font-size: 14px;
        }

        .section-label {
            color: #41d2ca;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }

        .login-brand {
            min-height: 430px;
            padding: 35px 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .brand-mark {
            font-size: 48px;
            margin-bottom: 24px;
        }

        .brand-eyebrow {
            color: #2ed8ce;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 3px;
        }

        .brand-title {
            color: #ffffff;
            font-size: clamp(32px, 4vw, 52px);
            line-height: 1.12;
            font-weight: 850;
            margin: 15px 0;
        }

        .brand-description {
            color: #9cb1c8;
            font-size: 15px;
            line-height: 1.8;
            max-width: 520px;
        }

        .brand-status {
            display: inline-block;
            margin-top: 28px;
            padding: 9px 14px;
            border: 1px solid #245c61;
            border-radius: 30px;
            background: #0d3037;
            color: #4fe0c9;
            font-size: 12px;
            width: fit-content;
        }

        .login-footer {
            color: #6f869e;
            font-size: 11px;
            text-align: center;
            margin-top: 24px;
            letter-spacing: 1px;
        }

        @media (max-width: 800px) {
            [data-testid="stMainBlockContainer"],
            .main .block-container {
                padding: 1.2rem 1rem;
            }

            .hero-title {
                font-size: 24px;
            }

            .login-brand {
                min-height: auto;
                padding: 10px 5px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================
# CABEÇALHO DAS TELAS
# =====================================

def cabecalho(titulo, descricao, secao):
    st.html(
        f"""
        <div class="hero">
            <div class="hero-label">
                SUPERVISORY INDUSTRIAL &nbsp; / &nbsp; {secao}
            </div>
            <div class="hero-title">{titulo}</div>
            <div class="hero-description">{descricao}</div>
        </div>
        """
    )


# =====================================
# TELA DE LOGIN
# =====================================

def tela_login(log):
    aplicar_estilo()
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.85], gap="large")

    with col1:
        st.html(
            """
            <div class="login-brand">
                <div class="brand-mark">⚙️</div>
                <div class="brand-eyebrow">INDUSTRIAL CONTROL SYSTEM</div>
                <div class="brand-title">SUPERVISORY<br>INDUSTRIAL</div>
                <div class="brand-description">
                    Plataforma de supervisão e controle de processos industriais,
                    com acompanhamento operacional, monitoramento de variáveis
                    e gerenciamento de eventos.
                </div>
                <div class="brand-status">● AMBIENTE DE SIMULAÇÃO ATIVO</div>
            </div>
            """
        )

    with col2:
        with st.container(border=True):
            st.html('<div class="section-label">ACESSO AO SISTEMA</div>')
            st.subheader("Autenticação")
            st.caption("Entre com suas credenciais de acesso.")
            st.divider()

            usuario = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário",
            )
            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
            )

            if st.button(
                "Entrar no sistema  →",
                use_container_width=True,
                type="primary",
            ):
                if autenticar(usuario, senha, log):
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")

            st.divider()

            with st.expander("Informações sobre os perfis"):
                st.write("**Administrador:** acesso às telas administrativas e operacionais.")
                st.write("**Operador:** acesso ao processo e aos gráficos.")
                st.write("**Engenheiro:** acesso às telas permitidas pelo perfil.")

            st.html(
                """
                <div class="login-footer">
                    SISTEMA SUPERVISÓRIO INDUSTRIAL<br>
                    PROJETO INTEGRADOR
                </div>
                """
            )


# =====================================
# COMUNICAÇÃO OPC UA COM O SIMULADOR
# =====================================

URL_OPC = os.getenv(
    "OPC_UA_URL",
    "opc.tcp://10.211.55.3:4843",
)

NODE_START = "ns=1;s=Main.Start"
NODE_SENSOR = "ns=1;s=Main.Sensor"
NODE_MOTOR = "ns=1;s=Main.Motor"
NODE_VELOCIDADE = "ns=1;s=Main.Velocidade"


def obter_conexao_opc():
    """
    Reutiliza a classe Conexao_Opc fornecida pelo professor.
    A classe abre e fecha a conexão a cada leitura/escrita.
    """
    if (
        "opc" not in st.session_state
        or st.session_state.get("opc_url") != URL_OPC
    ):
        st.session_state.opc = Conexao_Opc(URL_OPC)
        st.session_state.opc_url = URL_OPC

    return st.session_state.opc


# =====================================
# REGISTRAR LEITURAS REAIS NO MYSQL
# =====================================

def registrar_leitura_sensor(sensor, valor, unidade, equipamento="Esteira 01"):
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO leituras_sensores (
                equipamento, sensor, valor, unidade
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (equipamento, sensor, valor, unidade),
        )

        conexao.commit()
        return True

    except Exception:
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# =====================================
# MONITORAMENTO REAL DO PROCESSO
# =====================================

@st.fragment(run_every=2)
def monitorar_processo_opc(log):
    """Lê as variáveis reais do CLP, registra eventos e apresenta alertas."""
    try:
        opc = obter_conexao_opc()

        start = opc.leitura_valor(NODE_START)
        sensor = opc.leitura_valor(NODE_SENSOR)
        motor = opc.leitura_valor(NODE_MOTOR)
        velocidade = opc.leitura_valor(NODE_VELOCIDADE)

        if any(valor is None for valor in (start, sensor, motor, velocidade)):
            raise RuntimeError("O CLP não retornou todas as variáveis esperadas.")

        leitura_atual = {
            "start": bool(start),
            "sensor": bool(sensor),
            "motor": bool(motor),
            "velocidade": float(velocidade),
            "data_hora": datetime.now(),
        }
        leitura_anterior = st.session_state.get("opc_ultima_leitura")

        # Registra cada mudança uma única vez, comparando com a leitura anterior.
        if leitura_anterior is not None:
            if leitura_atual["motor"] != leitura_anterior["motor"]:
                estado = "LIGADA" if leitura_atual["motor"] else "DESLIGADA"
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"Estado da esteira alterado para {estado}",
                )

            if leitura_atual["sensor"] != leitura_anterior["sensor"]:
                estado_sensor = (
                    "Caixa detectada" if leitura_atual["sensor"] else "Sensor livre"
                )
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"Sensor de presença: {estado_sensor}",
                )

            if leitura_atual["start"] != leitura_anterior["start"]:
                estado_start = "iniciado" if leitura_atual["start"] else "parado"
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"Processo {estado_start} pelo comando de partida",
                )

            if abs(leitura_atual["velocidade"] - leitura_anterior["velocidade"]) >= 0.001:
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"Velocidade alterada para {leitura_atual['velocidade']:.2f} m/s",
                )

        # Histórico curto para visualização em tempo real.
        if "leituras_processo" not in st.session_state:
            st.session_state.leituras_processo = []

        st.session_state.leituras_processo.append({
            "Horário": leitura_atual["data_hora"].strftime("%H:%M:%S"),
            "Velocidade (m/s)": round(leitura_atual["velocidade"], 3),
        })
        st.session_state.leituras_processo = st.session_state.leituras_processo[-30:]

        # Persiste as variáveis a cada 10 segundos e sempre que houver mudança.
        agora = datetime.now()
        ultima_gravacao = st.session_state.get("opc_ultima_gravacao")

        houve_mudanca = (
            leitura_anterior is None
            or leitura_atual["motor"] != leitura_anterior["motor"]
            or leitura_atual["sensor"] != leitura_anterior["sensor"]
            or leitura_atual["start"] != leitura_anterior["start"]
            or abs(leitura_atual["velocidade"] - leitura_anterior["velocidade"]) >= 0.001
        )

        intervalo_vencido = (
            ultima_gravacao is None
            or (agora - ultima_gravacao).total_seconds() >= 10
        )

        if houve_mudanca or intervalo_vencido:
            resultados = [
                registrar_leitura_sensor(
                    "Estado do motor", int(leitura_atual["motor"]), "BOOL"
                ),
                registrar_leitura_sensor(
                    "Sensor de presença", int(leitura_atual["sensor"]), "BOOL"
                ),
                registrar_leitura_sensor(
                    "Comando de partida", int(leitura_atual["start"]), "BOOL"
                ),
                registrar_leitura_sensor(
                    "Velocidade da esteira", leitura_atual["velocidade"], "m/s"
                ),
            ]

            if all(resultados):
                st.session_state.opc_ultima_gravacao = agora
            else:
                st.warning("Uma ou mais leituras do CLP não foram gravadas no MySQL.")

        # Alertas baseados somente nos sinais disponíveis no CLP.
        alertas_atuais = []

        if leitura_atual["start"] and not leitura_atual["motor"]:
            alertas_atuais.append(
                "Comando de partida ativo, mas o motor não confirmou funcionamento."
            )

        if leitura_atual["motor"] and leitura_atual["velocidade"] <= 0:
            alertas_atuais.append("Motor ligado sem velocidade configurada.")

        if leitura_atual["sensor"] and not leitura_atual["motor"]:
            alertas_atuais.append(
                "Caixa detectada com a esteira parada. Verifique o processo."
            )

        alertas_anteriores = st.session_state.get("opc_alertas_ativos", [])

        for alerta in alertas_atuais:
            if alerta not in alertas_anteriores:
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"ALERTA: {alerta}",
                    nivel="WARNING",
                )

        for alerta in alertas_anteriores:
            if alerta not in alertas_atuais:
                log.registrar_evento_processo(
                    "Esteira 01",
                    f"Alerta normalizado: {alerta}",
                )

        st.session_state.opc_alertas_ativos = alertas_atuais

        # Registra a recuperação da comunicação OPC UA.
        if st.session_state.get("opc_ultimo_erro"):
            log.registrar_evento_processo(
                "Esteira 01",
                "Comunicação OPC UA restabelecida com o CLP",
            )
            st.session_state.opc_ultimo_erro = None

        # Guarda a leitura atual depois de comparar e registrar transições.
        st.session_state.opc_ultima_leitura = leitura_atual

        # Indicadores operacionais.
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Estado da esteira", "LIGADA" if leitura_atual["motor"] else "PARADA")

        with col2:
            st.metric(
                "Sensor de presença",
                "CAIXA DETECTADA" if leitura_atual["sensor"] else "LIVRE",
            )

        with col3:
            st.metric("Velocidade", f"{leitura_atual['velocidade']:.2f} m/s")

        with col4:
            st.metric("Comando de partida", "ATIVO" if leitura_atual["start"] else "INATIVO")

        # Representação didática da esteira, caixa e sensor com HTML/CSS.
        classe_esteira = "running" if leitura_atual["motor"] else "stopped"
        classe_sensor = "detected" if leitura_atual["sensor"] else "free"
        classe_caixa = "box-visible" if leitura_atual["sensor"] else "box-hidden"

        visual = f"""
        <style>
        .planta-processo {{
            background: #10243a; border: 1px solid #31506c;
            border-radius: 12px; padding: 22px; color: #e8f2fc; margin: 12px 0;
        }}
        .planta-titulo {{ font-size: 15px; font-weight: 750; margin-bottom: 18px; }}
        .linha-planta {{ display: flex; align-items: center; gap: 18px; }}
        .motor-planta {{ background: #1c3852; border: 2px solid #63809d;
            border-radius: 10px; padding: 15px 12px; text-align: center; min-width: 88px; }}
        .esteira-planta {{ flex: 1; min-width: 120px; height: 65px; position: relative;
            border: 6px solid #8193a5; border-radius: 9px; background: #18202a; overflow: hidden; }}
        .esteira-superficie {{ height: 100%; background: repeating-linear-gradient(
            90deg, #34495b 0px, #34495b 12px, #1e2e3e 12px, #1e2e3e 24px); }}
        .esteira-planta.running .esteira-superficie {{ animation: movimentoEsteira .6s linear infinite; }}
        .caixa-planta {{ position: absolute; width: 27px; height: 27px; top: 13px;
            left: 12%; background: #d99b4a; border: 2px solid #f4c47d; border-radius: 3px; }}
        .caixa-planta.box-hidden {{ display: none; }}
        .esteira-planta.running .caixa-planta.box-visible {{ animation: movimentoCaixa 4s linear infinite; }}
        .sensor-planta {{ min-width: 90px; text-align: center; font-size: 12px; }}
        .lampada-planta {{ display: inline-block; width: 14px; height: 14px;
            border-radius: 50%; margin-right: 6px; background: #16b981; box-shadow: 0 0 8px #16b981; }}
        .lampada-planta.detected {{ background: #ef4444; box-shadow: 0 0 9px #ef4444; }}
        .planta-legenda {{ margin-top: 17px; color: #a9bdd1; font-size: 12px; }}
        @keyframes movimentoEsteira {{ from {{ background-position: 0 0; }} to {{ background-position: 24px 0; }} }}
        @keyframes movimentoCaixa {{ from {{ left: 12%; }} to {{ left: 85%; }} }}
        @media (max-width: 600px) {{ .linha-planta {{ gap: 8px; }} .motor-planta, .sensor-planta {{ min-width: 65px; font-size: 10px; }} }}
        </style>
        <div class="planta-processo">
            <div class="planta-titulo">REPRESENTAÇÃO DO PROCESSO INDUSTRIAL — ESTEIRA 01</div>
            <div class="linha-planta">
                <div class="motor-planta">⚙️<br>MOTOR</div>
                <div class="esteira-planta {classe_esteira}">
                    <div class="esteira-superficie"></div>
                    <div class="caixa-planta {classe_caixa}"></div>
                </div>
                <div class="sensor-planta">
                    <span class="lampada-planta {classe_sensor}"></span><br>SENSOR
                </div>
            </div>
            <div class="planta-legenda">
                Estados e animação associados às leituras recebidas pelo CLP via OPC UA.
            </div>
        </div>
        """

        st.html(visual)

        # Área de alertas operacionais.
        st.subheader("Alertas do processo")

        if alertas_atuais:
            for alerta in alertas_atuais:
                st.warning(alerta)
        elif leitura_atual["motor"]:
            st.success("Esteira em operação. Nenhum alerta ativo.")
        else:
            st.info("Esteira parada. Nenhuma condição de alerta identificada.")

        st.caption("Leituras do CLP atualizadas automaticamente a cada 2 segundos.")

        historico = pd.DataFrame(st.session_state.leituras_processo)

        if not historico.empty:
            st.line_chart(
                historico,
                x="Horário",
                y="Velocidade (m/s)",
                x_label="Horário",
                y_label="Velocidade (m/s)",
            )

    except Exception as erro:
        mensagem_erro = str(erro)

        if st.session_state.get("opc_ultimo_erro") != mensagem_erro:
            log.registrar(
                "ERROR",
                f"Falha na comunicação OPC UA com o CLP: {mensagem_erro}",
            )
            log.registrar_evento_processo(
                "Esteira 01",
                f"Falha na comunicação OPC UA com o CLP: {mensagem_erro}",
                nivel="ERROR",
            )
            st.session_state.opc_ultimo_erro = mensagem_erro

        st.error(
            "Não foi possível comunicar com o CLP pelo OPC UA. "
            "Verifique se o simulador está em execução e se o servidor OPC UA está habilitado."
        )
        st.warning("ALERTA: comunicação com o processo industrial interrompida.")
        st.caption(f"Detalhe técnico: {mensagem_erro}")


# =====================================
# TELA DO PROCESSO
# =====================================

def tela_processo(log):
    aplicar_estilo()

    cabecalho(
        "Controle do Processo",
        "Supervisão e controle da esteira transportadora via OPC UA.",
        "PROCESSO",
    )

    st.html('<div class="section-label">MONITORAMENTO DO CLP</div>')

    with st.container(border=True):
        monitorar_processo_opc(log)

    leitura = st.session_state.get("opc_ultima_leitura", {})
    velocidade_atual = float(leitura.get("velocidade", 0.5))

    st.divider()
    st.html('<div class="section-label">PAINEL DE COMANDOS</div>')

    with st.container(border=True):
        st.subheader("Esteira 01 — Comandos operacionais")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🟢 Ligar esteira",
                use_container_width=True,
                type="primary",
            ):
                try:
                    opc = obter_conexao_opc()
                    sucesso = opc.escrita_bool(NODE_START, True)

                    if sucesso:
                        log.registrar(
                            "INFO",
                            f"{st.session_state.usuario} enviou comando para ligar a Esteira 01.",
                        )
                        st.success("Comando de partida enviado ao CLP.")
                        st.rerun()
                    else:
                        st.error("O CLP não confirmou o envio do comando.")

                except Exception as erro:
                    log.registrar(
                        "ERROR",
                        f"Falha ao ligar a Esteira 01 via OPC UA: {erro}",
                    )
                    st.error(f"Erro na comunicação OPC UA: {erro}")

        with col2:
            if st.button(
                "🔴 Desligar esteira",
                use_container_width=True,
            ):
                try:
                    opc = obter_conexao_opc()
                    sucesso = opc.escrita_bool(NODE_START, False)

                    if sucesso:
                        log.registrar(
                            "INFO",
                            f"{st.session_state.usuario} enviou comando para desligar a Esteira 01.",
                        )
                        st.success("Comando de parada enviado ao CLP.")
                        st.rerun()
                    else:
                        st.error("O CLP não confirmou o envio do comando.")

                except Exception as erro:
                    log.registrar(
                        "ERROR",
                        f"Falha ao desligar a Esteira 01 via OPC UA: {erro}",
                    )
                    st.error(f"Erro na comunicação OPC UA: {erro}")

        st.divider()
        st.subheader("Ajuste de velocidade da esteira")

        st.caption(
            "O valor é enviado ao CLP como REAL, em metros por segundo. "
            "O valor atual vem da variável Main.Velocidade."
        )

        with st.form("form_velocidade_esteira"):
            velocidade_desejada = st.number_input(
                "Velocidade desejada (m/s)",
                min_value=0.0,
                value=max(0.0, velocidade_atual),
                step=0.1,
                format="%.2f",
            )

            enviar_velocidade = st.form_submit_button(
                "Aplicar velocidade",
                use_container_width=True,
                type="primary",
            )

        if enviar_velocidade:
            try:
                opc = obter_conexao_opc()
                sucesso = opc.escrita_float(
                    NODE_VELOCIDADE,
                    float(velocidade_desejada),
                )

                if sucesso:
                    log.registrar(
                        "INFO",
                        (
                            f"{st.session_state.usuario} enviou ajuste de "
                            f"velocidade da Esteira 01 para "
                            f"{velocidade_desejada:.2f} m/s."
                        ),
                    )
                    st.success("Ajuste de velocidade enviado ao CLP.")
                    st.rerun()
                else:
                    st.error("Não foi possível enviar o ajuste ao CLP.")

            except Exception as erro:
                log.registrar(
                    "ERROR",
                    f"Falha ao ajustar velocidade da Esteira 01 via OPC UA: {erro}",
                )
                st.error(
                    "O servidor OPC UA não aceitou o ajuste de velocidade. "
                    f"Detalhe: {erro}"
                )

    st.caption(
        "O processo é executado no Open Industry Project. "
        "O supervisório envia comandos e recebe as variáveis do CLP "
        "pela conexão OPC UA."
    )


# =====================================
# TELA DE ACESSO AO BANCO DE DADOS
# =====================================

def tela_banco_dados():
    aplicar_estilo()

    cabecalho(
        "Acesso ao Banco de Dados",
        "Consulta dos registros de eventos armazenados no MySQL.",
        "BANCO DE DADOS",
    )

    st.caption(
        "Esta consulta exibe somente eventos operacionais associados aos equipamentos. "
        "Eventos de login, segurança e atividades administrativas ficam no AWS CloudWatch."
    )

    engine = None

    try:
        engine = criar_engine()

        with engine.connect() as conexao:
            resultado = conexao.execute(
                text(
                    """
                    SELECT MIN(data_hora), MAX(data_hora)
                    FROM eventos
                    WHERE equipamento IS NOT NULL
                      AND equipamento <> 'Sistema'
                    """
                )
            ).one()

            primeira_data, ultima_data = resultado

            if primeira_data is None or ultima_data is None:
                st.info("Ainda não existem eventos registrados no banco de dados.")
                return

            equipamentos = pd.read_sql_query(
                text(
                    """
                    SELECT DISTINCT equipamento
                    FROM eventos
                    WHERE equipamento IS NOT NULL
                      AND equipamento <> 'Sistema'
                    ORDER BY equipamento
                    """
                ),
                con=conexao,
            )["equipamento"].dropna().tolist()

            usuarios = pd.read_sql_query(
                text(
                    """
                    SELECT DISTINCT usuario
                    FROM eventos
                    WHERE usuario IS NOT NULL
                      AND equipamento IS NOT NULL
                      AND equipamento <> 'Sistema'
                    ORDER BY usuario
                    """
                ),
                con=conexao,
            )["usuario"].dropna().tolist()

            st.html('<div class="section-label">FILTROS DE CONSULTA</div>')

            col1, col2 = st.columns(2)

            with col1:
                equipamento = st.selectbox("Equipamento", ["Todos"] + equipamentos)

            with col2:
                usuario = st.selectbox("Usuário", ["Todos"] + usuarios)

            col3, col4 = st.columns(2)

            with col3:
                data_inicial = st.date_input(
                    "Data inicial",
                    value=primeira_data.date(),
                    min_value=primeira_data.date(),
                    max_value=ultima_data.date(),
                )

            with col4:
                data_final = st.date_input(
                    "Data final",
                    value=ultima_data.date(),
                    min_value=primeira_data.date(),
                    max_value=ultima_data.date(),
                )

            evento = st.text_input(
                "Pesquisar evento",
                placeholder="Digite uma palavra ou trecho do evento",
            )

            st.divider()

            if data_inicial > data_final:
                st.warning("A data inicial não pode ser posterior à data final.")
                return

            sql = """
                SELECT
                    data_hora AS 'Data e hora',
                    equipamento AS 'Equipamento',
                    evento AS 'Evento',
                    usuario AS 'Usuário',
                    nivel AS 'Nível'
                FROM eventos
                WHERE equipamento IS NOT NULL
                  AND equipamento <> 'Sistema'
                  AND data_hora >= :inicio
                  AND data_hora < :fim
            """

            parametros = {
                "inicio": datetime.combine(data_inicial, datetime.min.time()),
                "fim": datetime.combine(
                    data_final + timedelta(days=1),
                    datetime.min.time(),
                ),
            }

            if equipamento != "Todos":
                sql += " AND equipamento = :equipamento"
                parametros["equipamento"] = equipamento

            if usuario != "Todos":
                sql += " AND usuario = :usuario"
                parametros["usuario"] = usuario

            if evento.strip():
                sql += " AND evento LIKE :evento"
                parametros["evento"] = f"%{evento.strip()}%"

            sql += " ORDER BY data_hora DESC"

            dados = pd.read_sql_query(
                text(sql),
                con=conexao,
                params=parametros,
            )

            st.html('<div class="section-label">RESULTADO DA CONSULTA</div>')

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Registros encontrados", len(dados))

            with col2:
                total_equipamentos = dados["Equipamento"].nunique() if not dados.empty else 0
                st.metric("Equipamentos", total_equipamentos)

            with col3:
                total_usuarios = dados["Usuário"].nunique() if not dados.empty else 0
                st.metric("Usuários", total_usuarios)

            if dados.empty:
                st.info("Nenhum registro encontrado com os filtros selecionados.")
            else:
                st.dataframe(
                    dados,
                    use_container_width=True,
                    hide_index=True,
                )

    except Exception:
        st.error(
            "Não foi possível consultar os registros do MySQL. "
            "Verifique a conexão e a estrutura da tabela eventos."
        )

    finally:
        if engine is not None:
            engine.dispose()


def formatar_tempo(segundos):
    """Formata uma duração em HH:MM:SS."""
    segundos = max(0, int(segundos))
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def calcular_indicadores_motor(estado_motor, intervalo_maximo_segundos=15):
    """Calcula tempo observado ligado e acionamentos pelas transições BOOL."""
    if estado_motor.empty:
        return (
            0,
            0,
            pd.DataFrame(columns=["dia", "Tempo ligado (minutos)"]),
            pd.DataFrame(columns=["dia", "Acionamentos"]),
        )

    dados = estado_motor[["data_hora", "valor_numerico"]].copy()
    dados = dados.dropna().sort_values("data_hora").reset_index(drop=True)

    if dados.empty:
        return (
            0,
            0,
            pd.DataFrame(columns=["dia", "Tempo ligado (minutos)"]),
            pd.DataFrame(columns=["dia", "Acionamentos"]),
        )

    dados["estado"] = (dados["valor_numerico"] >= 1).astype(int)
    dados["estado_anterior"] = dados["estado"].shift(1)

    dados["acionamento"] = (
        (dados["estado"] == 1) & (dados["estado_anterior"] == 0)
    )

    acionamentos = int(dados["acionamento"].sum())

    dados["proxima_data"] = dados["data_hora"].shift(-1)
    dados["proximo_estado"] = dados["estado"].shift(-1)

    dados["intervalo_segundos"] = (
        dados["proxima_data"] - dados["data_hora"]
    ).dt.total_seconds()

    intervalos_validos = dados[
        (dados["estado"] == 1)
        & (dados["proximo_estado"] == 1)
        & (dados["intervalo_segundos"] > 0)
        & (dados["intervalo_segundos"] <= intervalo_maximo_segundos)
    ].copy()

    intervalos_fechamento = dados[
        (dados["estado"] == 1)
        & (dados["proximo_estado"] == 0)
        & (dados["intervalo_segundos"] > 0)
        & (dados["intervalo_segundos"] <= intervalo_maximo_segundos)
    ].copy()

    intervalos = pd.concat(
        [intervalos_validos, intervalos_fechamento],
        ignore_index=True,
    )

    tempo_total = (
        float(intervalos["intervalo_segundos"].sum())
        if not intervalos.empty
        else 0.0
    )

    if intervalos.empty:
        tempo_por_dia = pd.DataFrame(
            columns=["dia", "Tempo ligado (minutos)"]
        )
    else:
        intervalos["dia"] = intervalos["data_hora"].dt.date

        tempo_por_dia = (
            intervalos.groupby("dia")["intervalo_segundos"]
            .sum()
            .div(60)
            .reset_index(name="Tempo ligado (minutos)")
        )

    if dados[dados["acionamento"]].empty:
        acionamentos_por_dia = pd.DataFrame(
            columns=["dia", "Acionamentos"]
        )
    else:
        iniciados = dados[dados["acionamento"]].copy()
        iniciados["dia"] = iniciados["data_hora"].dt.date

        acionamentos_por_dia = (
            iniciados.groupby("dia")
            .size()
            .reset_index(name="Acionamentos")
        )

    return tempo_total, acionamentos, tempo_por_dia, acionamentos_por_dia


# =====================================
# TELA DE GRÁFICOS E INDICADORES
# =====================================

def tela_graficos():
    aplicar_estilo()

    cabecalho(
        "Gráficos e Indicadores",
        "Histórico das variáveis reais recebidas do CLP pelo OPC UA.",
        "GRÁFICOS",
    )

    st.html('<div class="section-label">PERÍODO DE ANÁLISE</div>')

    periodo = st.selectbox(
        "Selecione o período dos registros",
        [
            "Últimas 24 horas",
            "Últimos 7 dias",
            "Últimos 30 dias",
            "Todo o histórico",
        ],
        index=2,
        key="periodo_graficos_opc",
    )

    if periodo == "Últimas 24 horas":
        inicio = datetime.now() - timedelta(hours=24)
    elif periodo == "Últimos 7 dias":
        inicio = datetime.now() - timedelta(days=7)
    elif periodo == "Últimos 30 dias":
        inicio = datetime.now() - timedelta(days=30)
    else:
        inicio = None

    engine = None

    try:
        engine = criar_engine()

        with engine.connect() as conexao:
            if inicio is None:
                filtro_sql = ""
                parametros = {}
            else:
                filtro_sql = "WHERE data_hora >= :inicio"
                parametros = {"inicio": inicio}

            sensores = pd.read_sql_query(
                text(
                    f"""
                    SELECT data_hora, equipamento, sensor, valor, unidade
                    FROM leituras_sensores
                    {filtro_sql}
                    ORDER BY data_hora ASC
                    """
                ),
                con=conexao,
                params=parametros,
            )

            eventos = pd.read_sql_query(
                text(
                    f"""
                    SELECT data_hora, equipamento, evento, usuario, nivel
                    FROM eventos
                    WHERE equipamento IS NOT NULL
                      AND equipamento <> 'Sistema'
                      {f"AND data_hora >= :inicio" if inicio is not None else ""}
                    ORDER BY data_hora ASC
                    """
                ),
                con=conexao,
                params=parametros,
            )

        if not sensores.empty:
            sensores["data_hora"] = pd.to_datetime(
                sensores["data_hora"], errors="coerce"
            )

            sensores["valor_numerico"] = pd.to_numeric(
                sensores["valor"], errors="coerce"
            )

            sensores["sensor_normalizado"] = (
                sensores["sensor"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.casefold()
            )
        else:
            sensores["valor_numerico"] = pd.Series(dtype="float64")
            sensores["sensor_normalizado"] = pd.Series(dtype="object")

        if not eventos.empty:
            eventos["data_hora"] = pd.to_datetime(
                eventos["data_hora"], errors="coerce"
            )

            eventos["evento_texto"] = (
                eventos["evento"].fillna("").astype(str)
            )

            eventos["evento_normalizado"] = (
                eventos["evento_texto"].str.casefold()
            )
        else:
            eventos["evento_texto"] = pd.Series(dtype="object")
            eventos["evento_normalizado"] = pd.Series(dtype="object")

        velocidade = sensores[
            sensores["sensor_normalizado"].str.contains(
                "velocidade da esteira", regex=False, na=False
            )
            & sensores["unidade"].fillna("").astype(str).str.strip().str.casefold().eq("m/s")
        ].copy()

        estado_motor = sensores[
            sensores["sensor_normalizado"].str.contains(
                "estado do motor", regex=False, na=False
            )
        ].copy()

        estado_sensor = sensores[
            sensores["sensor_normalizado"].str.contains(
                "sensor de presença", regex=False, na=False
            )
            | sensores["sensor_normalizado"].str.contains(
                "sensor de presenca", regex=False, na=False
            )
        ].copy()

        velocidade = velocidade.dropna(
            subset=["data_hora", "valor_numerico"]
        )

        estado_motor = estado_motor.dropna(
            subset=["data_hora", "valor_numerico"]
        )

        estado_sensor = estado_sensor.dropna(
            subset=["data_hora", "valor_numerico"]
        )

        eventos_caixa = eventos[
            eventos["evento_normalizado"].str.contains(
                "caixa detectada", regex=False, na=False
            )
        ].copy()

        leituras_opc = (
            len(velocidade) + len(estado_motor) + len(estado_sensor)
        )

        (
            tempo_funcionamento_seg,
            total_acionamentos,
            tempo_por_dia,
            acionamentos_por_dia,
        ) = calcular_indicadores_motor(estado_motor)

        velocidade_atual = (
            float(velocidade.iloc[-1]["valor_numerico"])
            if not velocidade.empty
            else None
        )

        motor_atual = (
            "LIGADA"
            if not estado_motor.empty
            and int(estado_motor.iloc[-1]["valor_numerico"]) == 1
            else "PARADA"
            if not estado_motor.empty
            else "SEM DADOS"
        )

        sensor_atual = (
            "CAIXA DETECTADA"
            if not estado_sensor.empty
            and int(estado_sensor.iloc[-1]["valor_numerico"]) == 1
            else "LIVRE"
            if not estado_sensor.empty
            else "SEM DADOS"
        )

        st.divider()
        st.html('<div class="section-label">RESUMO DO PROCESSO</div>')

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.metric("Leituras reais do CLP", leituras_opc)

        with col2:
            st.metric("Estado da esteira", motor_atual)

        with col3:
            st.metric("Sensor de presença", sensor_atual)

        with col4:
            st.metric(
                "Velocidade atual",
                f"{velocidade_atual:.2f} m/s"
                if velocidade_atual is not None
                else "SEM DADOS",
            )

        with col5:
            st.metric(
                "Tempo ligado observado",
                formatar_tempo(tempo_funcionamento_seg),
            )

        with col6:
            st.metric("Acionamentos", total_acionamentos)

        st.caption(
            "Os registros operacionais são consultados separadamente dos logs de autenticação e segurança, que permanecem no AWS CloudWatch. "
            "Os indicadores acima utilizam somente os registros identificados "
            "como Estado do motor, Sensor de presença e Velocidade da esteira. "
            "Os registros antigos de temperatura e RPM não entram nesses indicadores."
        )

        # VELOCIDADE REAL DA ESTEIRA
        st.divider()
        st.subheader("Velocidade da esteira ao longo do tempo")

        if not velocidade.empty:
            dados_grafico = (
                velocidade[["data_hora", "valor_numerico"]]
                .dropna()
                .sort_values("data_hora")
            )

            maior_valor = float(dados_grafico["valor_numerico"].max())
            limite_superior = max(0.6, maior_valor * 1.2)

            especificacao_grafico = {
                "mark": {
                    "type": "line",
                    "point": True,
                    "strokeWidth": 3,
                },
                "height": 350,
                "encoding": {
                    "x": {
                        "field": "data_hora",
                        "type": "temporal",
                        "title": "Data e hora",
                    },
                    "y": {
                        "field": "valor_numerico",
                        "type": "quantitative",
                        "title": "Velocidade (m/s)",
                        "scale": {
                            "domain": [0, limite_superior],
                            "nice": False,
                        },
                    },
                    "tooltip": [
                        {
                            "field": "data_hora",
                            "type": "temporal",
                            "title": "Data e hora",
                        },
                        {
                            "field": "valor_numerico",
                            "type": "quantitative",
                            "title": "Velocidade (m/s)",
                            "format": ".2f",
                        },
                    ],
                },
            }

            st.vega_lite_chart(
                dados_grafico,
                spec=especificacao_grafico,
                use_container_width=True,
            )

            st.caption(
                "Dados reais recebidos da variável Main.Velocidade via OPC UA. "
                "A escala vertical começa em zero."
            )
        else:
            st.info(
                "Ainda não existem leituras de velocidade da esteira no período. "
                "Abra a tela Processo e mantenha o monitoramento ativo para gerar o histórico."
            )

        # ESTADO DO MOTOR / ESTEIRA
        st.divider()
        st.subheader("Estado da esteira ao longo do tempo")

        if not estado_motor.empty:
            estado_motor["estado"] = estado_motor["valor_numerico"].apply(
                lambda valor: 1 if valor >= 1 else 0
            )

            st.line_chart(
                estado_motor,
                x="data_hora",
                y="estado",
                x_label="Data e hora",
                y_label="Estado (0 = parada, 1 = ligada)",
            )

            st.caption(
                "0 = parada | 1 = ligada. Dados registrados a partir da variável Main.Motor."
            )
        else:
            st.info(
                "Ainda não existem registros do estado do motor/esteira no período."
            )

        # SENSOR DE PRESENÇA
        st.divider()
        st.subheader("Detecção de caixas pelo sensor")

        if not estado_sensor.empty:
            estado_sensor["deteccao"] = estado_sensor["valor_numerico"].apply(
                lambda valor: 1 if valor >= 1 else 0
            )

            st.line_chart(
                estado_sensor,
                x="data_hora",
                y="deteccao",
                x_label="Data e hora",
                y_label="Detecção (0 = livre, 1 = caixa)",
            )

            st.caption(
                "0 = sensor livre | 1 = caixa detectada. Dados registrados a partir da variável Main.Sensor."
            )
        else:
            st.info(
                "Ainda não existem registros do sensor de presença no período."
            )

        # DETECÇÕES POR DIA
        st.divider()
        st.subheader("Caixas detectadas por dia")

        if not eventos_caixa.empty:
            eventos_caixa = eventos_caixa.dropna(subset=["data_hora"])
            eventos_caixa["dia"] = eventos_caixa["data_hora"].dt.date

            caixas_por_dia = (
                eventos_caixa.groupby("dia")
                .size()
                .reset_index(name="Caixas detectadas")
            )

            st.bar_chart(
                caixas_por_dia,
                x="dia",
                y="Caixas detectadas",
                x_label="Dia",
                y_label="Detecções",
            )

            st.caption(
                "Contagem baseada nos eventos de transição para 'Caixa detectada'. "
                "É uma contagem de detecções, não uma confirmação de peças aprovadas."
            )
        else:
            st.info(
                "Ainda não existem eventos de detecção de caixas no período selecionado."
            )

        # EVENTOS POR DIA
        st.divider()
        st.subheader("Eventos operacionais por dia")

        eventos_validos = eventos.dropna(subset=["data_hora"]).copy()

        if not eventos_validos.empty:
            eventos_validos["dia"] = eventos_validos["data_hora"].dt.date

            eventos_por_dia = (
                eventos_validos.groupby("dia")
                .size()
                .reset_index(name="Quantidade de eventos")
            )

            st.bar_chart(
                eventos_por_dia,
                x="dia",
                y="Quantidade de eventos",
                x_label="Dia",
                y_label="Quantidade de eventos",
            )
        else:
            st.info("Não existem eventos registrados no período selecionado.")

        # TEMPO DE FUNCIONAMENTO
        st.divider()
        st.subheader("Tempo de funcionamento da esteira por dia")

        if not tempo_por_dia.empty:
            st.bar_chart(
                tempo_por_dia,
                x="dia",
                y="Tempo ligado (minutos)",
                x_label="Dia",
                y_label="Tempo ligado (minutos observados)",
            )
        else:
            st.info(
                "Ainda não há intervalos consecutivos suficientes com o motor ligado "
                "para calcular o tempo de funcionamento."
            )

        st.caption(
            "O cálculo utiliza as amostras do estado do motor. Intervalos maiores que "
            "15 segundos são desconsiderados para não presumir funcionamento durante lacunas de registro."
        )

        # QUANTIDADE DE ACIONAMENTOS
        st.divider()
        st.subheader("Acionamentos da esteira por dia")

        if not acionamentos_por_dia.empty:
            st.bar_chart(
                acionamentos_por_dia,
                x="dia",
                y="Acionamentos",
                x_label="Dia",
                y_label="Acionamentos (transição 0 → 1)",
            )
        else:
            st.info(
                "Ainda não existem transições registradas de motor desligado para ligado."
            )

        st.caption(
            "Cada acionamento corresponde a uma transição registrada de 0 (desligado) para 1 (ligado) em Main.Motor."
        )

        # HISTÓRICO RECENTE DO PROCESSO
        st.divider()
        st.subheader("Eventos recentes do processo")

        if not eventos.empty:
            mascara_processo = eventos["evento_normalizado"].str.contains(
                "esteira|motor|sensor de presença|sensor de presenca|opc ua|caixa detectada|velocidade|alerta|comando de partida|processo",
                regex=True,
                na=False,
            )

            eventos_processo = eventos.loc[mascara_processo].copy()

            if not eventos_processo.empty:
                eventos_processo = eventos_processo.sort_values(
                    "data_hora",
                    ascending=False,
                ).head(30)

                eventos_processo = eventos_processo[
                    ["data_hora", "equipamento", "evento", "usuario", "nivel"]
                ].rename(
                    columns={
                        "data_hora": "Data e hora",
                        "equipamento": "Equipamento",
                        "evento": "Evento",
                        "usuario": "Usuário",
                        "nivel": "Nível",
                    }
                )

                st.dataframe(
                    eventos_processo,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "Não existem eventos específicos da esteira ou dos sensores no período."
                )
        else:
            st.info("Ainda não existem eventos do processo no período selecionado.")

        # INDICADORES COMPLEMENTARES
        st.divider()
        st.subheader("Indicadores complementares")

        st.info(
            "O simulador atual disponibiliza Main.Start, Main.Motor, Main.Sensor e "
            "Main.Velocidade. As detecções do sensor são apresentadas como detecções, "
            "não como ciclos completos. Temperatura, nível, válvulas e quantidade de "
            "ciclos somente serão exibidos quando existirem sinais correspondentes no CLP."
        )

    except Exception:

        st.error(
            "Não foi possível carregar os gráficos. "
            "Verifique a conexão com o MySQL e a estrutura das tabelas."
        )

    finally:
        if engine is not None:
            engine.dispose()


# =====================================
# MONITORAMENTO DE SEGURANÇA
# =====================================

def ler_logs_cloudwatch(log, minutos=60, limite_paginas=10):
    """Consulta os eventos do grupo CloudWatch configurado no GerenciadorLog."""
    cliente = getattr(log, "cloudwatch", None)
    grupo = getattr(log, "grupo_cloudwatch", None)

    if cliente is None or not grupo:
        raise RuntimeError(
            "Cliente CloudWatch indisponível. Verifique as credenciais e a região AWS."
        )

    inicio_ms = int(
        (datetime.now().timestamp() - int(minutos) * 60) * 1000
    )

    eventos_brutos = []
    proximo_token = None

    for _ in range(limite_paginas):
        argumentos = {
            "logGroupName": grupo,
            "startTime": inicio_ms,
            "limit": 100,
        }

        if proximo_token:
            argumentos["nextToken"] = proximo_token

        resposta = cliente.filter_log_events(**argumentos)
        eventos_brutos.extend(resposta.get("events", []))

        novo_token = resposta.get("nextToken")

        if not novo_token or novo_token == proximo_token:
            break

        proximo_token = novo_token

    registros = []

    for evento in eventos_brutos:
        mensagem_original = str(evento.get("message", ""))
        timestamp = evento.get("timestamp")

        data_evento = (
            datetime.fromtimestamp(timestamp / 1000)
            if timestamp is not None
            else datetime.now()
        )

        try:
            conteudo = json.loads(mensagem_original)
        except (json.JSONDecodeError, TypeError):
            conteudo = None

        if isinstance(conteudo, dict):
            mensagem = str(conteudo.get("mensagem", mensagem_original))
            nivel = str(conteudo.get("nivel", "INFO")).upper()
            usuario = conteudo.get("usuario") or "Não identificado"
            equipamento = conteudo.get("equipamento") or "Sistema"
        else:
            mensagem = mensagem_original
            nivel = "INFO"
            usuario = "Não identificado"
            equipamento = "Sistema"

            texto_upper = mensagem.upper()

            for nivel_possivel in ("CRITICAL", "ERROR", "WARNING", "INFO"):
                if nivel_possivel in texto_upper:
                    nivel = nivel_possivel
                    break

        registros.append(
            {
                "data": data_evento,
                "nivel": nivel,
                "usuario": usuario,
                "equipamento": equipamento,
                "mensagem": mensagem,
                "origem": "AWS CloudWatch",
            }
        )

    colunas = [
        "data",
        "nivel",
        "usuario",
        "equipamento",
        "mensagem",
        "origem",
    ]

    if not registros:
        return pd.DataFrame(columns=colunas)

    dados = pd.DataFrame(registros, columns=colunas)
    dados["data"] = pd.to_datetime(dados["data"], errors="coerce")

    return dados.dropna(subset=["data"]).sort_values(
        "data",
        ascending=False,
    )


@st.fragment(run_every=10)
def tela_monitoramento(log):
    aplicar_estilo()

    if st.session_state.perfil not in ("admin", "engenheiro"):
        st.error("Acesso não autorizado.")

        log.registrar(
            "WARNING",
            (
                "Tentativa de acesso não autorizado ao Monitoramento - "
                f"usuário: {st.session_state.usuario}"
            ),
        )
        return

    cabecalho(
        "Monitoramento de Segurança",
        "Análise de eventos, registros e atividades do sistema, incluindo logs da AWS CloudWatch.",
        "SEGURANÇA",
    )

    st.html('<div class="section-label">FONTE DOS REGISTROS</div>')
    st.info("Os registros de acesso e segurança são consultados diretamente no AWS CloudWatch.")

    minutos = st.selectbox(
        "Período de consulta",
        [
            "Últimos 15 minutos",
            "Última 1 hora",
            "Últimas 6 horas",
            "Últimas 24 horas",
            "Últimos 7 dias",
        ],
        index=1,
        key="periodo_logs_seguranca",
    )

    mapa_minutos = {
        "Últimos 15 minutos": 15,
        "Última 1 hora": 60,
        "Últimas 6 horas": 360,
        "Últimas 24 horas": 1440,
        "Últimos 7 dias": 10080,
    }

    janela_minutos = mapa_minutos[minutos]

    st.caption("Monitoramento atualizado automaticamente a cada 10 segundos.")

    try:
        with st.spinner("Consultando eventos no AWS CloudWatch..."):
            logs = ler_logs_cloudwatch(log, janela_minutos)

        st.success(
            f"Consulta realizada no grupo {log.grupo_cloudwatch} — "
            f"região {log.regiao_cloudwatch}."
        )

    except Exception as erro:
        st.error(
            "Não foi possível consultar o AWS CloudWatch. "
            "Verifique se a sessão do AWS Academy/VocLabs está ativa "
            "e se as permissões de leitura de logs estão disponíveis."
        )
        st.caption(f"Detalhe técnico: {erro}")
        return

    if logs.empty:
        st.info("Nenhum evento encontrado na fonte e no período selecionados.")
        return

    total_logs = len(logs)
    total_info = int((logs["nivel"] == "INFO").sum())
    total_warn = int((logs["nivel"] == "WARNING").sum())
    total_erro = int((logs["nivel"] == "ERROR").sum())
    total_crit = int((logs["nivel"] == "CRITICAL").sum())

    st.divider()
    st.html('<div class="section-label">RESUMO DOS EVENTOS</div>')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total", total_logs)

    with col2:
        st.metric("INFO", total_info)

    with col3:
        st.metric("WARNING", total_warn)

    with col4:
        st.metric("ERROR", total_erro)

    with col5:
        st.metric("CRITICAL", total_crit)

    st.divider()
    st.subheader("Análise de Segurança")

    invalidas = logs["mensagem"].astype(str).str.contains(
        "Tentativa de login inválida",
        na=False,
        case=False,
        regex=False,
    )

    tentativas_invalidas = int(invalidas.sum())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Tentativas inválidas no período", tentativas_invalidas)

    with col2:
        if tentativas_invalidas >= 3:
            st.error("🚨 Possível ataque de força bruta!")
        else:
            st.success("Nenhum alerta de força bruta detectado no período.")

    st.divider()
    st.subheader("Distribuição dos Eventos")

    distribuicao = logs["nivel"].value_counts().reindex(
        ["INFO", "WARNING", "ERROR", "CRITICAL"],
        fill_value=0,
    )

    st.bar_chart(distribuicao)

    st.divider()
    st.subheader("Histórico de Eventos")

    col1, col2 = st.columns(2)

    with col1:
        filtro_nivel = st.selectbox(
            "Filtrar por nível",
            ["Todos", "INFO", "WARNING", "ERROR", "CRITICAL"],
            key="filtro_nivel_logs",
        )

    with col2:
        usuarios_disponiveis = sorted(
            str(item) for item in logs["usuario"].dropna().unique()
        )

        filtro_usuario = st.selectbox(
            "Filtrar por usuário",
            ["Todos"] + usuarios_disponiveis,
            key="filtro_usuario_logs",
        )

    exibicao = logs.copy()

    if filtro_nivel != "Todos":
        exibicao = exibicao[exibicao["nivel"] == filtro_nivel]

    if filtro_usuario != "Todos":
        exibicao = exibicao[
            exibicao["usuario"].astype(str) == filtro_usuario
        ]

    exibicao = exibicao.sort_values("data", ascending=False)

    st.dataframe(
        exibicao[
            ["data", "nivel", "usuario", "equipamento", "mensagem", "origem"]
        ].rename(
            columns={
                "data": "Data e hora",
                "nivel": "Nível",
                "usuario": "Usuário",
                "equipamento": "Equipamento",
                "mensagem": "Evento",
                "origem": "Origem",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# =====================================
# TELA DE CADASTRO DE USUÁRIOS
# =====================================

def tela_cadastro_usuarios(log):
    import bcrypt

    aplicar_estilo()

    # Somente administradores podem gerenciar contas.
    if st.session_state.perfil != "admin":
        st.error("Acesso não autorizado. Somente administradores podem gerenciar usuários.")

        log.registrar(
            "WARNING",
            (
                "Tentativa de acesso não autorizado ao Cadastro de Usuários - "
                f"usuário: {st.session_state.usuario}"
            ),
        )
        return

    cabecalho(
        "Cadastro de Usuários",
        "Gerenciamento de contas, perfis e permissões de acesso.",
        "USUÁRIOS",
    )

    perfis = ["admin", "operador", "engenheiro"]

    # Consulta a lista atual de usuários.
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT id, usuario, perfil, status
            FROM usuarios
            ORDER BY usuario
            """
        )

        registros = cursor.fetchall()

        usuarios = pd.DataFrame(
            registros,
            columns=["ID", "Usuário", "Perfil", "Status"],
        )

    except Exception:
        st.error("Não foi possível consultar os usuários no MySQL.")
        return

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()

    # Resumo das contas.
    total = len(usuarios)
    ativos = int((usuarios["Status"] == 1).sum()) if not usuarios.empty else 0
    inativos = int((usuarios["Status"] == 0).sum()) if not usuarios.empty else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de usuários", total)

    with col2:
        st.metric("Contas ativas", ativos)

    with col3:
        st.metric("Contas inativas", inativos)

    st.divider()

    # Cadastro de nova conta.
    st.subheader("Cadastrar novo usuário")

    with st.container(border=True):
        with st.form("form_novo_usuario", clear_on_submit=True):
            novo_usuario = st.text_input(
                "Nome de usuário",
                placeholder="Digite o nome de usuário",
            )

            nova_senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite a senha",
            )

            novo_perfil = st.selectbox(
                "Perfil de acesso",
                perfis,
                format_func=lambda perfil: perfil.capitalize(),
            )

            cadastrar = st.form_submit_button(
                "Cadastrar usuário",
                use_container_width=True,
                type="primary",
            )

        if cadastrar:
            if not novo_usuario.strip() or not nova_senha:
                st.error("Preencha o nome de usuário e a senha.")

            else:
                conexao = None
                cursor = None

                try:
                    senha_hash = bcrypt.hashpw(
                        nova_senha.encode("utf-8"),
                        bcrypt.gensalt(),
                    ).decode("utf-8")

                    conexao = conectar_banco()
                    cursor = conexao.cursor()

                    cursor.execute(
                        """
                        INSERT INTO usuarios (usuario, senha_hash, perfil, status)
                        VALUES (%s, %s, %s, 1)
                        """,
                        (novo_usuario.strip(), senha_hash, novo_perfil),
                    )

                    conexao.commit()

                    log.registrar(
                        "INFO",
                        (
                            f"Novo usuário cadastrado: {novo_usuario.strip()} "
                            f"- perfil: {novo_perfil}"
                        ),
                    )

                    st.success("Usuário cadastrado com sucesso!")
                    st.rerun()

                except Exception:

                    st.error(
                        "Não foi possível cadastrar. Verifique se o nome "
                        "de usuário já existe."
                    )

                finally:
                    if cursor is not None:
                        cursor.close()

                    if conexao is not None:
                        conexao.close()

    st.divider()
    st.subheader("Usuários cadastrados")

    tabela = usuarios.copy()
    tabela["Status"] = tabela["Status"].map({1: "Ativo", 0: "Inativo"})

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
    )

    if usuarios.empty:
        st.info("Não existem usuários cadastrados para editar.")
        return

    st.divider()
    st.subheader("Editar usuário")

    usuario_selecionado = st.selectbox(
        "Selecione o usuário",
        usuarios["Usuário"].tolist(),
        key="usuario_selecionado_edicao",
    )

    registro = usuarios[
        usuarios["Usuário"] == usuario_selecionado
    ].iloc[0]

    usuario_id = int(registro["ID"])
    perfil_atual = str(registro["Perfil"])
    status_atual = int(registro["Status"])

    with st.container(border=True):
        with st.form("form_editar_usuario"):
            usuario_editado = st.text_input(
                "Nome de usuário",
                value=usuario_selecionado,
            )

            perfil_editado = st.selectbox(
                "Perfil",
                perfis,
                index=perfis.index(perfil_atual) if perfil_atual in perfis else 0,
            )

            senha_editada = st.text_input(
                "Nova senha (opcional)",
                type="password",
                placeholder="Deixe vazio para manter a senha atual",
            )

            salvar_edicao = st.form_submit_button(
                "Salvar alterações",
                use_container_width=True,
                type="primary",
            )

        if salvar_edicao:
            usuario_editado = usuario_editado.strip()

            if not usuario_editado:
                st.error("O nome de usuário não pode ficar vazio.")

            elif (
                usuario_selecionado == st.session_state.usuario
                and perfil_editado != "admin"
            ):
                st.error(
                    "Não é permitido remover o perfil de administrador da própria conta."
                )

            else:
                conexao = None
                cursor = None

                try:
                    conexao = conectar_banco()
                    cursor = conexao.cursor()

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM usuarios
                        WHERE perfil = 'admin' AND status = 1
                        """
                    )

                    total_admins = int(cursor.fetchone()[0])

                    if (
                        status_atual == 1
                        and perfil_atual == "admin"
                        and perfil_editado != "admin"
                        and total_admins <= 1
                    ):
                        st.error(
                            "O sistema precisa manter pelo menos um administrador ativo."
                        )

                    else:
                        cursor.execute(
                            """
                            UPDATE usuarios
                            SET usuario = %s, perfil = %s
                            WHERE id = %s
                            """,
                            (usuario_editado, perfil_editado, usuario_id),
                        )

                        if senha_editada:
                            senha_hash = bcrypt.hashpw(
                                senha_editada.encode("utf-8"),
                                bcrypt.gensalt(),
                            ).decode("utf-8")

                            cursor.execute(
                                "UPDATE usuarios SET senha_hash = %s WHERE id = %s",
                                (senha_hash, usuario_id),
                            )

                        conexao.commit()

                        if usuario_selecionado == st.session_state.usuario:
                            st.session_state.usuario = usuario_editado
                            st.session_state.perfil = perfil_editado

                        log.registrar(
                            "INFO",
                            (
                                f"Cadastro atualizado: {usuario_selecionado} "
                                f"para {usuario_editado} - perfil: {perfil_editado}"
                            ),
                        )

                        st.success("Cadastro atualizado com sucesso!")
                        st.rerun()

                except Exception:

                    st.error(
                        "Não foi possível atualizar. Verifique se o nome "
                        "de usuário já existe."
                    )

                finally:
                    if cursor is not None:
                        cursor.close()

                    if conexao is not None:
                        conexao.close()

    st.divider()
    st.subheader("Status da conta")

    if status_atual == 1:
        st.success("Esta conta está ativa.")

        if st.button("Desativar usuário", use_container_width=True):
            if usuario_selecionado == st.session_state.usuario:
                st.error(
                    "Você não pode desativar a própria conta enquanto estiver conectado."
                )

            else:
                conexao = None
                cursor = None

                try:
                    conexao = conectar_banco()
                    cursor = conexao.cursor()

                    if perfil_atual == "admin":
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM usuarios
                            WHERE perfil = 'admin' AND status = 1
                            """
                        )

                        total_admins = int(cursor.fetchone()[0])
                    else:
                        total_admins = 2

                    if perfil_atual == "admin" and total_admins <= 1:
                        st.error(
                            "Não é possível desativar o último administrador ativo."
                        )

                    else:
                        cursor.execute(
                            "UPDATE usuarios SET status = 0 WHERE id = %s",
                            (usuario_id,),
                        )

                        conexao.commit()

                        log.registrar(
                            "WARNING",
                            f"Usuário desativado: {usuario_selecionado}",
                        )

                        st.success("Usuário desativado com sucesso!")
                        st.rerun()

                except Exception:
                    st.error("Não foi possível desativar o usuário.")

                finally:
                    if cursor is not None:
                        cursor.close()

                    if conexao is not None:
                        conexao.close()

    else:
        st.warning("Esta conta está inativa.")

        if st.button(
            "Ativar usuário",
            use_container_width=True,
            type="primary",
        ):
            conexao = None
            cursor = None

            try:
                conexao = conectar_banco()
                cursor = conexao.cursor()

                cursor.execute(
                    "UPDATE usuarios SET status = 1 WHERE id = %s",
                    (usuario_id,),
                )

                conexao.commit()

                log.registrar(
                    "INFO",
                    f"Usuário ativado: {usuario_selecionado}",
                )

                st.success("Usuário ativado com sucesso!")
                st.rerun()

            except Exception:
                st.error("Não foi possível ativar o usuário.")

            finally:
                if cursor is not None:
                    cursor.close()

                if conexao is not None:
                    conexao.close()