"""
YouTube Playlist Downloader
Phase 1 Source Code
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Description:
This Python application provides a user-friendly GUI for downloading all videos
in a YouTube playlist using pytubefix and tkinter. It supports folder selection,
progress tracking, cancellation, and autoplay of the first downloaded video.

Phase 1 Features:
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
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytubefix import Playlist

class PlaylistDownloader:
    """Class that encapsulates the GUI and core functionality of the playlist downloader."""

    def __init__(self, root):
        """Initializes the GUI window, state variables, and launches setup."""
        self.root = root
        self.cancel_download = False
        self.folder_path = tk.StringVar()
        self.clapper_board = "\U0001F3AC"  # symbol
        self.setup_gui()

    def setup_gui(self):
        """Creates the complete GUI layout using tkinter widgets."""
        self.root.title(f"{self.clapper_board} YouTube Playlist Downloader {self.clapper_board}")
        self.root.configure(bg="#87CEEB")  # Sky blue background

        # App Title
        tk.Label(self.root, text=f"{self.clapper_board} YouTube Playlist Downloader {self.clapper_board}",
                 font=("Arial", 18, "bold"), bg="#87CEEB", fg="black").pack(pady=10)

        # Playlist URL Entry
        tk.Label(self.root, text="Enter YouTube Playlist URL:",
                 font=("Arial", 12, "bold"), bg="#87CEEB", fg="black").pack()
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        # Folder Selection Button
        tk.Button(self.root, text="Select Folder", command=self.select_folder,
                  font=("Arial", 12, "bold"), bg="#FFD700", fg="black").pack(pady=5)

        # Folder Path Display
        tk.Label(self.root, textvariable=self.folder_path,
                 font=("Arial", 12, "bold"), bg="#87CEEB", fg="black").pack(pady=5)

        # Download Button
        tk.Button(self.root, text="Download Playlist", command=self.download_playlist,
                  font=("Arial", 12, "bold"), bg="#32CD32", fg="white").pack(pady=5)

        # Cancel Button
        tk.Button(self.root, text="Cancel Download", command=self.cancel_download_action,
                  font=("Arial", 12, "bold"), bg="#FF4500", fg="white").pack(pady=5)

        # Play Video Button
        tk.Button(self.root, text="Play Video", command=self.play_video,
                  font=("Arial", 12, "bold"), bg="#1E90FF", fg="white").pack(pady=5)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Footer
        tk.Label(self.root, text="© CMSC 495 6982 Computer Science Capstone - Group 3",
                 font=("Arial", 10, "italic"), bg="#87CEEB", fg="black").pack(pady=10)

    def select_folder(self):
        """Opens a directory selection dialog and stores the selected folder path."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def cancel_download_action(self):
        """Sets a flag to cancel the current download loop gracefully."""
        self.cancel_download = True
        messagebox.showinfo("Canceled", "Download canceled!")

    def play_video(self):
        """Attempts to play the first .mp4 video file in the selected folder."""
        save_path = self.folder_path.get()
        if not save_path:
            messagebox.showerror("Error", "Please select a download folder first.")
            return

        files = [f for f in os.listdir(save_path) if f.endswith(".mp4")]
        if files:
            os.startfile(os.path.join(save_path, files[0]))
        else:
            messagebox.showerror("Error", "No downloaded videos found.")

    def download_playlist(self):
        """Validates inputs and launches a thread to download all videos in the playlist."""
        self.cancel_download = False
        url = self.url_entry.get()
        save_path = self.folder_path.get()

        if not url or not save_path:
            messagebox.showerror("Error", "Please provide all required inputs.")
            return

        try:
            playlist = Playlist(url)
            self.progress_bar["maximum"] = len(playlist.video_urls)
            messagebox.showinfo("Downloading", f"Downloading playlist: '{playlist.title}'...")

            # Function to run the download loop in a separate thread
            def download_thread():
                for index, video in enumerate(playlist.videos):
                    if self.cancel_download:
                        break

                    # Retrieve and download the best progressive stream
                    stream = video.streams.filter(progressive=True, file_extension="mp4").first()
                    video_path = stream.download(output_path=save_path)

                    # Update progress bar
                    self.progress_bar["value"] = index + 1
                    self.root.update_idletasks()

                    # Auto-play the first video
                    if index == 0:
                        os.startfile(video_path)

                if not self.cancel_download:
                    messagebox.showinfo("Success", f"Download complete!\nVideos saved in '{save_path}'.")

            threading.Thread(target=download_thread).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {e}")

# Entry point of the program
if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistDownloader(root)
    root.mainloop()
