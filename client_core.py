import socket
import threading


class ClientCore:
    def __init__(self, host, port, nickname, update_chat_callback):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.update_chat_callback = update_chat_callback
        self.client_socket = None
        self.running = False

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.running = True
        # Send the nickname to the server upon connecting
        self.send(self.nickname)
        threading.Thread(target=self.receive).start()

    def send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def receive(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.update_chat_callback(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.running = False

    def disconnect(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
