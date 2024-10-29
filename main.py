import os
import platform
if platform.system() == "Windows":
    lib_path = os.path.join(os.path.dirname(__file__), "lib")
    os.add_dll_directory(lib_path)

from device_manager import DeviceManager
from mapping_manager import MappingManager
from audio_player import AudioPlayer
from ui import AppUI
from PyQt5.QtWidgets import QApplication
import sys
import hid


def main():
    app = QApplication(sys.argv)
    
    # Initialize components
    device_manager = DeviceManager()
    mapping_manager = MappingManager()
    audio_player = AudioPlayer()
    
    # Create the main UI and inject dependencies
    ui = AppUI(device_manager, mapping_manager, audio_player)
    
    # Start the UI loop
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
