import sys
import os
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger_config import setup_logger
logger = setup_logger(__name__)

class FTCP:

    def __init__(self, tcp_port=5002):
        self.deal_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = None
        self.udp_socket = None
        self.tcp_port = tcp_port

    def bind(self, address: str, port: int):
        self.deal_socket.bind((address, port))
        logger.info(f"Servidor UDP ligado em {address}:{port}")

        while True:
            req, addr = self.deal_socket.recvfrom(1024)
            req = req.decode().strip()
            logger.debug(f"Solicitação UDP de {addr}: {req}")

            _, proto, file = [x.strip() for x in req.split(",")]

            if proto.upper() != "TCP":
                res = b"ERROR,PROTOCOLO INVALIDO,,"
                logger.warning(f"Protocolo inválido de {addr}")
                self.deal_socket.sendto(res, addr)
                continue 

            if not os.path.exists(file):
                res = b"ERROR,ARQUIVO NAO ENCONTRADO,,"
                logger.error(f"Arquivo não encontrado: {file}")
                self.deal_socket.sendto(res, addr)
                continue

            proto, port = self.__negotiate_proto(addr, file)
            res = f"RESPONSE,{proto},{port},{file}".encode()
            logger.info(f"Enviando resposta de negociação para {addr}")
            self.deal_socket.sendto(res, addr)
            self.__negotiate_tcp(addr, file)

    def __negotiate_proto(self, address, file) -> tuple:
        port = self.tcp_port
        return "TCP", port

    def __negotiate_tcp(self, address, file):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind(('', self.tcp_port))
            s.listen(1)

            logger.info("Esperando conexão TCP...")
            conn, client_addr = s.accept()
            logger.info(f"Cliente TCP conectado de {client_addr}")
            self.__handle_connection(conn, file)
    
    def __handle_connection(self, conn, file):
        with open(file, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.sendall(chunk)

        conn.close()
        logger.info(f"Arquivo '{file}' enviado com sucesso")

    def close(self):
        self.deal_socket.close()
        logger.info("Socket UDP fechado")
