"""
YouTube Playlist Downloader Test
Phase 1 Source Code
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Description:
This test file implements basic unit testing for the main YouTube Playlist Downloader functionality.

Authors:
- Group 3 – CMSC 495 Capstone Project (University of Maryland Global Campus)

Last Updated: July 2025
License: For educational use only.
"""
import unittest
from unittest.mock import patch
import tkinter as tk
import sys
import os

# Temporarily append the project file to make importing easier
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playlist_downloader_phase1 import PlaylistDownloader

# Extends this class from TestCase for assertion access, etc.
class TestPlaylistDownloader(unittest.TestCase):

    def setUp(self):
        """Initialize baseline objects and conditions to execute tests"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = PlaylistDownloader(self.root)

    def tearDown(self):
        """Clean up test artifacts"""
        self.root.destroy()

    @patch('tkinter.filedialog.askdirectory', return_value='C:/test-folder')
    def test_select_folder_sets_path(self, mock_askdirectory):
        """Validates the folder path is correctly set to the directory selected by the user"""
        self.app.select_folder()
        self.assertEqual(self.app.folder_path.get(), 'C:/test-folder')
    
    @patch('tkinter.messagebox.showinfo')
    def test_cancel_download_action_sets_flag(self, mock_showinfo):
        """Validates the download cancellation flag is set when button is selected"""
        self.app.cancel_download = False
        self.app.cancel_download_action()
        self.assertTrue(self.app.cancel_download)
        # Suppress the dialog box for the test, but validate it was called
        mock_showinfo.assert_called()
