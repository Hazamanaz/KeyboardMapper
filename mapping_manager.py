# mapping_manager.py

import json
import os

class MappingManager:
    def __init__(self, config_path="config.json"):
        """Initializes the MappingManager and loads existing mappings."""
        self.config_path = config_path
        self.mappings = {}  # Holds key-action pairs
        self.load_mappings()
        print("MappingManager initialized with mappings:", self.mappings)

    def add_mapping(self, key, action):
        """Adds a new key-action mapping."""
        self.mappings[key] = action
        print(f"Mapping added: {key} -> {action}")
        self.save_mappings()

    def remove_mapping(self, key):
        """Removes a key-action mapping."""
        if key in self.mappings:
            del self.mappings[key]
            print(f"Mapping removed: {key}")
            self.save_mappings()
        else:
            print(f"No mapping found for key: {key}")

    def execute_action(self, key):
        """Executes the action associated with the given key."""
        action = self.mappings.get(key)
        if action:
            print(f"Executing action for key: {key} -> {action}")
            # Add logic to execute the action (e.g., control AudioPlayer here)
            # Example: audio_player.play_track(track_id) if action == "play_track"
        else:
            print(f"No action mapped for key: {key}")

    def save_mappings(self):
        """Saves current mappings to the config file."""
        with open(self.config_path, "w") as file:
            json.dump(self.mappings, file)
        print("Mappings saved to", self.config_path)

    def load_mappings(self):
        """Loads mappings from the config file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                self.mappings = json.load(file)
            print("Mappings loaded from", self.config_path)
        else:
            print("No config file found; starting with empty mappings.")
