import sys
import os
from ftcp import FTCP
from configparser import ConfigParser
from exceptions import ServerConfigurationException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger_config import setup_logger

logger = setup_logger(__name__)


def server_config(filename="config.ini"):
    try:
        config = ConfigParser()
        config.read(filename)
        return int(config["SERVER"]["TCP_PORT"]), int(config["SERVER"]["UDP_NEGOTIATION_PORT"])
    except Exception as e:
        raise ServerConfigurationException(
            f"Erro ao ler arquivo de configuração: {str(e)}")


def main():
    try:
        tcp_port, udp_port = server_config()
        ftcp = FTCP(tcp_port)
        logger.info("Servidor FTCP iniciado")

        ftcp.bind("", udp_port)

    except KeyboardInterrupt:
        logger.info("Encerrando servidor por interrupção")
    except Exception as e:
        logger.error(f"Erro: {e}")
    finally:
        ftcp.close()


if __name__ == "__main__":
    main()
