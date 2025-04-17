import sys
from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket as tcp_socket, SOCK_STREAM
from configparser import ConfigParser

from exceptions import (InvalidArgumentsException,
                        TCPConnectionException, FTCPException)
from logger_config import setup_logger

logger = setup_logger(__name__)


def get_config():
    config = ConfigParser()
    config.read("config.ini")
    return config["SERVER"]


def get_udp_port():
    return int(get_config()["UDP_NEGOTIATION_PORT"])


def validate_args(args):
    if len(args) != 3:
        raise InvalidArgumentsException("Número incorreto de argumentos. Uso correto: python client.py <PROTOCOL> <FILE>")


def get_args(args):
    validate_args(args)
    return args[1].strip().upper(), args[2].strip().lower()


def request_file_over_udp(proto, file):
    with socket(AF_INET, SOCK_DGRAM) as udp_client:
        msg = f"REQUEST,{proto},{file}".encode()
        logger.debug(f"Enviando mensagem UDP: {msg}")
        udp_client.sendto(msg, ("localhost", get_udp_port()))

        data, _ = udp_client.recvfrom(1024)
        response = data.decode().strip()
        logger.debug(f"Resposta recebida do servidor: {response}")

        return response


def send_confirm():
    with socket(AF_INET, SOCK_DGRAM) as udp_client:
        msg = f"CONFIRM,UDP,Arquivo recebido".encode()
        logger.debug(f"Enviando mensagem UDP: {msg}")
        udp_client.sendto(msg, ("localhost", get_udp_port()))


def handle_tcp_transfer(port, file):
    try:
        with tcp_socket(AF_INET, SOCK_STREAM) as client_tcp:
            logger.info(f"Conectando ao servidor TCP na porta {port}")
            client_tcp.connect(("127.0.0.1", int(port)))

            # Enviar comando get,arquivo
            get_command = f"get,{file}".encode()
            client_tcp.sendall(get_command)
            logger.info(f"Comando 'get,{file}' enviado")

            total_bytes = 0  # novo: contar bytes

            with open(f"cliente_{file}", "wb") as f:
                while True:
                    chunk = client_tcp.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    total_bytes += len(chunk)

            logger.info(f"Arquivo '{file}' salvo com sucesso, {total_bytes} bytes recebidos")

            # NOVO: enviar FCP_ACK depois de terminar
            ack_message = f"FCP_ACK,{total_bytes}".encode()
            client_tcp.sendall(ack_message)
            logger.info(f"Mensagem FCP_ACK enviada: {ack_message}")

            client_tcp.close()
            send_confirm()

    except Exception as e:
        raise TCPConnectionException(f"Falha na conexão TCP: {str(e)}")


def main(args):
    try:
        proto, file = get_args(args)
        response = request_file_over_udp(proto, file)

        if response.startswith("ERROR"):
            logger.error(f"Erro recebido: {response}")
            return

        
        if ":" in response:
            _, rest = response.split(":")
        else:
            raise FTCPException("Resposta inválida do servidor")

        port, file = [x.strip() for x in rest.split(",")]

        handle_tcp_transfer(port, file)

    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
