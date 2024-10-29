# audio_player.py

import pygame
import os

class AudioPlayer:
    def __init__(self):
        """Initializes the audio player and loads pygame mixer."""
        pygame.mixer.init()
        self.tracks = {}       # Dictionary to store loaded tracks by track ID
        self.currently_playing = None  # Track ID of the currently playing track
        print("AudioPlayer initialized")

    def load_track(self, track_id, track_path):
        """Loads an audio track and assigns it to a track ID."""
        if not os.path.exists(track_path):
            print(f"Error: Track file {track_path} does not exist.")
            return

        # Load the track using pygame mixer and add to the tracks dictionary
        self.tracks[track_id] = track_path
        print(f"Track loaded: {track_id} -> {track_path}")

    def play_track(self, track_id):
        """Plays the specified track."""
        if track_id not in self.tracks:
            print(f"Error: Track ID {track_id} not found.")
            return
        
        # Stop current track if another is playing
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        # Load and play the new track
        pygame.mixer.music.load(self.tracks[track_id])
        pygame.mixer.music.play()
        self.currently_playing = track_id
        print(f"Playing track: {track_id}")

    def pause_track(self):
        """Pauses the currently playing track."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Track paused")

    def resume_track(self):
        """Resumes the paused track."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            print("Track resumed")

    def stop_all(self):
        """Stops all tracks."""
        pygame.mixer.music.stop()
        self.currently_playing = None
        print("All tracks stopped")

    def is_playing(self, track_id):
        """Returns True if the specified track is currently playing."""
        return self.currently_playing == track_id and pygame.mixer.music.get_busy()
