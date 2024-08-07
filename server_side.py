import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

clients = []
Chat_file = r'Database\\Chats.txt'
Log_For_Connections = r'Database\\LogOfConnecting.txt'


def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode('utf-8')
    #store this above in logsOfConnection.txt
    with open(Log_For_Connections, 'a') as f:
        f.write(f"{nickname} connected from {addr}.")

    clients.append(client_socket)
    client_socket.send("Welcome to the chat!".encode('utf-8'))
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # to have messages stored in Chats.txt file.
                with open(Chat_file, 'a') as file:
                    file.write(f"{nickname}: {message}\n")

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
    # to have this stored on the LogsOfConnection.txt file with the time and date using module.
    with open(Log_For_Connections, 'a') as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{current_time} - {host}:{port} - {len(clients)
                                                       }\n" + "Waiting For Connections\n")

    while True:
        client_socket, addr = server.accept()
        # storing the connection data into the file named LogsOfConnection.txt.
        with open(Log_For_Connections, 'a') as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f'{current_time} : Connection from {addr}\n')

        threading.Thread(target=handle_client, args=(
            client_socket, addr)).start()


def copy_to_clipboard(text):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Now it stays on the clipboard after the window is closed
    root.destroy()


def show_server_info(host, port):
    root = tk.Tk()
    root.title("BlackRose Server Side")
    root.tk.call("wm", "iconphoto", root._w,
                 tk.PhotoImage(file="Logo\\Server_Logo.png"))
    
    def copy_info_IP():
        copy_to_clipboard(f"{host}")
        messagebox.showinfo(
            "Copied", "IP address copied to clipboard.")
        
    label_IP = tk.Label(root, text=f"Server running on {host}")
    label_IP.pack(padx=20, pady=20)
    copy_button_IP = tk.Button(root, text="Copy-IP", command=copy_info_IP)
    copy_button_IP.pack(pady=10)

    def copy_info_port():
        copy_to_clipboard(f"{port}")
        messagebox.showinfo(
            "Copied", "Port copied to clipboard.")
    label_Port = tk.Label(root, text=f"Server Using Port: {port}")
    label_Port.pack(padx=20,pady=20)
    copy_button_port = tk.Button(
        root, text="Copy-Port", command=copy_info_port)
    copy_button_port.pack(pady=10)

    
    # def copy_info_IP():
    #     copy_to_clipboard(f"{host}:{port}")
    #     messagebox.showinfo(
    #         "Copied", "IP address copied to clipboard.")
        
    # def copy_info_port():
    #     copy_to_clipboard(f"{host}:{port}")
    #     messagebox.showinfo(
    #         "Copied", "Port copied to clipboard.")


    tk.Button(root, text="End", command=root.destroy).pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5555
    threading.Thread(target=start_server, args=(HOST, PORT)).start()
    show_server_info(HOST, PORT)
