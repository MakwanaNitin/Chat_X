import socket
import threading
import tkinter as tk
from tkinter import messagebox
import time


clients = []
Chat_file = r'Database\\Chats.txt'
Log_For_Connections = r'Database\\LogOfConnecting.txt'

def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode('utf-8')
    print(f"{nickname} connected from {addr}.")
    clients.append(client_socket)
    client_socket.send("Welcome to the chat!".encode('utf-8'))
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                #to have messages stored in Chats.txt file.
                with open(Chat_file, 'a') as file:
                    file.write(f"{nickname}: {message}\n")

                # print(f"{nickname}: {message}")
                broadcast(f"{nickname}: {message}", client_socket)
            else:
                remove(client_socket)
                break
        except:
            remove(client_socket)
            break


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)


def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    #to have this stored on the LogsOfConnection.txt file with the time and date using module.
    with open(Log_For_Connections, 'a') as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{current_time} - {host}:{port} - {len(clients)}")


    # print(f"Server started on {host}:{port}, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(
            client_socket, addr)).start()


def show_server_info(host, port):
    root = tk.Tk()
    root.title("Server Info")
    label = tk.Label(root, text=f"Server running on {host}:{port}")
    label.pack(padx=20, pady=20)
    tk.Button(root, text="OK", command=root.destroy).pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5555
    threading.Thread(target=start_server, args=(HOST, PORT)).start()
    show_server_info(HOST, PORT)
