from ftcp import FTCP
from configparser import ConfigParser

config_filename = "config.ini"

config = ConfigParser()
config.read(config_filename)

tcp_port = int(config['SERVER']['TCP_PORT'])

ftcp = FTCP(tcp_port)

port = config['SERVER']['UDP_NEGOTIATION_PORT']
ftcp.bind('', int(port))
ftcp.close()
