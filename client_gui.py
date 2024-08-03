import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import colorchooser
from tkinter import font as tkfont
import pandas as pd
import os

from client_core import ClientCore

file_path = r'Database\\User.csv'
Log_file = r'Database\\Logs.csv'
Error_file = r'Database\\Error.txt'
Debugging_file = r'Database\\Debugging.txt'


class ClientGUI:
    def __init__(self):
        self.running = True
        self.client_core = None

        # Initialize the main Tkinter window
        self.root = tk.Tk()
        self.root.title("BlackRose")
        self.root.tk.call("wm", "iconphoto", self.root._w,
                          tk.PhotoImage(file="Logo\Logo.png"))
        # self.root.resizable(0, 0)

        # Create frames for login and registration
        self.login_frame = tk.Frame(self.root)
        self.registration_frame = tk.Frame(self.root)
        self.chat_frame = tk.Frame(self.root)

        # Pack all frames, only one will be visible at a time
        for frame in (self.login_frame, self.registration_frame, self.chat_frame):
            frame.grid(row=0, column=0, sticky='nsew')

        # Create a menu bar for navigation
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(
            label="Toggle Theme", command=self.toggle_theme)
        self.options_menu.add_command(
            label="Custom Theme", command=self.custom_theme)
        self.options_menu.add_command(
            label="Font Settings", command=self.font_settings)

        # Create font styles
        self.default_font = tkfont.Font(family="Arial", size=12)
        self.bold_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.italic_font = tkfont.Font(family="Arial", size=12, slant="italic")

        # Call methods to create widgets in each frame
        self.create_login_frame()
        self.create_registration_frame()
        self.create_chat_frame()

        # Show login frame initially
        self.show_frame(self.login_frame)

        # Start the main GUI loop
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def create_login_frame(self):
        ip_label = tk.Label(
            self.login_frame, text="Server IP", width=20, height=2)
        ip_label.grid(row=0, column=0, padx=10, pady=10)
        self.ip_entry = tk.Entry(self.login_frame, width=30)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)

        port_label = tk.Label(
            self.login_frame, text="Server Port", width=20, height=2)
        port_label.grid(row=1, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self.login_frame, width=30)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)

        username_label = tk.Label(
            self.login_frame, text="Username", width=20, height=2)
        username_label.grid(row=2, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)

        password_label = tk.Label(
            self.login_frame, text="Password", width=20, height=2)
        password_label.grid(row=3, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)

        login_button = tk.Button(
            self.login_frame, text="Login", width=20, height=2, command=self.login_check_up)
        login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        register_link = tk.Button(
            self.login_frame, text="Register", width=20, height=2, command=self.show_registration)
        register_link.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = tk.Label(
            self.login_frame, text="", width=30, height=2)
        self.result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_registration_frame(self):
        new_username_label = tk.Label(
            self.registration_frame, text="Username", width=20, height=2)
        new_username_label.grid(row=0, column=0, padx=10, pady=10)
        self.new_username_entry = tk.Entry(self.registration_frame, width=30)
        self.new_username_entry.grid(row=0, column=1, padx=10, pady=10)

        new_password_label = tk.Label(
            self.registration_frame, text="Password", width=20, height=2)
        new_password_label.grid(row=1, column=0, padx=10, pady=10)
        self.new_password_entry = tk.Entry(
            self.registration_frame, show="*", width=30)
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=10)

        register_button = tk.Button(
            self.registration_frame, text="Register", width=20, height=2, command=self.register_user)
        register_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        login_link = tk.Button(self.registration_frame, text="Back to Login",
                               width=20, height=2, command=self.show_login)
        login_link.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_chat_frame(self):
        self.chat_label = tk.Label(
            self.chat_frame, text="Chat:", bg="lightgray", fg="black")
        self.chat_label.config(font=self.default_font)
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            self.chat_frame, bg="white", fg="black", wrap=tk.WORD)
        self.text_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        self.text_area.config(state='disabled', font=self.default_font)

        self.msg_label = tk.Label(
            self.chat_frame, text="Message:", bg="lightgray", fg="black")
        self.msg_label.config(font=self.default_font)
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(
            self.chat_frame, height=3, bg="white", fg="black", wrap=tk.WORD)
        self.input_area.pack(padx=20, pady=5, fill=tk.X)
        self.input_area.bind(
            '<Return>', self._write_with_enter)  # Bind Enter key
        self.input_area.config(font=self.default_font)

        self.send_button = tk.Button(
            self.chat_frame, text="Send", command=self.write)
        self.send_button.config(font=self.default_font)
        self.send_button.pack(padx=20, pady=5)

    def login_check_up(self):
        # Check if the file exists
        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "User data file not found.")
            #to have this error stored in Error.txt file.
            with open("Error.txt", "a") as f:
                f.write("User data file not found.[login_check_up]\n")
            return

        # Attempt to read the CSV file
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "User data file is empty.")
            # to have this error stored in Error.txt file.
            with open("Error.txt", "a") as f:
                f.write("User data file is empty.[login_check_up]\n")
            return

        # Get username and password from the entries
        username = self.username_entry.get()
        password = self.password_entry.get()

        # # Debugging print statements
        # print(f"Trying to login with username: {
        #       username} and password: {password}")
        # print(f"Dataframe head: \n{df.head()}")


        #to have this all stored in the debugging.txt
        with open("debugging.txt", "a") as f:
            f.write(f"Trying to login with username: {username} and password: {password}\
                    \nDataframe head: \n{df.head()} \n")



        # Check if the username exists in the dataframe
        if username in df['username'].values:
            user_data = df[df['username'] == username]
            user_password = user_data['password'].values

            # Debugging print statements
            # print(f"Stored data for {username}: {user_data}")
            # print(f"Stored password for {username}: {user_password}")


            # to have this all stored in the debugging.txt
            with open("debugging.txt", "a") as f:
                f.write(f"Stored data for {username}: {user_data}\n")
                f.write(f"Stored password for {username}: {user_password}\n")

            

            if user_password and user_password[0] == password:
                self.nickname = username
                print(f"Login successful for {username}")
                self.start_chat()
            else:
                self.result_label.config(
                    text="Invalid username or password.", fg="red")
                print("Invalid password.")
        else:
            self.result_label.config(
                text="Invalid username or password.", fg="red")
            print("Invalid username.")

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # Check if the file exists
        if not os.path.isfile(file_path):
            # Create the file with headers if it does not exist
            with open(file_path, 'w') as file:
                file.write('username,password\n')

        # Attempt to read the CSV file
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=['username', 'password'])

        if new_username in df['username'].values:
            messagebox.showerror("Error", "Username already exists.")
            # to have this error stored in Error.txt file.
            with open("Error.txt", "a") as f:
                f.write(f"Error: Username {new_username} already exists.\n")

        else:
            df = df.append({'username': new_username,
                           'password': new_password}, ignore_index=True)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Registration successful.")
            # to have this all stored in the debugging.txt along with username and password.
            with open("debugging.txt", "a") as f:
                f.write(f"Stored data for {new_username}: {new_password}\n")
                # self.new_username_entry.delete(0, tk.END)
                # self.new_password_entry.delete(0, tk.END)
            self.show_login()

    def show_login(self):
        self.show_frame(self.login_frame)

    def show_registration(self):
        self.show_frame(self.registration_frame)

    def show_frame(self, frame):
        frame.tkraise()

    def start_chat(self):
        # Hide login and registration frames
        self.show_frame(self.chat_frame)

        # Set up the client core with the necessary parameters
        host = self.ip_entry.get()
        port = int(self.port_entry.get())
        nickname = self.username_entry.get()
        self.client_core = ClientCore(host, port, nickname, self.update_chat)
        self.client_core.connect_to_server()

    def update_chat(self, message):
        # Determine if the message is from the sender or the receiver
        if message.startswith(self.client_core.nickname + ":"):#the formatting of the sender and the receiver in the chatting
            alignment = "right"
            tag = "sender"
        else:
            alignment = "left"
            tag = "receiver"

        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n", tag)
        self.text_area.tag_configure(
            "sender", justify='right', foreground="blue")
        self.text_area.tag_configure(
            "receiver", justify='left', foreground="green")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def write(self):
        message = self.input_area.get("1.0", tk.END).strip()
        if message:
            self.client_core.send(message)
            self.input_area.delete("1.0", tk.END)
            self.update_chat(f"{self.client_core.nickname}: {message}")#this is for how the chat formating will look

    def _write_with_enter(self, event):
        self.write()
        return 'break'

    def stop(self):
        self.running = False
        if self.client_core:
            self.client_core.disconnect()
        self.root.quit()

    def toggle_theme(self):
        current_bg = self.chat_frame.cget("bg")
        if current_bg == "white":
            self.set_theme("dark")
        else:
            self.set_theme("light")

    def set_theme(self, theme):
        if theme == "dark":
            bg_color = "black"
            fg_color = "red"
        else:
            bg_color = "white"
            fg_color = "red"

        self.chat_frame.config(bg=bg_color)
        self.chat_label.config(bg=bg_color, fg=fg_color)
        self.text_area.config(bg=bg_color, fg=fg_color)
        self.msg_label.config(bg=bg_color, fg=fg_color)
        self.input_area.config(bg=bg_color, fg=fg_color)
        self.send_button.config(bg=bg_color, fg=fg_color)

    def custom_theme(self):
        bg_color = colorchooser.askcolor(title="Choose background color")[1]
        fg_color = colorchooser.askcolor(title="Choose text color")[1]
        self.chat_frame.config(bg=bg_color)
        self.chat_label.config(bg=bg_color, fg=fg_color)
        self.text_area.config(bg=bg_color, fg=fg_color)
        self.msg_label.config(bg=bg_color, fg=fg_color)
        self.input_area.config(bg=bg_color, fg=fg_color)
        self.send_button.config(bg=bg_color, fg=fg_color)

    def font_settings(self):
        font_settings_window = tk.Toplevel(self.root)
        font_settings_window.title("Font Settings")

        tk.Label(font_settings_window, text="Font Family:").grid(
            row=0, column=0)
        font_family_entry = tk.Entry(font_settings_window)
        font_family_entry.grid(row=0, column=1)

        tk.Label(font_settings_window, text="Font Size:").grid(row=1, column=0)
        font_size_entry = tk.Entry(font_settings_window)
        font_size_entry.grid(row=1, column=1)

        tk.Label(font_settings_window, text="Bold:").grid(row=2, column=0)
        bold_var = tk.BooleanVar()
        bold_check = tk.Checkbutton(font_settings_window, variable=bold_var)
        bold_check.grid(row=2, column=1)

        tk.Label(font_settings_window, text="Italic:").grid(row=3, column=0)
        italic_var = tk.BooleanVar()
        italic_check = tk.Checkbutton(
            font_settings_window, variable=italic_var)
        italic_check.grid(row=3, column=1)

        def apply_font_settings():
            font_family = font_family_entry.get() or "Arial"
            font_size = int(font_size_entry.get() or 12)
            weight = "bold" if bold_var.get() else "normal"
            slant = "italic" if italic_var.get() else "roman"
            new_font = (font_family, font_size, weight, slant)
            self.chat_label.config(font=new_font)
            self.text_area.config(font=new_font)
            self.msg_label.config(font=new_font)
            self.input_area.config(font=new_font)
            self.send_button.config(font=new_font)
            font_settings_window.destroy()

        apply_button = tk.Button(font_settings_window,
                                 text="Apply", command=apply_font_settings)
        apply_button.grid(row=4, column=0, columnspan=2)


if __name__ == "__main__":
    client = ClientGUI()
