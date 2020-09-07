import socket
import threading

class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'altera-server.ddns.net'
        self.name = input('name: ')
        self.join()

    def join(self):
        self.sock.connect((self.ip, 2288))
        self.sock.send(self.name.encode('utf-8'))
        he = threading.Thread(target=self.send)
        le = threading.Thread(target=self.recv)
        he.start()
        le.start()

    def send(self):
        while True:
            self.sock.send(input('msg: ').encode('utf-8'))
    def recv(self):
        while True:
            print(f"{self.sock.recv(1024).decode('utf-8')}\n:")


main = Main()