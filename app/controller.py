from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
import os

class Controller:
    """Manages the interaction between the model and view."""

    def __init__(self, model, view):
        """Initialise the Controller with model and view instances."""
        self.model = model
        self.view = view
        self.setup_connections()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_recording_time)
        self.recording = False
        self.save_folder = os.getcwd()  # Default to current working directory

    def setup_connections(self):
        """Set up signal-slot connections between view elements and controller methods."""
        self.view.recordPushButton.clicked.connect(self.toggle_recording)
        self.view.folderPushButton.clicked.connect(self.select_save_folder)
        self.view.populate_mic_combo_box(self.model.get_available_devices())

    def toggle_recording(self):
        """Toggle between starting and stopping the recording."""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start the audio recording process."""
        device_index = self.view.get_selected_device_index()
        self.model.start_recording(device_index)
        self.recording = True
        self.view.set_record_button_text("Stop")
        self.view.set_folder_button_enabled(False)
        self.update_timer.start(100)  # Update every 100 ms

    def stop_recording(self):
        """Stop the audio recording process and save the recording."""
        self.model.stop_recording()
        self.recording = False
        self.view.set_record_button_text("Start")
        self.view.set_folder_button_enabled(True)
        self.update_timer.stop()
        self.save_recording()

    def update_recording_time(self):
        """Update the displayed recording time in the view."""
        elapsed_time = self.model.get_recording_time()
        minutes, seconds = divmod(int(elapsed_time), 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.view.set_time_label(time_str)

    def save_recording(self):
        """Save the recorded audio to a file."""
        timestamp = self.model.get_timestamp()
        filename = f"recording_{timestamp}.wav"
        full_path = os.path.join(self.save_folder, filename)
        self.model.save_recording(full_path)

    def select_save_folder(self):
        """Open a dialog for the user to select a folder for saving recordings."""
        folder = QFileDialog.getExistingDirectory(self.view, "Select Folder for Saving Recordings")
        if folder:
            self.save_folder = folder
            self.view.update_folder_button_tooltip(folder)