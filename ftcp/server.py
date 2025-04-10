import sys
import os
from ftcp import FTCP
from configparser import ConfigParser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger_config import setup_logger
logger = setup_logger(__name__)

config_filename = "config.ini"
config = ConfigParser()
config.read(config_filename)

tcp_port = int(config['SERVER']['TCP_PORT'])
udp_port = int(config['SERVER']['UDP_NEGOTIATION_PORT'])

ftcp = FTCP(tcp_port)

logger.info("Servidor rodando")

try:
    ftcp.bind('', udp_port)  
except KeyboardInterrupt:
    logger.info("Encerrando servidor")
    ftcp.close()
