import sys
from socket import socket, AF_INET, SOCK_DGRAM


def usage():
    print("usage")


def main(args):
    proto = args[1]
    file = args[2]
    client = socket(AF_INET, SOCK_DGRAM)

    msg = f"{proto},{file}".encode()

    client.sendto(msg, ("localhost", 5002))

    data, _ = client.recvfrom(1024)

    print(f"{data.decode()}")
    #


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        usage()
        sys.exit(1)

    main(args)
