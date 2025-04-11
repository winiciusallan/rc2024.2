class FTCPException(Exception):
    pass


class InvalidProtocolException(Exception):
    def __init__(self, message="Protocolo inválido. Apenas 'TCP' é suportado."):
        super().__init__(message)


class FileNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__(f"Arquivo '{filename}' não encontrado.")


class TCPConnectionException(Exception):
    def __init__(self, message="Erro na conexão TCP."):
        super().__init__(message)


class InvalidArgumentsException(Exception):
    def __init__(self, message="Argumentos inválidos fornecidos."):
        super().__init__(message)


class ServerConfigurationException(Exception):
    def __init__(self, message="Erro ao carregar configuração do servidor."):
        super().__init__(message)
