from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import sys

host = '192.168.2.94'
porta = 6668
buffer_size = 1500

server = socket(AF_INET, SOCK_STREAM)

try:
    server.connect((host, porta))
except Exception:
    print('Conexão não foi realizada porque o servidor está offline.')
    time.sleep(5) 
    exit()

def recv(): #recebimento de mensagens
    while True:
        try: 
            data = server.recv(buffer_size).decode('utf8')
        except:
            server.close()
            print('A conexão foi perdida.')
            exit()
        if (data == ''):
            exit()

        print(data)

process = Thread(target=recv).start()

while True:
    try:
        data = input()
        #Achei na internet não sei como funciona
        sys.stdout.write("\033[A")
        sys.stdout.write("\033[K")
    except:
        exit()
    try:
        server.send(data.encode())
    except:
        exit()