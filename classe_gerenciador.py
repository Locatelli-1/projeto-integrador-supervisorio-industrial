import json
import logging
import socket
import time
from datetime import datetime

import boto3
import streamlit as st

from conexao_banco import conectar_banco


class GerenciadorLog:
    """Registra eventos no arquivo local, MySQL e AWS CloudWatch."""

    def __init__(self, arquivo):
        self.arquivo = arquivo

        logging.basicConfig(
            filename=self.arquivo,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8",
            force=True,
        )

        self.grupo_cloudwatch = "/projeto-integrador/supervisorio"
        nome_host = socket.gethostname().replace(".local", "").replace(" ", "-")
        self.fluxo_cloudwatch = f"streamlit-{nome_host}"
        self.regiao_cloudwatch = "us-east-1"
        self.cloudwatch = None
        self.cloudwatch_pronto = False

        try:
            self.cloudwatch = boto3.client(
                "logs",
                region_name=self.regiao_cloudwatch,
            )
            self.cloudwatch_pronto = self._preparar_cloudwatch()
        except Exception as erro:
            logging.warning(
                "CloudWatch não inicializado. Os registros locais e MySQL continuarão ativos: %s",
                erro,
            )

    def _preparar_cloudwatch(self):
        """Garante a existência do grupo e do fluxo de logs."""
        if self.cloudwatch is None:
            return False

        try:
            grupos = self.cloudwatch.describe_log_groups(
                logGroupNamePrefix=self.grupo_cloudwatch,
                limit=50,
            ).get("logGroups", [])

            grupo_existe = any(
                item.get("logGroupName") == self.grupo_cloudwatch
                for item in grupos
            )

            if not grupo_existe:
                try:
                    self.cloudwatch.create_log_group(
                        logGroupName=self.grupo_cloudwatch
                    )
                except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
                    pass

            fluxos = self.cloudwatch.describe_log_streams(
                logGroupName=self.grupo_cloudwatch,
                logStreamNamePrefix=self.fluxo_cloudwatch,
                limit=50,
            ).get("logStreams", [])

            fluxo_existe = any(
                item.get("logStreamName") == self.fluxo_cloudwatch
                for item in fluxos
            )

            if not fluxo_existe:
                try:
                    self.cloudwatch.create_log_stream(
                        logGroupName=self.grupo_cloudwatch,
                        logStreamName=self.fluxo_cloudwatch,
                    )
                except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
                    pass

            return True

        except Exception as erro:
            logging.warning(
                "Não foi possível preparar o CloudWatch; arquivo local e MySQL permanecem ativos: %s",
                erro,
            )
            return False

    @staticmethod
    def _nivel_logging(nivel):
        niveis = {
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return niveis.get(str(nivel).upper(), logging.INFO)

    @staticmethod
    def _identificar_usuario(mensagem):
        try:
            usuario = st.session_state.get("usuario")
        except Exception:
            usuario = None

        if not usuario and "usuário: " in mensagem:
            usuario = mensagem.rsplit("usuário: ", 1)[-1].strip()

        return usuario

    @staticmethod
    def _identificar_equipamento(mensagem):
        texto = str(mensagem).casefold()

        if "esteira 01" in texto:
            return "Esteira 01"
        if "motor 01" in texto:
            return "Motor 01"
        return "Sistema"

    def _registrar_mysql(self, equipamento, mensagem, usuario, nivel):
        conexao = None
        cursor = None

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()

            sql = """
                INSERT INTO eventos (
                    equipamento,
                    evento,
                    usuario,
                    nivel
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (equipamento, mensagem, usuario, nivel),
            )
            conexao.commit()

        except Exception as erro:
            logging.error(
                "Falha ao registrar evento no MySQL: %s",
                erro,
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()

    def _registrar_cloudwatch(self, equipamento, mensagem, usuario, nivel):
        if self.cloudwatch is None:
            return

        if not self.cloudwatch_pronto:
            self.cloudwatch_pronto = self._preparar_cloudwatch()

        if not self.cloudwatch_pronto:
            return

        evento = {
            "timestamp_local": datetime.now().astimezone().isoformat(),
            "nivel": nivel,
            "usuario": usuario,
            "equipamento": equipamento,
            "mensagem": mensagem,
        }

        try:
            self.cloudwatch.put_log_events(
                logGroupName=self.grupo_cloudwatch,
                logStreamName=self.fluxo_cloudwatch,
                logEvents=[
                    {
                        "timestamp": int(time.time() * 1000),
                        "message": json.dumps(
                            evento,
                            ensure_ascii=False,
                        ),
                    }
                ],
            )

        except Exception as erro:
            # Não interrompe o supervisório se a sessão temporária da AWS expirar.
            logging.warning(
                "Falha ao enviar evento ao CloudWatch: %s",
                erro,
            )
            self.cloudwatch_pronto = False

    def registrar(self, nivel, mensagem):
        nivel = str(nivel).upper()
        mensagem = str(mensagem)

        # 1. ARQUIVO LOCAL
        logging.log(
            self._nivel_logging(nivel),
            mensagem,
        )

        # 2. IDENTIFICAÇÃO DO USUÁRIO E EQUIPAMENTO
        usuario = self._identificar_usuario(mensagem)
        equipamento = self._identificar_equipamento(mensagem)

        # 3. BANCO DE DADOS MYSQL
        self._registrar_mysql(
            equipamento,
            mensagem,
            usuario,
            nivel,
        )

        # 4. AWS CLOUDWATCH
        self._registrar_cloudwatch(
            equipamento,
            mensagem,
            usuario,
            nivel,
        )