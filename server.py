import socket
import threading
import json

HOST_ADDRESS = "127.0.0.1"
UDP_PORT     = 20001
TCP_PORT     = 20004
UDP_ADDRESS  = (HOST_ADDRESS,UDP_PORT)
TCP_ADDRESS  = (HOST_ADDRESS,TCP_PORT)
BUFFERSIZE   = 1024
HTTP_RESPONSE = '''\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {}

{}
'''
my_udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_udp_server.bind(UDP_ADDRESS)

my_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_tcp_server.bind(TCP_ADDRESS)
my_tcp_server.listen()

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_client_socket.bind(UDP_ADDRESS)

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_client_socket.bind(TCP_ADDRESS)

def handle_udp():
    print(f"Iniciando servidor UDP")
    while True:
        data, addr = my_udp_server.recvfrom(BUFFERSIZE)
        print(f"Recebendo dados do dispositivo: {addr}")
        print(f"Dados = {data}")
        return data.decode('utf-8')
    
def get_consumption(udp_data):
    return json.loads(udp_data).get('taxa_consumo')

def get_consumption(udp_data):
    return json.loads(udp_data).get('consumo_total')

def get_device_id(udp_data):
    return json.loads(udp_data).get('num_contrato')

def get_request_param(request):
    print(f'path: {request.split()[1]}')
    return (request.split()[1]).decode('utf-8')

# def parse_tcp_request(request):
#     return (str(request.split('GET /')[1]).split(' HTTP/1.1')[0])

def handle_tcp():
    print(f"Iniciando servidor TCP na porta {TCP_PORT}")
    while True:
        message = handle_udp()
        num_contrato = get_device_id(message)
        print('NUM. DO CONTRATO')
        print(num_contrato)
        print('dados recebidos do dispositivo UDP:')
        print(message)
        conn, addr = my_tcp_server.accept()
        request = conn.recv(BUFFERSIZE)
        print('param do REQUEST')
        print(get_request_param(request))
        tcp_user_id = get_request_param(request).split('/')[1]
        print("TCP USER ID!!!")
        print(tcp_user_id)
        print("conn:")
        print(conn)
        print("addr:")
        print(addr)
        print('-----')
        print(request)
        if (tcp_user_id == num_contrato):
            conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))
        else:
            message = 'Esse usuario nao foi encontrado!!!'
            conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))

if __name__ == "__main__":
    # handle_tcp()

    # receive_udp_thread = threading.Thread(target = handle_udp)
    # receive_udp_thread.start()

    send_tcp_thread = threading.Thread(target = handle_tcp)
    send_tcp_thread.start()