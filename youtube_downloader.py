import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

download_folder = ""

def install_ytdlp():
    try:
        import yt_dlp
        status.set("yt-dlp detected ✔")
    except ImportError:
        status.set("Installing yt-dlp...")
        root.update()
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            status.set("yt-dlp installed ✔")
        except Exception as e:
            status.set("Failed to install yt-dlp")
            messagebox.showerror("Install Error", str(e))

def choose_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_label.config(text=folder)

def run_download():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not download_folder:
        messagebox.showerror("Error", "Please choose a download folder.")
        return

    status.set("Downloading...")
    root.update()

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", f"{download_folder}/%(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(cmd)
        status.set("Download complete ✔")
    except Exception as e:
        status.set("Download failed")
        messagebox.showerror("Error", str(e))

def start_download():
    threading.Thread(target=run_download).start()

# GUI
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x260")

status = tk.StringVar()
status.set("Ready")

tk.Label(root, text="YouTube URL").pack(pady=5)

url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Button(root, text="Choose Download Folder", command=choose_folder).pack(pady=5)

folder_label = tk.Label(root, text="No folder selected", wraplength=400)
folder_label.pack()

tk.Button(root, text="Download (Best Quality)", command=start_download).pack(pady=15)

tk.Label(root, textvariable=status).pack(pady=10)

install_ytdlp()

root.mainloop()