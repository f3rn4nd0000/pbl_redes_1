import socket
import threading 
import uuid
import sys
import time
import json
import random
from datetime import datetime

HOST = '0.0.0.0'
PORT = 20001

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = (HOST, PORT)
bufferSize          = 1024

class Device:

    def __init__(self):
        self.id = self.generate_id()
        self.client = self.create_client()
        self.device_total_consumption = 0
        self.consumption_rate = 0
        self.lock = threading.Lock()

    def generate_id(self) -> str:
        """
        Retorna um codigo UUID gerado com base no horário, portanto único,
        será usado para simular a geração de um numero de contrato para cada
        dispositivo/cliente
        """
        device_id = str(uuid.uuid1())
        print('device_id: '+device_id)
        return device_id

    def create_client(self)-> socket.socket:
        """
        Gera um socket entre o servidor e o dispositivo especificados pelo endereço
        armazenado em serverAddressPort (IP, Porta)
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(serverAddressPort)
        return client

    def alter_consumption(self, key) -> int:
        """
        Simula a alteração de consumo com base no input do usuário
        """
        if key == 'up':
            self.consumption_rate += 1
        elif key == 'down' and self.device_total_consumption > 0:
            self.consumption_rate -= 1
        if self.consumption_rate < 0:
            self.consumption_rate = 0
        # else:
        #     sys.exit(0)
        elif key == '\x03': # Detecta se CTRL+C foi pressionado
            message = f"O dispositivo {self.id} está sendo encerrado"
            print(message)
            self.client.send(message.encode())
            sys.exit(0)

        self.device_total_consumption += self.consumption_rate
        return self.consumption_rate

    def calculate_total_consumption(self, key) -> int:
        consumption_rate_variance = self.alter_consumption(key)
        if consumption_rate_variance > 0:
            self.device_total_consumption  += self.consumption_rate
        else:   
            self.device_total_consumption = self.device_total_consumption
        
        print(45*'-')
        print(f"taxa de consumo atual eh de: {self.consumption_rate} KWh")
        print(f"Consumo total do dispositivo eh de: {self.device_total_consumption} KWh")    
        print(45*'-')
        
        return self.device_total_consumption

    def send_message(self):
        # message = (
        #     f"taxa de consumo atual é: {self.consumption_rate} KWh\n"
        #     f"Consumo total do dispositivo é: {self.device_total_consumption} KWh\n"
        #     f"Num de contrato do cliente: {self.id}\n"
        #     )
        horario_atual = datetime.now()

        payload = {
            "taxa_consumo": f"{self.consumption_rate} KWh",
            "consumo_total": f"{self.device_total_consumption} KWh",
            "num_contrato": f"{self.id}",
            "dia_horario": f"{horario_atual.strftime('dia:%D horario:%H:%M:%S')}"
        }

        message = json.dumps(payload)

        if self.consumption_rate < 0:
            message = f"Dispositivo parou de consumir!\nEncerrando!"
        print('>>> mensagem enviada:')
        print(message)
        # print(len(message.encode()))
        print(self.client)
        self.client.sendto(message.encode(), serverAddressPort)

def random_select():
        possibilities = ['up', 'down']
        key = random.choice(possibilities)
        time.sleep(1)
        print(key)
        return key 

if __name__ == "__main__":
    new_device = Device()
    time.sleep(2)
    while True:
        key = random_select()
        new_device.alter_consumption(key)
        new_device.send_message()
