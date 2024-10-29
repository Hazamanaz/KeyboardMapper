# ui.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QFileDialog, QTextEdit, QDialog, QListWidget
)
from PyQt5.QtCore import Qt

class DeviceSelectionDialog(QDialog):
    def __init__(self, device_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Device")
        self.device_manager = device_manager
        self.selected_device = None

        layout = QVBoxLayout()
        self.device_list = QListWidget()
        
        # List devices
        self.populate_device_list()

        layout.addWidget(QLabel("Available Devices:"))
        layout.addWidget(self.device_list)
        select_button = QPushButton("Select")
        select_button.clicked.connect(self.select_device)
        layout.addWidget(select_button)
        self.setLayout(layout)

    def populate_device_list(self):
        # Enumerate and display devices
        devices = self.device_manager.enumerate_devices()
        for device in devices:
            self.device_list.addItem(device["product_string"])

    def select_device(self):
        selected_item = self.device_list.currentItem()
        if selected_item:
            self.selected_device = selected_item.text()
            self.accept()  # Close dialog with "OK" status

class AppUI(QMainWindow):
    def __init__(self, device_manager, mapping_manager, audio_player):
        super().__init__()
        
        self.device_manager = device_manager
        self.mapping_manager = mapping_manager
        self.audio_player = audio_player
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Keyboard Mapper")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Device Selection Panel
        device_panel = QHBoxLayout()
        self.select_device_button = QPushButton("Select Device")
        self.select_device_button.clicked.connect(self.show_device_selection_dialog)
        device_panel.addWidget(QLabel("Device Selection:"))
        device_panel.addWidget(self.select_device_button)
        
        # Key Mapping Panel
        mapping_panel = QVBoxLayout()
        self.mapping_table = QTableWidget(0, 2)  # Empty table with 2 columns
        self.mapping_table.setHorizontalHeaderLabels(["Key", "Action"])
        self.mapping_table.horizontalHeader().setStretchLastSection(True)
        self.key_detection_button = QPushButton("Key Detection Mode")
        self.key_detection_button.clicked.connect(self.start_key_detection)
        self.add_mapping_button = QPushButton("Add Mapping")
        self.add_mapping_button.clicked.connect(self.add_mapping)
        self.remove_mapping_button = QPushButton("Remove Mapping")
        self.remove_mapping_button.clicked.connect(self.remove_mapping)
        
        # Add Save/Load buttons
        self.save_mappings_button = QPushButton("Save Mappings")
        self.save_mappings_button.clicked.connect(self.save_mappings)
        self.load_mappings_button = QPushButton("Load Mappings")
        self.load_mappings_button.clicked.connect(self.load_mappings)
        
        mapping_panel.addWidget(QLabel("Key Mappings"))
        mapping_panel.addWidget(self.mapping_table)
        mapping_panel.addWidget(self.key_detection_button)
        mapping_panel.addWidget(self.add_mapping_button)
        mapping_panel.addWidget(self.remove_mapping_button)
        mapping_panel.addWidget(self.save_mappings_button)
        mapping_panel.addWidget(self.load_mappings_button)

        # Audio Control Panel
        audio_panel = QVBoxLayout()
        self.track_table = QTableWidget(0, 2)  # Empty table with 2 columns
        self.track_table.setHorizontalHeaderLabels(["Track ID", "File Path"])
        self.track_table.horizontalHeader().setStretchLastSection(True)
        self.load_track_button = QPushButton("Load Track")
        self.load_track_button.clicked.connect(self.load_track)
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_track)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_track)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_all_tracks)
        
        audio_panel.addWidget(QLabel("Audio Tracks"))
        audio_panel.addWidget(self.track_table)
        audio_panel.addWidget(self.load_track_button)
        audio_panel.addWidget(self.play_button)
        audio_panel.addWidget(self.pause_button)
        audio_panel.addWidget(self.stop_button)

        # Console Panel
        console_panel = QVBoxLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        
        console_panel.addWidget(QLabel("Status / Console"))
        console_panel.addWidget(self.console_output)

        # Assemble layout
        main_layout.addLayout(device_panel)
        main_layout.addLayout(mapping_panel)
        main_layout.addLayout(audio_panel)
        main_layout.addLayout(console_panel)
        
        self.setCentralWidget(central_widget)

    def show_device_selection_dialog(self):
        """Opens a dialog to select the target device."""
        dialog = DeviceSelectionDialog(self.device_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.console_output.append(f"Device selected: {dialog.selected_device}")
            # Use the selected device in your logic

    def start_key_detection(self):
        """Starts key detection mode."""
        self.console_output.append("Key detection mode started...")
        key = self.device_manager.start_key_detection()
        if key:
            self.console_output.append(f"Detected key: {key}")

    def add_mapping(self):
        """Adds a mapping by prompting for a key and an action."""
        key, action = "ExampleKey", "ExampleAction"  # Placeholder values
        self.mapping_manager.add_mapping(key, action)
        self.update_mapping_table()
        self.console_output.append(f"Added mapping: {key} -> {action}")

    def remove_mapping(self):
        """Removes the selected mapping from the table."""
        selected_items = self.mapping_table.selectedItems()
        if selected_items:
            key = selected_items[0].text()
            self.mapping_manager.remove_mapping(key)
            self.update_mapping_table()
            self.console_output.append(f"Removed mapping for key: {key}")

    def load_track(self):
        """Opens file dialog to load an audio track."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Track", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            track_id = f"track_{len(self.audio_player.tracks) + 1}"
            self.audio_player.load_track(track_id, file_path)
            self.update_track_table()
            self.console_output.append(f"Loaded track: {track_id} -> {file_path}")

    def play_track(self):
        """Plays the selected track."""
        selected_items = self.track_table.selectedItems()
        if selected_items:
            track_id = selected_items[0].text()
            self.audio_player.play_track(track_id)
            self.console_output.append(f"Playing track: {track_id}")

    def pause_track(self):
        """Pauses the currently playing track."""
        self.audio_player.pause_track()
        self.console_output.append("Track paused")

    def stop_all_tracks(self):
        """Stops all tracks."""
        self.audio_player.stop_all()
        self.console_output.append("All tracks stopped")

    def save_mappings(self):
        """Saves the current mappings."""
        self.mapping_manager.save_mappings()
        self.console_output.append("Mappings saved")

    def load_mappings(self):
        """Loads mappings from the config file."""
        self.mapping_manager.load_mappings()
        self.update_mapping_table()
        self.console_output.append("Mappings loaded")

    def update_mapping_table(self):
        """Refreshes the mapping table with current mappings."""
        self.mapping_table.setRowCount(0)  # Clear table
        for key, action in self.mapping_manager.mappings.items():
            row_position = self.mapping_table.rowCount()
            self.mapping_table.insertRow(row_position)
            self.mapping_table.setItem(row_position, 0, QTableWidgetItem(key))
            self.mapping_table.setItem(row_position, 1, QTableWidgetItem(action))

    def update_track_table(self):
        """Refreshes the track table with loaded tracks."""
        self.track_table.setRowCount(0)  # Clear table
        for track_id, file_path in self.audio_player.tracks.items():
            row_position = self.track_table.rowCount()
            self.track_table.insertRow(row_position)
            self.track_table.setItem(row_position, 0, QTableWidgetItem(track_id))
            self.track_table.setItem(row_position, 1, QTableWidgetItem(file_path))
