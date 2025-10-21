import json
import os
from pathlib import Path

class Settings:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.settings_file = self.base_path / "settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file or create default"""
        default_settings = {
            "sound_volume": 0.5,
            "music_volume": 0.3,
            "animations": True,
            "difficulty": "normal",
            "high_score": 0,
            "games_played": 0,
            "games_won": 0
        }
        
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update default settings with loaded ones
                    default_settings.update(loaded_settings)
            else:
                # Save default settings
                self.save_settings(default_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        return default_settings
    
    def save_settings(self, settings=None):
        """Save settings to JSON file"""
        try:
            if settings:
                self.settings.update(settings)
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save_settings()
    
    def update_game_stats(self, won=False):
        """Update game statistics"""
        self.settings["games_played"] += 1
        if won:
            self.settings["games_won"] += 1
            # Update high score if current streak is better
            current_streak = self.get("current_streak", 0) + 1
            self.set("current_streak", current_streak)
            if current_streak > self.settings["high_score"]:
                self.set("high_score", current_streak)
        else:
            self.set("current_streak", 0)
        
        self.save_settings()