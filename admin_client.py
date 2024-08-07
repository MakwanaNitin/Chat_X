import tkinter as tk
from tkinter import colorchooser, messagebox


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.colors = {}
        self.theme = "light"  # Default theme

        # Initialize GUI components
        self.chat_frame = tk.Frame(root)
        self.chat_label = tk.Label(self.chat_frame, text="Chat")
        self.text_area = tk.Text(self.chat_frame)
        self.msg_label = tk.Label(self.chat_frame, text="Messages")
        self.input_area = tk.Entry(self.chat_frame)

        self.chat_frame.pack()
        self.chat_label.pack()
        self.text_area.pack()
        self.msg_label.pack()
        self.input_area.pack()

        # Setup initial theme
        self._apply_theme()

        # Example button to change theme
        self.theme_button = tk.Button(
            root, text="Set Custom Theme", command=self.custom_theme)
        self.theme_button.pack()

        # Button to open Admin Panel
        self.admin_button = tk.Button(
            root, text="Open Admin Panel", command=self.open_admin_panel)
        self.admin_button.pack()

    def custom_theme(self):
        # Allow users to set custom colors
        bg_color = colorchooser.askcolor(title="Choose Background Color")[1]
        fg_color = colorchooser.askcolor(title="Choose Foreground Color")[1]
        textarea_bg_color = colorchooser.askcolor(
            title="Choose Textarea Background Color")[1]
        textarea_fg_color = colorchooser.askcolor(
            title="Choose Textarea Foreground Color")[1]

        if bg_color and fg_color and textarea_bg_color and textarea_fg_color:
            self.colors["custom"] = {
                "bg": bg_color,
                "fg": fg_color,
                "textarea_bg": textarea_bg_color,
                "textarea_fg": textarea_fg_color
            }
            self.theme = "custom"
            self._apply_theme()

    def _apply_theme(self):
        # Define the default themes
        colors = {
            "light": {
                "bg": "lightgray",
                "fg": "black",
                "textarea_bg": "white",
                "textarea_fg": "black"
            },
            "dark": {
                "bg": "black",
                "fg": "white",
                "textarea_bg": "gray",
                "textarea_fg": "white"
            },
            "custom": {
                "bg": "lightgray",
                "fg": "black",
                "textarea_bg": "white",
                "textarea_fg": "black"
            }
        }

        # Update with custom colors if any
        colors.update(self.colors)

        # Apply the selected theme colors
        theme_colors = colors.get(self.theme, colors["light"])
        self.chat_frame.configure(bg=theme_colors["bg"])
        self.chat_label.configure(bg=theme_colors["bg"], fg=theme_colors["fg"])
        self.text_area.configure(
            bg=theme_colors["textarea_bg"], fg=theme_colors["textarea_fg"])
        self.msg_label.configure(bg=theme_colors["bg"], fg=theme_colors["fg"])
        self.input_area.configure(
            bg=theme_colors["textarea_bg"], fg=theme_colors["textarea_fg"])

    def open_admin_panel(self):
        AdminPanel(self)


class AdminPanel:
    def __init__(self, chat_app):
        self.chat_app = chat_app
        self.root = tk.Toplevel(chat_app.root)
        self.root.title("Admin Panel")

        # Add components for admin functionalities
        self.user_list_label = tk.Label(self.root, text="User List")
        self.user_list = tk.Listbox(self.root)

        self.log_label = tk.Label(self.root, text="Chat Logs")
        self.log_text = tk.Text(self.root, state=tk.DISABLED)

        self.theme_label = tk.Label(self.root, text="Theme Management")
        self.theme_button = tk.Button(
            self.root, text="Set Custom Theme", command=chat_app.custom_theme)

        self.user_list_label.pack()
        self.user_list.pack()
        self.log_label.pack()
        self.log_text.pack()
        self.theme_label.pack()
        self.theme_button.pack()

        # Dummy data for demonstration
        self._populate_dummy_data()

    def _populate_dummy_data(self):
        # Populate the user list with dummy data
        users = ["User1", "User2", "User3"]
        for user in users:
            self.user_list.insert(tk.END, user)

        # Populate the chat logs with dummy data
        logs = [
            "User1: Hello!",
            "User2: Hi there!",
            "User3: Good morning!"
        ]
        self.log_text.configure(state=tk.NORMAL)
        for log in logs:
            self.log_text.insert(tk.END, log + "\n")
        self.log_text.configure(state=tk.DISABLED)


# Create the main application window
root = tk.Tk()
app = ChatApp(root)
root.mainloop()
