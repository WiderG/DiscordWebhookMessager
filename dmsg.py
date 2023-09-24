import tkinter as tk
from tkinter import messagebox
import requests
import tempfile
import os
import subprocess  # Import the subprocess module

# Color constants for Discord-like color scheme
BACKGROUND_COLOR = "#36393f"  # Dark gray background
TEXT_COLOR = "#ffffff"        # White text
BUTTON_COLOR = "#7289da"      # Discord blue
RED_COLOR = "#ff0000"         # Red color for cache clear
TEXTBOX_BACKGROUND_COLOR = "#202225"  # Discord-like text box background color

CACHE_FILE = os.path.join(tempfile.gettempdir(), "WWH_Webhooks")

def send_message(event=None):
    webhook_url = webhook_entry.get()
    message = message_entry.get()

    # Apply formatting tags based on button clicks
    if bold_var.get():
        message = f"**{message}**"
    if italic_var.get():
        message = f"*{message}*"
    if underline_var.get():
        message = f"__{message}__"

    payload = {
        "content": message,
        "tts": False,
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            status_label.config(text="Message sent successfully!", fg="green")
            save_webhook_to_cache(webhook_url)  # Save the webhook URL to cache
            message_entry.delete(0, tk.END)  # Clear the message entry box
        else:
            status_label.config(text="Error: Unable to send message", fg="red")
    except requests.exceptions.MissingSchema:
        status_label.config(text="Error: Invalid webhook URL", fg="red")
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Display the error in a message box

def save_webhook_to_cache(webhook_url):
    with open(CACHE_FILE, "w") as cache_file:
        cache_file.write(webhook_url)

def load_webhook_from_cache():
    try:
        with open(CACHE_FILE, "r") as cache_file:
            return cache_file.read().strip()
    except FileNotFoundError:
        return ""

def clear_cache():
    confirmation = messagebox.askyesno("Clear Cache", "Are you sure you want to clear the cache?", icon='warning')
    if confirmation:
        try:
            os.remove(CACHE_FILE)
            status_label.config(text="Cache Cleared", fg=RED_COLOR)  # Display "Cache Cleared" in red
            messagebox.showinfo("Cache Cleared", "Cache cleared successfully!", icon='info')
            webhook_entry.delete(0, tk.END)  # Clear the webhook input box
        except FileNotFoundError:
            messagebox.showinfo("Cache Cleared", "Cache is already empty.", icon='info')

# Function to open the Utilities window
def open_utilities_window():
    utilities_window = tk.Toplevel(app)
    utilities_window.title("Utilities")
    utilities_window.configure(bg=BACKGROUND_COLOR)

    # Close program button function
    def close_program():
        app.quit()  # Quit the main application

    close_button = tk.Button(utilities_window, text="Close Program", command=close_program, bg=BUTTON_COLOR, fg=TEXT_COLOR, borderwidth=0, relief=tk.RAISED, padx=10, pady=5, highlightthickness=0)
    close_button.pack(pady=1)  # Add a 1mm gap below the button

    # Open cache location button function
    def open_cache_location():
        cache_dir = os.path.dirname(CACHE_FILE)
        subprocess.Popen(["explorer", cache_dir])  # Open the cache directory in Explorer

    open_cache_button = tk.Button(utilities_window, text="Open Cache Location", command=open_cache_location, bg=BUTTON_COLOR, fg=TEXT_COLOR, borderwidth=0, relief=tk.RAISED, padx=10, pady=5, highlightthickness=0)
    open_cache_button.pack(pady=1)  # Add a 1mm gap below the button

    # Display cache file name
    cache_filename_label = tk.Label(utilities_window, text=f"Cache File: {os.path.basename(CACHE_FILE)}", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    cache_filename_label.pack(pady=1)  # Add a 1mm gap below the label

# Create the main application window
app = tk.Tk()
app.title("Discord Webhook Messenger")  # Change the window title
app.configure(bg=BACKGROUND_COLOR)  # Set background color

# Load the cached webhook URL, if available
cached_webhook_url = load_webhook_from_cache()

# Webhook URL Entry
webhook_label = tk.Label(app, text="Webhook URL:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
webhook_label.pack()
webhook_entry = tk.Entry(app, width=60, bg=TEXTBOX_BACKGROUND_COLOR, fg=TEXT_COLOR)
webhook_entry.pack()
webhook_entry.insert(0, cached_webhook_url)  # Populate the entry with the cached URL

# Message Entry
message_label = tk.Label(app, text="Message:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
message_label.pack()
message_entry = tk.Entry(app, width=60, bg=TEXTBOX_BACKGROUND_COLOR, fg=TEXT_COLOR)
message_entry.pack()
message_entry.bind('<Return>', send_message)  # Bind Enter key to send_message function

# Formatting Buttons
formatting_frame = tk.Frame(app, bg=BACKGROUND_COLOR)
formatting_frame.pack(side=tk.BOTTOM, anchor=tk.W)

bold_var = tk.BooleanVar()
bold_button = tk.Checkbutton(formatting_frame, text="Bold", variable=bold_var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BACKGROUND_COLOR)  # Make the check button tick more readable
bold_button.grid(row=0, column=0, padx=5, pady=1, sticky=tk.W)  # Add a 1mm gap above and below the button

italic_var = tk.BooleanVar()
italic_button = tk.Checkbutton(formatting_frame, text="Italic", variable=italic_var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BACKGROUND_COLOR)  # Make the check button tick more readable
italic_button.grid(row=0, column=1, padx=5, pady=1, sticky=tk.W)  # Add a 1mm gap above and below the button

underline_var = tk.BooleanVar()
underline_button = tk.Checkbutton(formatting_frame, text="Underline", variable=underline_var, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, selectcolor=BACKGROUND_COLOR)  # Make the check button tick more readable
underline_button.grid(row=0, column=2, padx=5, pady=1, sticky=tk.W)  # Add a 1mm gap above and below the button

# Send Button
send_button = tk.Button(app, text="Send Message", command=send_message, bg=BUTTON_COLOR, fg=TEXT_COLOR, borderwidth=0, relief=tk.RAISED, padx=10, pady=5, highlightthickness=0)
send_button.pack(pady=1)  # Add a 1mm gap below the button

# Clear Cache Button
clear_cache_button = tk.Button(app, text="Clear Cache", command=clear_cache, bg=RED_COLOR, fg=TEXT_COLOR, borderwidth=0, relief=tk.RAISED, padx=10, pady=5, highlightthickness=0)
clear_cache_button.pack(pady=1)  # Add a 1mm gap below the button

# Utilities Button (Opens Utilities window)
utilities_button = tk.Button(app, text="Utilities", command=open_utilities_window, bg=BUTTON_COLOR, fg=TEXT_COLOR, borderwidth=0, relief=tk.RAISED, padx=10, pady=5, highlightthickness=0)
utilities_button.pack(pady=1)  # Add a 1mm gap below the button

# Status Label
status_label = tk.Label(app, text="", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
status_label.pack()

# Made in the UK Label
made_in_uk_label = tk.Label(app, text="Made in the UK by Wider", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, anchor="se")
made_in_uk_label.pack(side=tk.RIGHT, padx=10, pady=10)  # Add 10 pixels of padding to the bottom right corner

# Start the GUI application
app.mainloop()
