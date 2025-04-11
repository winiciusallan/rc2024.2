from ftcp import FTCP
from configparser import ConfigParser
from logger_config import setup_logger

logger = setup_logger(__name__)


def server_config(filename="config.ini"):
    config = ConfigParser()
    config.read(filename)
    return int(config["SERVER"]["TCP_PORT"]), int(
        config["SERVER"]["UDP_NEGOTIATION_PORT"]
    )


def main():
    tcp_port, udp_port = server_config()

    ftcp = FTCP(tcp_port)
    logger.info("Servidor rodando")

    try:
        ftcp.bind("", udp_port)
    except KeyboardInterrupt:
        logger.info("Encerrando servidor")
        ftcp.close()


if __name__ == "__main__":
    main()
