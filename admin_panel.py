import tkinter as tk
from tkinter import messagebox
import csv
import os
from admin_core import AdminCore

ADMIN_CSV_FILE = 'Database\\admin.csv'
REFRESH_INTERVAL = 5000  # milliseconds


def ensure_csv_file_exists():
    """Ensure the CSV file exists and has the correct fields."""
    if not os.path.exists(ADMIN_CSV_FILE):
        with open(ADMIN_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password'])
    else:
        with open(ADMIN_CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header != ['username', 'password']:
                with open(ADMIN_CSV_FILE, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['username', 'password'])


def read_admin_csv():
    """Read admin users from the CSV file."""
    ensure_csv_file_exists()
    users = {}
    with open(ADMIN_CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 2:
                users[row[0]] = row[1]
    return users


def write_admin_csv(username, password):
    """Write a new admin user to the CSV file."""
    ensure_csv_file_exists()
    with open(ADMIN_CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])


def show_login_panel():
    login_root = tk.Tk()
    login_root.title("Admin Login")

    users = read_admin_csv()

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            login_root.destroy()
            open_admin_panel()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid credentials. Please try again.")

    def show_registration_panel():
        login_root.destroy()
        create_registration_panel()

    tk.Label(login_root, text="Username").pack(padx=20, pady=5)
    username_entry = tk.Entry(login_root)
    username_entry.pack(padx=20, pady=5)

    tk.Label(login_root, text="Password").pack(padx=20, pady=5)
    password_entry = tk.Entry(login_root, show="*")
    password_entry.pack(padx=20, pady=5)

    tk.Button(login_root, text="Login", command=authenticate).pack(pady=10)
    tk.Button(login_root, text="Register",
              command=show_registration_panel).pack(pady=10)
    login_root.mainloop()


def create_registration_panel():
    registration_root = tk.Tk()
    registration_root.title("Admin Registration")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            users = read_admin_csv()
            if username in users:
                messagebox.showerror("Registration Failed",
                                     "Username already exists.")
            else:
                write_admin_csv(username, password)
                messagebox.showinfo("Registration Successful",
                                    "Admin account created!")
                registration_root.destroy()
                show_login_panel()
        else:
            messagebox.showerror("Registration Failed",
                                 "Please fill in both fields.")

    tk.Label(registration_root, text="Username").pack(padx=20, pady=5)
    username_entry = tk.Entry(registration_root)
    username_entry.pack(padx=20, pady=5)

    tk.Label(registration_root, text="Password").pack(padx=20, pady=5)
    password_entry = tk.Entry(registration_root, show="*")
    password_entry.pack(padx=20, pady=5)

    tk.Button(registration_root, text="Register",
              command=register).pack(pady=10)
    tk.Button(registration_root, text="Back to Login", command=lambda: [
              registration_root.destroy(), show_login_panel()]).pack(pady=10)
    registration_root.mainloop()


def open_admin_panel():
    admin_root = tk.Tk()
    admin_root.title("Admin Panel")

    # Create an instance of AdminCore
    # Use your server's host and port
    admin_core = AdminCore("localhost", 5555,
                           on_active_users_update,
                           on_chat_logs_update,
                           on_error_logs_update)
    admin_core.connect_to_server()

    def on_active_users_update(users):
        user_list.delete(0, tk.END)
        for user in users:
            user_list.insert(tk.END, user)

    def on_chat_logs_update(logs):
        log_text.configure(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "\n".join(logs))
        log_text.configure(state=tk.DISABLED)

    def on_error_logs_update(logs):
        error_log_text.configure(state=tk.NORMAL)
        error_log_text.delete(1.0, tk.END)
        error_log_text.insert(tk.END, "\n".join(logs))
        error_log_text.configure(state=tk.DISABLED)

    user_list_label = tk.Label(admin_root, text="Active Users")
    user_list = tk.Listbox(admin_root)
    user_list_label.pack()
    user_list.pack()

    log_label = tk.Label(admin_root, text="Chat Logs")
    global log_text
    log_text = tk.Text(admin_root, state=tk.DISABLED)
    log_label.pack()
    log_text.pack()

    error_log_label = tk.Label(admin_root, text="Error Logs")
    global error_log_text
    error_log_text = tk.Text(admin_root, state=tk.DISABLED)
    error_log_label.pack()
    error_log_text.pack()

    def refresh_all():
        admin_core.request_active_users()
        admin_core.request_chat_logs()
        admin_core.request_error_logs()
        admin_root.after(REFRESH_INTERVAL, refresh_all)

    refresh_all()
    admin_root.mainloop()


if __name__ == "__main__":
    show_login_panel()
