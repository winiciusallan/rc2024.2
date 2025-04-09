import os
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

class FTCP:

    def __init__(self, tcp_port=5002):
        self.deal_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = None
        self.udp_socket = None
        self.tcp_port = tcp_port

    def bind(self, address: str, port: int):
        self.deal_socket.bind((address, port))

        while True:
            req, addr = self.deal_socket.recvfrom(1024)
            #print(f"udp recebido de {addr}: {req.decode()}")
            req = req.decode().strip()

            _, proto, file = [x.strip() for x in req.split(",")]

            if proto.upper() != "TCP":
                res = b"ERROR,PROTOCOLO INVALIDO,,"
                print(res)
                self.deal_socket.sendto(res, addr)
                continue 

            if not os.path.exists(file):
                res = b"ERROR,ARQUIVO NAO ENCONTRADO,,"
                print(res)
                self.deal_socket.sendto(res, addr)
                continue

            proto, port = self.__negotiate_proto(addr, file)
            res = f"RESPONSE,{proto},{port},{file}".encode()
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

            #print(f"esperando conexão tcp")
            conn, client_addr = s.accept()
            #print(f"cliente tcp conectado")
            self.__handle_connection(conn, file)
    
    def __handle_connection(self, conn, file):
        with open(file, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.sendall(chunk)

        conn.close()
        print(f"arquivo enviado com sucesso")

    def close(self):
        self.deal_socket.close()
