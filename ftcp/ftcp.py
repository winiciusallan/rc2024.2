import os
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_WR

from exceptions import InvalidProtocolException, FileNotFoundException, TCPConnectionException
from logger_config import setup_logger

logger = setup_logger(__name__)


class FTCP:

    def __init__(self, tcp_port=5002):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_port = tcp_port

    def bind(self, address: str, port: int):
        self.socket.bind((address, port))
        logger.info(f"Servidor UDP ligado em {address}:{port}")

        while True:
            req, addr = self.socket.recvfrom(1024)
            logger.debug(f"Ouvindo nova conexão")

            try:
                self.__handle_request(req.decode().strip(), addr)
            except Exception as e:
                logger.error(f"Erro na requisição: {e}")

    def __handle_request(self, req: str, addr):
        try:
            msg, proto, file = [x.strip() for x in req.split(",")]

            if msg == "CONFIRM":
                return

            if not self.__validate_proto(proto, addr):
                return

            if not self.__validate_file(file, addr):
                return

            self.__send_response(addr, file)

        except ValueError:
            logger.error(f"Formato inválido de requisição: {req}")

    def __validate_proto(self, proto: str, addr) -> bool:
        if proto.upper() != "TCP":
            logger.warning(f"Protocolo inválido de {addr}")
            self.__send_error("PROTOCOLO INVALIDO", addr)
            raise InvalidProtocolException()
        return True

    def __validate_file(self, file: str, addr) -> bool:
        if not os.path.exists(file):
            logger.error(f"Arquivo não encontrado: {file}")
            self.__send_error("ARQUIVO NAO ENCONTRADO", addr)
            raise FileNotFoundException(file)
        return True

    def __send_response(self, addr, file: str):
        response = f"RESPONSE:{self.tcp_port},{file}".encode()
        logger.info(f"Enviando resposta de negociação para {addr}")
        self.socket.sendto(response, addr)

        try:
            self.__negotiate_tcp(file)
        except TCPConnectionException as e:
            logger.error(str(e))

    def __send_error(self, message: str, addr):
        error_response = f"ERROR,{message},,".encode()
        self.socket.sendto(error_response, addr)

    def __negotiate_tcp(self, file):
        try:
            with socket(AF_INET, SOCK_STREAM) as server_socket:
                server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                server_socket.bind(("", self.tcp_port))
                server_socket.listen(1)

                logger.info("Esperando conexão TCP...")
                conn, client_addr = server_socket.accept()
                logger.info(f"Cliente TCP conectado de {client_addr}")

                try:
                    # Receber comando get,arquivo
                    get_request = conn.recv(1024).decode().strip()
                    logger.debug(f"Comando recebido: {get_request}")

                    if not get_request.startswith("get,"):
                        logger.error("Comando inválido recebido.")
                        conn.close()
                        return

                    requested_file = get_request.split(",")[1]

                    if requested_file != file:
                        logger.error("Arquivo solicitado não corresponde ao negociado.")
                        conn.close()
                        return

                    # Enviar o arquivo
                    self.__send_file(conn, file)

                    # Esperar FCP_ACK depois do envio
                    ack_message = conn.recv(1024).decode().strip()
                    logger.debug(f"Mensagem FCP_ACK recebida: {ack_message}")

                    if not ack_message.startswith("FCP_ACK,"):
                        logger.error("ACK inválido recebido.")
                    else:
                        bytes_received = ack_message.split(",")[1]
                        logger.info(f"Cliente confirmou recebimento de {bytes_received} bytes")

                finally:
                    conn.close()
                    logger.info("Conexão TCP encerrada com sucesso")

        except Exception as e:
            logger.error(f"Erro na negociação TCP: {str(e)}")
            raise TCPConnectionException(str(e))

    def __send_file(self, conn, file):
        with open(file, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.sendall(chunk)

        conn.shutdown(SHUT_WR)
        logger.info(f"Arquivo '{file}' enviado com sucesso")

    def close(self):
        self.socket.close()
        logger.info("Socket UDP fechado")
