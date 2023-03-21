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
my_udp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
my_udp_server.bind(UDP_ADDRESS)

my_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_tcp_server.bind(TCP_ADDRESS)
my_tcp_server.listen()

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_client_socket.bind(UDP_ADDRESS)

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_client_socket.bind(TCP_ADDRESS)

packets_received = []
colecao_packets = {}

def handle_udp():
        data, addr = my_udp_server.recvfrom(BUFFERSIZE)
        print((data, addr))
        print(f"Recebendo dados do dispositivo: {addr}")
        print(f"Dados = {data.decode('utf-8')}")
        packets_received.append(data.decode('utf-8'))
        # if ('packets_received from: '+get_device_id(data)) in payload:
        #     print('ATUALIZANDO')
        #     payload.update({'packets_received from: '+get_device_id(data): data.decode('utf-8')})
        # else:
            # print('APENAS INSERINDO')
        print('atualizando')
        colecao_packets[get_device_id(data)] = data.decode('utf-8')
        print('>>>>>>>>>>>>>colecao de packets<<<<<<<<<<<<<')
        print(colecao_packets)
        print(data.decode('utf-8'))
        return data.decode('utf-8')
    
def get_consumption_rate(udp_data):
    return json.loads(udp_data).get('taxa_consumo')

def get_total_consumption(udp_data):
    total_consumption_value = str(json.loads(udp_data).get('consumo_total')).split('KWh')[0]
    return total_consumption_value

def get_device_id(udp_data):
    return json.loads(udp_data).get('num_contrato')

def get_day_time(udp_data):
    return json.loads(udp_data).get('dia_horario')

def get_request_param(request):
    print(f'path: {(request.split()[1]).decode("utf-8")}')
    return (request.split()[1]).decode('utf-8')

def generate_bill():
    message = f"""
    FATURA CORRESPONDENTE AO PERIODO DE \n{get_day_time(packets_received[0])}\nA \n{get_day_time(packets_received[len(packets_received)-1])}
    VALOR DA FATURA = R$ {int(get_total_consumption(packets_received[len(packets_received)-1])) - int(get_total_consumption(packets_received[0]))}
    """
    alert = f"""
    ATENCAO, VOCE EXCEDEU A COTA MENSAL DE CONSUMO TOTAL DE 100KW

    FATURA CORRESPONDENTE AO PERIODO DE \n{get_day_time(packets_received[0])}\nA \n{get_day_time(packets_received[len(packets_received)-1])}
    VALOR DA FATURA = R$ {int(get_total_consumption(packets_received[len(packets_received)-1])) - int(get_total_consumption(packets_received[0]))}
    """
    if (int(get_total_consumption(packets_received[len(packets_received)-1])) - int(get_total_consumption(packets_received[0])) > 100):
        message = alert
    return message

def handle_tcp(conn, addr):
    print(f"Iniciando servidor TCP na porta {TCP_PORT}")
    while True:
        udp_data = handle_udp()
        num_contrato = get_device_id(udp_data)
        print('NUM. DO CONTRATO')
        print(num_contrato)
        print('dados recebidos do dispositivo UDP:')
        print(udp_data)
        request = conn.recv(BUFFERSIZE)
        print('param do REQUEST')
        print(get_request_param(request))
        url_path = get_request_param(request)
        print('URL PATH')
        print(url_path)
        tcp_user_id = get_request_param(request).split('/')[1]
        print("TCP USER ID!!!")
        print(tcp_user_id)
        print("conn:")
        print(conn)
        print("addr:")
        print(addr)
        print('-----')
        print(request)
        print('*******str(num_contrato)*******')
        print(str(num_contrato))
        if str(num_contrato) in colecao_packets.keys():
            if (tcp_user_id == num_contrato):
                if url_path.endswith('/fatura'):
                    print('ENTREI NO IF DE URL PATH')
                    message = generate_bill()
                    conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))
                elif (url_path == '/'):
                    message = handle_udp()
                    conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))
                else:
                    message = f"""
                    id do dispositivo: {get_device_id(udp_data)}
                    consumo instantaneo (KWh): {get_consumption_rate(udp_data)}
                    consumo total (KW): {get_total_consumption(udp_data)}
                    data e horario: {get_day_time(udp_data)}
                    """
                    conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))
            else:
                message = 'Esse dispositivo nao esta registrado no momento!!!'
                conn.send(HTTP_RESPONSE.format(len(message), message).encode('utf-8'))

if __name__ == "__main__":
    # handle_tcp()

    # receive_udp_thread = threading.Thread(target = handle_udp)
    # receive_udp_thread.start()

    # send_tcp_thread = threading.Thread(target = handle_tcp)
    while True:
        try:
            tcp_conn, tcp_client = my_tcp_server.accept()
            thread_tcp = threading.Thread(target = handle_tcp, args=(tcp_conn, tcp_client))
            thread_tcp.start()
        except Exception as e:
            print("Erro ao tentar conexao. Causa: ", e.args)  
