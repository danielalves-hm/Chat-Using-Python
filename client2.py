import socket
import pickle
from threading import Thread


class Client:
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 1234
        self.my_username = ''

        self.wait_to_send = 0
        self.wait_to_receive = 0

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.IP, self.PORT))

    def send_name(self):
        check_name = True
        while check_name:
            self.my_username = input('User name: ')
            self.client.send(bytes(f'{self.my_username}', 'utf-8'))
            msg = self.client.recv(32).decode('utf-8')
            print(f'Server says: {msg}')
            if msg == 'ACCEPT':
                check_name = False

    def send_or_receive(self):
        while True:
            if self.wait_to_send == 0:
                self.wait_to_send = 1
                Thread(target=self.send).start()

            if self.wait_to_receive == 0:
                self.wait_to_receive = 1
                Thread(target=self.receive).start()

    def send(self):
        to = input('To: ')
        msg = input('Message: ')

        msg_to_send = {"TO": f'{to}', "FROM": f'{self.my_username}', "MSG": f'{msg}'}
        msg_to_send = pickle.dumps(msg_to_send)

        self.client.send(msg_to_send)
        self.wait_to_send = 0

    def receive(self):
        msg_to_receive = self.client.recv(1024)
        msg = pickle.loads(msg_to_receive)

        print('-' * (10 + len(msg["FROM"])))
        print(f'FROM : {msg["FROM"]}')
        print(f'Message: {msg["MSG"]}')
        print('-' * (10 + len(msg["FROM"])))

        self.wait_to_receive = 0


c = Client()
c.send_name()
c.send_or_receive()
