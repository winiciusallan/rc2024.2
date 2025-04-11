import sys
import os
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
            logger.debug(f"Ouvindo nova conexão")
            req, addr = self.socket.recvfrom(1024)

            self.__handle_request(req.decode().strip(), addr)

    def __handle_request(self, req: str, addr):
        logger.debug(f"Solicitação UDP de {addr}: {req}")

        _, proto, file = [x.strip() for x in req.split(",")]

        if not self.__validate_proto(proto, addr):
            return

        if not self.__validate_file(file, addr):
            return

        self.__send_response(addr, file)

    def __validate_proto(self, proto: str, addr) -> bool:
        if proto.upper() != "TCP":
            logger.warning(f"Protocolo inválido de {addr}")
            self.__send_error("PROTOCOLO INVALIDO", addr)
            return False
        return True

    def __validate_file(self, file: str, addr) -> bool:
        if not os.path.exists(file):
            logger.error(f"Arquivo não encontrado: {file}")
            self.__send_error("ARQUIVO NAO ENCONTRADO", addr)
            return False
        return True

    def __send_response(self, addr, file: str):
        res = f"RESPONSE, TCP,{self.tcp_port},{file}".encode()
        logger.info(f"Enviando resposta de negociação para {addr}")
        self.socket.sendto(res, addr)
        self.__negotiate_tcp(file)

        response = f"RESPONSE,TCP,{self.tcp_port},{file}".encode()
        logger.info(f"Enviando resposta de negociação para {addr}")
        self.socket.sendto(response, addr)

    def __send_error(self, message: str, addr):
        error_response = f"ERROR,{message},,".encode()
        self.socket.sendto(error_response, addr)

    def __negotiate_tcp(self, file):
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind(("", self.tcp_port))
            server_socket.listen(1)

            logger.info("Esperando conexão TCP...")
            conn, client_addr = server_socket.accept()
            logger.info(f"Cliente TCP conectado de {client_addr}")
            self.__send_file(conn, file)

    def __send_file(self, conn, file):
        with conn, open(file, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.sendall(chunk)

        conn.close()
        logger.info(f"Arquivo '{file}' enviado com sucesso")

    def close(self):
        self.socket.close()
        logger.info("Socket UDP fechado")
