import socket
import threading
from logger_config import setup_logger

logger = setup_logger(__name__)


def udp_echo():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", 5698))
    logger.info("UDP server listening on port 5698")
    while True:
        data, addr = udp_sock.recvfrom(1024)
        if data:
            logger.info(f"UDP Received from {addr}: {data.decode('utf-8')}")
            udp_sock.sendto(data, addr)


def handle_tcp_client(conn, addr):
    logger.info(f"TCP Client connected from {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logger.info(f"TCP Received from {addr}: {data.decode('utf-8')}")
            conn.sendall(data)
    logger.info(f"TCP Client disconnected from {addr}")


def tcp_echo():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind(("0.0.0.0", 6000))
    tcp_sock.listen(5)
    logger.info("TCP server listening on port 6000")

    while True:
        conn, addr = tcp_sock.accept()
        client_thread = threading.Thread(
            target=handle_tcp_client, args=(conn, addr), daemon=True
        )
        client_thread.start()


def main():
    threading.Thread(target=udp_echo, daemon=True).start()
    threading.Thread(target=tcp_echo, daemon=True).start()

    logger.info("Servidor rodando. Pressione Ctrl+C para encerrar.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Servidor encerrado.")


if __name__ == "__main__":
    main()
