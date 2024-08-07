import socket
import threading

Error_file = "Database\\Error.txt"

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
                #save this inside the error_file.
                with open(Error_file, "a") as f:
                    f.write(f"Error receiving message: {e}\n [Client_core-file]")
                self.running = False

    def disconnect(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
