
from opcua import Client, ua


class Conexao_Opc:

    def __init__(self, url):
        # Endereço do servidor OPC UA
        self.url = url

    # =====================================
    # VALIDAÇÃO DO NODEID E DO VALOR
    # =====================================

    def __validar(self, node, valor=None):

        if not isinstance(node, str):
            return False

        # Padrão: "ns=1;s=Main.Start"
        if not node.startswith("ns="):
            return False

        if ";s=" not in node:
            return False

        if valor is not None:
            if not isinstance(valor, (bool, int, float)):
                return False

        return True

    # =====================================
    # CONEXÃO COM O CLP VIA OPC UA
    # =====================================

    def __conectar(self):

        cliente = Client(self.url)
        cliente.connect()

        return cliente

    def __obter_node(self, cliente, node):

        return cliente.get_node(node)

    # =====================================
    # LEITURA DE VALORES
    # =====================================

    def leitura_valor(self, node):

        if self.__validar(node) == True:

            client = self.__conectar()

            try:
                no_leitura = self.__obter_node(
                    client,
                    node
                )

                valor = no_leitura.get_value()

                return valor

            finally:
                client.disconnect()

        else:
            return None

    # =====================================
    # ESCRITA DE VALORES BOOLEANOS
    # =====================================

    def escrita_bool(self, node, valor):

        if self.__validar(node, valor) == False:
            return False

        if isinstance(valor, bool) == False:
            return False

        client = self.__conectar()

        try:
            no_escrita = self.__obter_node(
                client,
                node
            )

            no_escrita.set_value(
                ua.DataValue(
                    ua.Variant(
                        valor,
                        ua.VariantType.Boolean
                    )
                )
            )

            return True

        finally:
            client.disconnect()

    # =====================================
    # ESCRITA DE VALORES REAIS
    # =====================================

    def escrita_float(self, node, valor):

        if self.__validar(node, valor) == False:
            return False

        if isinstance(valor, (int, float)) == False:
            return False

        client = self.__conectar()

        try:
            no_escrita = self.__obter_node(
                client,
                node
            )

            no_escrita.set_value(
                ua.DataValue(
                    ua.Variant(
                        float(valor),
                        ua.VariantType.Float
                    )
                )
            )

            return True

        finally:
            client.disconnect()
