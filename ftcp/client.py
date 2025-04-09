import sys
from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket as tcp_socket, SOCK_STREAM
from configparser import ConfigParser

def usage():
    print("correct usage: python client.py <PROTOCOL> <FILE>")

def get_config():
    config = ConfigParser()
    config.read("config.ini")
    return config['SERVER']

def get_udp_port():
    config = get_config()
    udp_port = int(config['UDP_NEGOTIATION_PORT'])
    return udp_port

def validate_args(args):
    if len(args) != 3:
        usage()
        sys.exit(1)

def get_args(args):
    validate_args(args)
    return args[1].strip().upper(), args[2].strip().lower()

def main(args):
    proto, file = get_args(args)
    udp_client = socket(AF_INET, SOCK_DGRAM)

    msg = f"REQUEST,{proto},{file}".encode()
    #print(f"enviando mensagem {msg}")
    udp_client.sendto(msg, ("localhost", get_udp_port()))


    data, _ = udp_client.recvfrom(1024)
    response = data.decode().strip()
    #print(f"resposta recebida do servidor {response}")
    
    if response.startswith("ERROR"):
        return

    _, proto, port, file = [x.strip() for x in response.split(",")]

    if proto.upper() == "TCP":
        client_tcp = tcp_socket(AF_INET, SOCK_STREAM)
        #print(f"conectando ao servidor tcp")
        client_tcp.connect(("127.0.0.1", int(port)))

        #print(f"conectado ao servidor, recebendo arquivo {file}")

        with open(f"cliente_{file}", "wb") as f:
            while True:
                chunk = client_tcp.recv(1024)
                if not chunk:
                    break
                f.write(chunk)

        client_tcp.close()
        #print(f"arquivo salvo como 'cliente_{file}' com sucesso")

if __name__ == "__main__":
    main(sys.argv)