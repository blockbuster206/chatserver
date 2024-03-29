from tkinter import *
import socket
import threading
import os
from time import sleep


class Main:
    def __init__(self):
        self.root = Tk()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = Entry(self.root, font=('Consolas', 15, 'bold'), bg='black', fg='white', insertbackground='white')
        self.root.resizable(0, 0)
        self.exiting = False
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.root.title('ALTERA CHAT CLIENT')
        self.listbox = Listbox(self.root, font=('Consolas', 15, 'bold'), bg='black', fg='white', width=52)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.geometry('600x400')
        self.name.pack(side=TOP)
        self.root.bind('<Return>', func=self.rootconfig)
        self.root.config(bg='black')

    def exit(self):
        self.exiting = True
        print('you have closed the connection')
        self.sock.close()
        sys.exit()


    def rootconfig(self, event):
        self.name.place(x=1000, y=1000)
        threading.Thread(target=self.join).start()


    def join(self):
        conlabel = Label(text='Connecting', font=('Consolas', 15, 'bold'), bg='black', fg='white')
        conlabel.pack(side=TOP)
        if not self.exiting:
            try:
                try:
                    self.sock.connect(('altera-server.ddns.net', 2288))
                except:
                    self.sock.connect(('localhost', 2288))
                finally:
                    self.sock.send(self.name.get().encode('utf-8'))
                    self.index = self.sock.recv(1024).decode('utf-8')
                    print(f'Your connection index: {self.index}')
            except:
                print("error couldn't connect to server\nretrying in 2 seconds")
                conlabel.destroy()
                print('retrying')
                self.join()
            finally:
                sleep(3)
                conlabel.place(x=1000, y=1000)
                print('connected to server')
                conlabel = Label(text='Connected to server', font=('Consolas', 15, 'bold'), bg='black', fg='white')
                conlabel.place(x=350, y=150)
                self.initbild()
                threading.Thread(target=self.recv).start()
                sleep(1)
                conlabel.destroy()
        else:
            sys.exit()



    def initbild(self):
        Label(text='ALTERA CHAT CLIENT V.1.0', font=('Consolas', 15, 'bold'), bg='black', fg='white').place(x=0, y=0)
        self.root.bind('<Return>', func=self.sendmsg)
        self.listbox.place(x=12, y=50)
        self.entry()

    def entry(self):
        Label(self.root, bg='black', fg='white', text='Messsge:', font=('Consolas', 15, 'bold')).place(x=0, y=320)
        self.hello = Text(self.root, bg='black', fg='white', height=1, font=('Consolas', 15, 'bold'),
                          insertbackground='white', bd=3)
        self.hello.place(x=0, y=369)

    def sendmsg(self, event):
        if not self.exiting:
            msg = str(self.hello.get("1.0", 'end-1c'))
            if msg == '':
                print('none')
            else:
                self.sock.send(msg.encode('utf-8'))
                self.entry()
        else:
            sys.exit()

    def recv(self):
        self.running = True
        while self.running:
            try:
                hello = self.sock.recv(1024).decode('utf-8')
                print(hello)
                self.listbox.insert(0, hello)
            except:
                if not self.exiting:
                    print('error: server connection lost')
                    threading.Thread(target=self.join).start()
                    self.running = False
                else:
                    self.running = False




mainmf = Main()
mainmf.root.mainloop()

