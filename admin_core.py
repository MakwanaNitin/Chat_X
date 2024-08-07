import socket
import threading
import json


class AdminCore:
    def __init__(self, host, port, active_users_callback, chat_logs_callback, error_logs_callback):
        self.host = host
        self.port = port
        self.active_users_callback = active_users_callback
        self.chat_logs_callback = chat_logs_callback
        self.error_logs_callback = error_logs_callback
        self.client_socket = None
        self.running = False

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.running = True
            threading.Thread(target=self.receive).start()
        except Exception as e:
            print(f"Connection failed: {e}")

    def send(self, msg):
        if self.client_socket:
            self.client_socket.send(json.dumps(msg).encode('utf-8'))

    def receive(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    if message['type'] == 'active_users':
                        self.active_users_callback(message['data'])
                    elif message['type'] == 'chat_logs':
                        self.chat_logs_callback(message['data'])
                    elif message['type'] == 'error_logs':
                        self.error_logs_callback(message['data'])
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False

    def disconnect(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()

    def request_active_users(self):
        self.send({'action': 'get_active_users'})

    def request_chat_logs(self):
        self.send({'action': 'get_chat_logs'})

    def request_error_logs(self):
        self.send({'action': 'get_error_logs'})
