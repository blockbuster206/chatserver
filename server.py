import socket
from multiprocessing import Process

class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'localhost'
        self.sock.bind((self.ip, 8888))
        self.sock.listen(1)
        print('hello')
        self.whileloop()


    def whileloop(self):
        self.s, self.a = self.sock.accept()
        while True:
            print(f'Rory: {self.s.recv(1024).decode()}')

main = Main()
