import json
import socket
import time
from datetime import datetime

import boto3
import streamlit as st

from conexao_banco import conectar_banco


class GerenciadorLog:
    """Envia logs da aplicação ao CloudWatch e grava eventos operacionais no MySQL."""

    def __init__(self):
        self.grupo_cloudwatch = "/projeto-integrador/supervisorio"
        nome_host = socket.gethostname().replace(".local", "").replace(" ", "-")
        self.fluxo_cloudwatch = f"streamlit-{nome_host}"
        self.regiao_cloudwatch = "us-east-1"
        self.cloudwatch = None
        self.cloudwatch_pronto = False
        self.erro_cloudwatch = None

        try:
            self.cloudwatch = boto3.client(
                "logs",
                region_name=self.regiao_cloudwatch,
            )
            self.cloudwatch_pronto = self._preparar_cloudwatch()
        except Exception as erro:
            self.erro_cloudwatch = str(erro)

    def _preparar_cloudwatch(self):
        """Garante a existência do grupo e do fluxo de logs no CloudWatch."""
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

            self.erro_cloudwatch = None
            return True

        except Exception as erro:
            self.erro_cloudwatch = str(erro)
            return False

    @staticmethod
    def _identificar_usuario(mensagem):
        try:
            usuario = st.session_state.get("usuario")
        except Exception:
            usuario = None

        if not usuario:
            for marcador in ("usuário: ", "usuario: "):
                if marcador in mensagem.casefold():
                    posicao = mensagem.casefold().rfind(marcador)
                    usuario = mensagem[posicao + len(marcador):].strip()
                    break

        return usuario or "Não identificado"

    @staticmethod
    def _identificar_equipamento(mensagem):
        texto = str(mensagem).casefold()

        if "esteira 01" in texto:
            return "Esteira 01"
        if "motor 01" in texto:
            return "Motor 01"
        return "Sistema"

    def _registrar_cloudwatch(self, equipamento, mensagem, usuario, nivel):
        if self.cloudwatch is None:
            return False

        if not self.cloudwatch_pronto:
            self.cloudwatch_pronto = self._preparar_cloudwatch()

        if not self.cloudwatch_pronto:
            return False

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
                        "message": json.dumps(evento, ensure_ascii=False),
                    }
                ],
            )
            self.erro_cloudwatch = None
            return True

        except Exception as erro:
            # Sem fallback local: falhas de envio permanecem visíveis no retorno.
            self.cloudwatch_pronto = False
            self.erro_cloudwatch = str(erro)
            return False

    def registrar(self, nivel, mensagem):
        """Registra eventos de acesso, segurança e aplicação somente no CloudWatch."""
        nivel = str(nivel).upper()
        mensagem = str(mensagem)
        usuario = self._identificar_usuario(mensagem)
        equipamento = self._identificar_equipamento(mensagem)

        return self._registrar_cloudwatch(
            equipamento,
            mensagem,
            usuario,
            nivel,
        )

    def registrar_evento_processo(
        self,
        equipamento,
        evento,
        usuario=None,
        nivel="INFO",
    ):
        """Grava exclusivamente eventos reais do processo na tabela eventos do MySQL."""
        equipamento = str(equipamento).strip()
        evento = str(evento).strip()
        nivel = str(nivel).upper()

        if not equipamento or not evento:
            return False

        if usuario is None:
            try:
                usuario = st.session_state.get("usuario")
            except Exception:
                usuario = None

        conexao = None
        cursor = None

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT INTO eventos (
                    equipamento,
                    evento,
                    usuario,
                    nivel
                )
                VALUES (%s, %s, %s, %s)
                """,
                (equipamento, evento, usuario, nivel),
            )
            conexao.commit()
            return True

        except Exception as erro:
            self.registrar(
                "ERROR",
                f"Falha ao registrar evento operacional no MySQL: {erro}",
            )
            return False

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()