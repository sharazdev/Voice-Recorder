from PyQt5 import QtWidgets
from app_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main window class for the audio recorder application."""

    def __init__(self):
        """Initialise the MainWindow and set up the user interface."""
        super().__init__()
        self.setupUi(self)

    def set_record_button_text(self, text):
        """Set the text of the record button."""
        self.recordPushButton.setText(text)

    def set_time_label(self, time_str):
        """Set the text of the time label."""
        self.timeQLabel.setText(time_str)

    def populate_mic_combo_box(self, devices):
        """Populate the microphone combo box with available devices."""
        self.micComboBox.clear()
        for device in devices:
            self.micComboBox.addItem(device[1], device[0])

    def get_selected_device_index(self):
        """Get the index of the currently selected device in the combo box."""
        return self.micComboBox.currentData()

    def set_folder_button_enabled(self, enabled):
        """Enable or disable the folder selection button."""
        self.folderPushButton.setEnabled(enabled)

    def update_folder_button_tooltip(self, folder):
        """Update the tooltip of the folder selection button with the current save folder."""
        self.folderPushButton.setToolTip(f"Save folder: {folder}")