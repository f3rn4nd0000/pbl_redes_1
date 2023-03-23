# pbl_redes_1

* * * 

Requisitos do problema:

1) O produto deve ser desenvolvido e depois testado através de contêineres Docker
2) As interfaces devem ser projetadase implementadas através de protocolo baseado em uma APl REST,
podendo ser testadas na apresentação através de softwares como Insomnia ou Postman;
3) Para permitir a avaliago do protótipo, o medidor de energia deve ser simulado por software para geração
de dados ficticios sobre o consumo. Para uma emulação realista do cenário proposto, cada dispositivo
medidor deve ser executado em um container Docker separado em um computador no laboratório;
4) O medidor deve possuir uma interface para controlar a geração dos dados em tempo real. Por exemplo,
através da interface deve ser possivel definir, aumentar ou diminuir o consumo de energia em kWh;
5) Por questões dos direitos comerciais, NENHUM framework de terceiro deve ser usado para implementar a
solução do problema. Neste caso, apenas os mecanismos básicos presentes no sistema operacional e
acessiveis pelas bibliotecas nativas da linguagem de programação podem ser usados para implementar a
comunicação sobre uma arquitetura de rede baseada no padrão da Internet.

Ambiente de desenvolvimento:

    ​ Sistema operacional: Arch Linux
    
    ​ Linguagem de programação: Python 3.10.4
    
    ​ Bibliotecas nativas utilizadas:
        - socket
        - json
        - threading
        - uuid

### Testando a aplicação:
* * *

Caso decida testar em ambiente local faça o clone do programa
e execute as instruções para instalar:
```
git clone https://github.com/f3rn4nd0000/pbl_redes_1.git
cd pbl_redes_1
```
Para rodar o servidor:
```
python servidor/server.py
```

Para rodar o dispositivo UDP:
```
python dispositivo-udp/udp-client.py
```
Lembre-se de modificar o IP no código, pois o IP do servidor foi definido em código (hardcoded) como o endereço do Larsid 06


No momento da inicialização do dispositivo UDP será gerado um [UUID](https://docs.python.org/3/library/uuid.html) e com base nele serão feitas as requisições para os respectivos dispositivos com aquele UUID


No portainer foram definidos os seguintes ambientes:
​ Larsid 06 (servidor) 
​ Larsid 02 e 03 (clientes UDP) 

Foram definidas as portas:
```
20001 para UDP
20004 para TCP
```

O programa contém dois endpoints que poderão receber 
requisições HTTP pelo Insomnia, que são as seguintes:

Requisição para endpoint <uuid>
```
GET http://172.16.103.6:20004/<uuid>
```
Exemplo de resposta para requisição acima:

```

id do dispositivo: 109e68d6-c9d1-11ed-b2b9-d46a6af0c499
consumo instantaneo (KWh): 1 KWh
consumo total (KW): 1 
data e horario: dia:03/23/23 horario:20:18:51

```

Requisição para endpoint <uuid>/fatura
```
GET http://172.16.103.6:20004/<uuid>/fatura
```
Exemplo de resposta para requisição acima:
```
    FATURA CORRESPONDENTE AO PERIODO DE 
dia:03/21/23 horario:20:31:58
A 
dia:03/21/23 horario:20:32:40
    VALOR DA FATURA = R$ 79
```

Para ambas requisições acima podemos ainda receber uma resposta do tipo:
```
Esse dispositivo nao esta registrado no momento!!!
```

