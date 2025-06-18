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

# GUI Setup
root = tk.Tk()
root.title("YouTube Playlist Downloader")

tk.Label(root, text="Enter YouTube Playlist URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

folder_path = tk.StringVar()
tk.Button(root, text="Select Folder", command=select_folder).pack(pady=5)
tk.Label(root, textvariable=folder_path).pack(pady=5)

download_button = tk.Button(root, text="Download Playlist", command=download_playlist)
download_button.pack(pady=5)

cancel_button = tk.Button(root, text="Cancel Download", command=cancel_download_action)
cancel_button.pack(pady=5)

play_button = tk.Button(root, text="Play Video", command=play_video)
play_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
