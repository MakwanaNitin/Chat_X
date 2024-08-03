import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import simpledialog
import threading
import socket

class AdminClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        self.nickname = "admin:Admin"
        self.socket.send(self.nickname.encode('utf-8'))

        self.gui_done = False
        self.running = True
        self.nicknames = {}

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tk.Tk()
        self.win.title("Admin Panel - BlackRose")

        self.chat_label = tk.Label(
            self.win, text="Admin Chat", font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.user_list_label = tk.Label(
            self.win, text="Online Users", font=("Arial", 12))
        self.user_list_label.pack(padx=20, pady=5)

        self.user_list_area = scrolledtext.ScrolledText(self.win, height=10)
        self.user_list_area.pack(padx=20, pady=5)
        self.user_list_area.config(state='disabled')

        self.msg_label = tk.Label(self.win, text="Message", font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
        self.input_area.bind('<Return>', self._send_message_with_enter)

        self.send_button = tk.Button(
            self.win, text="Send", command=self.send_message)
        self.send_button.pack(padx=20, pady=5)

        self.kick_button = tk.Button(
            self.win, text="Kick User", command=self.kick_user)
        self.kick_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def _send_message_with_enter(self, event):
        self.send_message()
        return "break"

    def send_message(self):
        message = self.input_area.get("1.0", "end").strip()
        self.socket.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == 'NICKNAME':
                    self.socket.send(self.nickname.encode('utf-8'))
                elif message.startswith('USERLIST'):
                    self.nicknames = {}
                    users = message[8:].split(',')
                    for user in users:
                        self.nicknames[user] = user
                    if self.gui_done:
                        self.update_user_list()
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message + '\n')
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.socket.close()
                break

    def update_user_list(self):
        self.user_list_area.config(state='normal')
        self.user_list_area.delete('1.0', 'end')
        for nickname in self.nicknames.values():
            self.user_list_area.insert('end', f'{nickname}\n')
        self.user_list_area.config(state='disabled')

    def kick_user(self):
        user_to_kick = simpledialog.askstring(
            "Kick User", "Enter the nickname of the user to kick:", parent=self.win)
        if user_to_kick in self.nicknames.values():
            self.socket.send(f'KICK {user_to_kick}'.encode('utf-8'))
            for client, nickname in list(self.nicknames.items()):
                if nickname == user_to_kick:
                    del self.nicknames[client]
                    break
            self.update_user_list()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.socket.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5555
    admin_client = AdminClient(HOST, PORT)