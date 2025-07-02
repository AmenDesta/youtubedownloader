"""
YouTube Playlist Downloader
Phase 1 Source Code
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Description:
This Python application provides a user-friendly GUI for downloading all videos
in a YouTube playlist using pytubefix and tkinter. It supports folder selection,
progress tracking, cancellation, and autoplay of the first downloaded video.

Features:
- Playlist URL input via GUI
- Output folder selection
- Real-time download progress bar
- Threaded download process to keep UI responsive
- Cancel functionality
- Auto playback of the first downloaded video (.mp4)

Authors:
- Group 3 – CMSC 495 Capstone Project (University of Maryland Global Campus)

Last Updated: July 2025
License: For educational use only.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytubefix import Playlist
import threading

cancel_download = False

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def cancel_download_action():
    global cancel_download
    cancel_download = True
    messagebox.showinfo("Canceled", "Download canceled!")

def play_video():
    save_path = folder_path.get()
    if not save_path:
        messagebox.showerror("Error", "Please select a download folder first.")
        return

    # Open the first downloaded video
    files = [f for f in os.listdir(save_path) if f.endswith(".mp4")]
    if files:
        first_video = os.path.join(save_path, files[0])
        os.startfile(first_video)
    else:
        messagebox.showerror("Error", "No downloaded videos found.")

def download_playlist():
    global cancel_download
    cancel_download = False

    url = url_entry.get()
    save_path = folder_path.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube playlist URL")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a download folder")
        return

    try:
        playlist = Playlist(url)

        progress_bar["maximum"] = len(playlist.video_urls)
        messagebox.showinfo("Downloading", f"Downloading playlist: '{playlist.title}'...")

        def download_videos():
            for index, video in enumerate(playlist.videos):
                if cancel_download:
                    break

                progress_bar["value"] = index + 1
                root.update_idletasks()

                print(f"Downloading '{video.title}'...")
                stream = video.streams.filter(progressive=True, file_extension="mp4").first()
                video_path = stream.download(output_path=save_path)

                if index == 0:  # Play the first video automatically
                    os.startfile(video_path)

            if not cancel_download:
                messagebox.showinfo("Success", f"Download complete! All videos saved in '{save_path}'.")

        threading.Thread(target=download_videos).start()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

# Define emoji as a variable (can be reused throughout)
clapper_board = "\U0001F3AC"

# GUI Setup
root = tk.Tk()
root.title(f"{clapper_board} YouTube Playlist Downloader {clapper_board}")

# Set background color
root.configure(bg="#87CEEB")  # Sky blue color

# App Title
app_title = tk.Label(root, text=f"{clapper_board} YouTube Playlist Downloader {clapper_board}",
                     font=("Arial", 18, "bold"), bg="#87CEEB", fg="black")
app_title.pack(pady=10)

tk.Label(root, text="Enter YouTube Playlist URL:", font=("Arial", 12, "bold"), bg="#87CEEB", fg="black").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

folder_path = tk.StringVar()
tk.Button(root, text="Select Folder", command=select_folder, font=("Arial", 12, "bold"), bg="#FFD700", fg="black").pack(pady=5)
tk.Label(root, textvariable=folder_path, font=("Arial", 12, "bold"), bg="#87CEEB", fg="black").pack(pady=5)

download_button = tk.Button(root, text="Download Playlist",command=download_playlist, font=("Arial", 12, "bold"), bg="#32CD32", fg="white")
download_button.pack(pady=5)

cancel_button = tk.Button(root, text="Cancel Download", command=cancel_download_action, font=("Arial", 12, "bold"), bg="#FF4500", fg="white")
cancel_button.pack(pady=5)

play_button = tk.Button(root, text="Play Video", command=play_video, font=("Arial", 12, "bold"), bg="#1E90FF", fg="white")
play_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Copyright Notice (Not Bold)
copyright_label = tk.Label(root, text="© CMSC 495 6982 Computer Science Capstone - Group 3", font=("Arial", 10, "italic"), bg="#87CEEB", fg="black")
copyright_label.pack(pady=10)

root.mainloop()
