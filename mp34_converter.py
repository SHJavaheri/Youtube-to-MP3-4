import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from yt_dlp import YoutubeDL
import os

# Initialize the main application window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("480x500")
root.configure(bg="#2a2a2a")  # Dark background

download_format = tk.StringVar(value="mp4")  # Default to mp4
save_path = ""  # Variable to store the chosen directory

# Set custom styles for a modern look
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 11), foreground="#FFFFFF", background="#2a2a2a")
style.configure("TEntry", font=("Arial", 12), padding=10)
style.configure("TButton", font=("Arial", 10, "bold"), padding=10, foreground="#ffffff")

# Hover effect function for buttons
def on_enter(e):
    e.widget.config(background="#4CAF50", foreground="#ffffff")

def on_leave(e):
    e.widget.config(background="#333333", foreground="#ffffff")

# Function to select the save directory
def select_save_directory():
    global save_path
    save_path = filedialog.askdirectory()
    if save_path:
        save_path_label.config(text=f"Save Location: {save_path}", foreground="#A3BE8C")
    else:
        save_path_label.config(text="Save Location: Not selected", foreground="#D08770")

# Function to download the YouTube video
def download_video():
    global save_path
    url = url_entry.get()
    file_name = file_name_entry.get()
    file_format = download_format.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    if not file_name:
        messagebox.showerror("Error", "Please enter a file name.")
        return

    if not save_path:
        messagebox.showerror("Error", "Please select a save location.")
        return

    output_template = os.path.join(save_path, f"{file_name}.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best' if file_format == 'mp3' else 'best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if file_format == 'mp3' else {},
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"{file_format.upper()} downloaded as {file_name}.{file_format} in {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Main Frame
main_frame = tk.Frame(root, bg="#333333", bd=2, relief="groove", padx=15, pady=15)
main_frame.pack(pady=30, padx=20, fill="both")

# Title Label
title_label = tk.Label(main_frame, text="YouTube Downloader", font=("Arial", 16, "bold"), fg="#EBCB8B", bg="#333333")
title_label.pack(pady=10)

# YouTube Link Entry
tk.Label(main_frame, text="YouTube Link:", font=("Arial", 11), bg="#333333", fg="#D8DEE9").pack(pady=10, anchor="w")
url_entry = tk.Entry(main_frame, width=50, font=("Arial", 12), bd=0, highlightthickness=1, relief="solid")
url_entry.pack(pady=5)

# File Name Entry
tk.Label(main_frame, text="File Name:", font=("Arial", 11), bg="#333333", fg="#D8DEE9").pack(pady=10, anchor="w")
file_name_entry = tk.Entry(main_frame, width=50, font=("Arial", 12), bd=0, highlightthickness=1, relief="solid")
file_name_entry.pack(pady=5)

# Format Selection
tk.Label(main_frame, text="Format:", font=("Arial", 11), bg="#333333", fg="#D8DEE9").pack(pady=10, anchor="w")
format_frame = tk.Frame(main_frame, bg="#333333")
format_frame.pack(pady=5)
mp4_radio = ttk.Radiobutton(format_frame, text="MP4", variable=download_format, value="mp4")
mp4_radio.grid(row=0, column=0, padx=10)
mp3_radio = ttk.Radiobutton(format_frame, text="MP3", variable=download_format, value="mp3")
mp3_radio.grid(row=0, column=1, padx=10)

# Save location selection
save_path_label = tk.Label(main_frame, text="Save Location: Not selected", font=("Arial", 10), fg="#D08770", bg="#333333")
save_path_label.pack(pady=5, anchor="w")
select_dir_button = tk.Button(main_frame, text="Select Save Location", font=("Arial", 10, "bold"), command=select_save_directory, bg="#4CAF50", fg="#ffffff", bd=0, padx=10, pady=5)
select_dir_button.pack(pady=10)
select_dir_button.bind("<Enter>", on_enter)
select_dir_button.bind("<Leave>", on_leave)

# Download Button
download_button = tk.Button(main_frame, text="Download", font=("Arial", 12, "bold"), command=download_video, bg="#333333", fg="#ffffff", bd=0, padx=15, pady=10, relief="flat")
download_button.pack(pady=15)
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Run the app
root.mainloop()
