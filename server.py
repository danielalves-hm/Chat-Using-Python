import socket
import pickle
from threading import Thread

class Server:
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 1234
        self.clients = []
        self.num_conections = 0
        self.num_threads = 0

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.IP, self.PORT))
        self.server.listen(5)

    def new_connection(self):
        while True:
            if self.num_threads == self.num_conections:
                Thread(target=self.new_client).start()
                self.num_threads += 1

    def new_client(self):
        clientsocket, address = self.server.accept()
        self.num_conections += 1

        try_name = True
        new_user = ''
        while try_name:
            new_user = clientsocket.recv(16).decode('utf-8')
            if len(self.clients) == 0:
                try_name = False
            else:
                for name in self.clients:
                    if name[1] == new_user:
                        clientsocket.send(bytes('FAILED', 'utf-8'))
                        break
                    else:
                        try_name = False
                        break

        clientsocket.send(bytes('ACCEPT', 'utf-8'))
        print('Nova conexão')
        self.clients.append((clientsocket, new_user))

        self.msg_manager(clientsocket, new_user)

    def msg_manager(self, clientsocket, user):
        while True:
            msg = clientsocket.recv(1024)
            msg = pickle.loads(msg)

            if msg["FROM"] == msg["TO"]:
                msg_to_send = {"TO": f'{user}', "FROM": f'Server', "MSG": f'You send it to yourself.'}
                msg_to_send = pickle.dumps(msg_to_send)
                clientsocket.send(msg_to_send)
            else:
                for i, name in enumerate(self.clients):
                    if name[1] == msg["TO"]:
                        msg_to_send = pickle.dumps(msg)
                        name[0].send(msg_to_send)
                    # elif i == len(self.clients) - 1:
                    #     msg_to_send = {"TO": f'{user}', "FROM": f'Server', "MSG": f'Recipient do not exist.'}
                    #     msg_to_send = pickle.dumps(msg_to_send)
                    #     clientsocket.send(msg_to_send)


s = Server()
s.new_connection()
