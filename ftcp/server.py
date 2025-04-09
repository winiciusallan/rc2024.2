from ftcp import FTCP
from configparser import ConfigParser

config_filename = "config.ini"

config = ConfigParser()
config.read(config_filename)

tcp_port = int(config['SERVER']['TCP_PORT'])
udp_port = int(config['SERVER']['UDP_NEGOTIATION_PORT'])

ftcp = FTCP(tcp_port)

print(f"servidor rodando")

try:
    ftcp.bind('', udp_port)  
except KeyboardInterrupt:
    print("\nencerrando servidor")
    ftcp.close()
