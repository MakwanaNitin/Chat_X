import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# File path for the CSV
file_path = r'D:\Computer_Programs\Python\Some_What_Big_Programs\Mini_Project\Database\User.csv'

# Function to check login credentials


def login_check_up():
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "User data file not found.")
        return

    df = pd.read_csv(file_path)
    username = username_entry.get()
    password = password_entry.get()

    if username in df['username'].values:
        user_password = df[df['username'] == username]['password'].values
        if user_password and user_password[0] == password:
            result_label.config(text="Login successful!", fg="green")
        else:
            result_label.config(text="Invalid username or password.", fg="red")
    else:
        result_label.config(text="Invalid username or password.", fg="red")

# Function to register new user


def register_user():
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['username', 'password'])

    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    if new_username in df['username'].values:
        messagebox.showerror("Error", "Username already exists.")
    else:
        new_user_df = pd.DataFrame(
            [{'username': new_username, 'password': new_password}])
        df = pd.concat([df, new_user_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", "Registration successful!")
        show_login()

# Function to show registration frame


def show_registration():
    login_frame.pack_forget()
    registration_frame.pack(fill='both', expand=True)

# Function to show login frame


def show_login():
    registration_frame.pack_forget()
    login_frame.pack(fill='both', expand=True)


root = tk.Tk()
root.title("DarkRose")
root.iconbitmap(
    r"D:\Computer_Programs\Python\Some_What_Big_Programs\Mini_Project\Logo\Logo.png")
root.resizable(0,0)


# Create frames for login and registration
login_frame = tk.Frame(root)
registration_frame = tk.Frame(root)

# Login Frame
username_label = tk.Label(login_frame, text="Username", width=20, height=2)
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_frame, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password", width=20, height=2)
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.grid(row=1, column=1, padx=10, pady=10)




login_button = tk.Button(login_frame, text="Login",
                         width=20, height=2, command=login_check_up)
login_button.grid(row=2, column=0,columnspan=2, padx=10, pady=10)

register_link = tk.Button(login_frame, text="Register" , width=20, height=2,
                          command=show_registration)
register_link.grid(row=3, column=0,columnspan=2, padx=10, pady=10)



result_label = tk.Label(login_frame, text="", width=20, height=2)
result_label.grid(row=3, column=1, padx=10, pady=10)
# Registration Frame
new_username_label = tk.Label(
    registration_frame, text="Username", width=20, height=2)
new_username_label.grid(row=0, column=0, padx=10, pady=10)

new_username_entry = tk.Entry(registration_frame, width=30)
new_username_entry.grid(row=0, column=1, padx=10, pady=10)

new_password_label = tk.Label(
    registration_frame, text="Password", width=20, height=2)
new_password_label.grid(row=1, column=0, padx=10, pady=10)

new_password_entry = tk.Entry(registration_frame, show="*", width=30)
new_password_entry.grid(row=1, column=1, padx=10, pady=10)




register_button = tk.Button(
    registration_frame, text="Register", width=20, height=2, command=register_user)
register_button.grid(row=2, column=0,columnspan=2, padx=10, pady=10)

login_link = tk.Button(
    registration_frame, text="Back to Login", command=show_login)
login_link.grid(row=3, column=0, padx=10, pady=10,columnspan=2)




# Show login frame initially
login_frame.pack(fill='both', expand=True)

# Show registration frame
registration_frame.pack_forget()

# Make the root loop till it stops
root.mainloop()