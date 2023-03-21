import socket
import threading
import json
import time

UDP_HOST         = "127.0.0.1"
UDP_PORT         = 20001
UDP_HOST_ADDRESS = ((UDP_HOST, UDP_PORT))
BUFFERSIZE       = 1024

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.connect(UDP_HOST_ADDRESS)
udp_data1 = f"Hello from {UDP_HOST}:{UDP_PORT}"
udp_data2 = f"Bye from {UDP_HOST}:{UDP_PORT}"

def send_data():
    while True:
        udp_client_socket.send(udp_data1.encode())
        print(f"Enviando {udp_data1}")
        time.sleep(3)
        udp_client_socket.send(udp_data2.encode())
        print(f"Enviando {udp_data2}")

if __name__ == "__main__":
    send_data()
