from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


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
            req = req.decode()
            break

        proto, port = self.__negotiate_proto(req, addr)
        file = req.split(",")[1]
        res = f"{proto},{port},{file}".encode()
        self.deal_socket.sendto(res, addr)

    def __negotiate_proto(self, req, address) -> tuple:
        proto = req.split(",")[0].upper()
        port = -1

        if proto == "TCP":
            self.__negotiate_tcp(address)
            port = self.tcp_port

        if proto == "UDP":
            port = address[1]

        return proto, port

    def __negotiate_tcp(self, address):
        tcp = self.tcp_socket
        tcp = socket(AF_INET, SOCK_STREAM)
        tcp.bind((address[0], self.tcp_port))
        tcp.listen(1)

    def close(self):
        self.deal_socket.close()
