import pygame

class AudioManager:
    def __init__(self, assets_manager, settings):
        self.assets = assets_manager
        self.settings = settings
        self.sounds_enabled = True
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
                print("Audio mixer initialized")
            except Exception as e:
                print(f"Could not initialize audio mixer: {e}")
                self.sounds_enabled = False
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sounds_enabled:
            return
        
        if sound_name not in self.assets.sounds:
            print(f"Sound not found: {sound_name}")
            return
        
        try:
            sound = self.assets.sounds[sound_name]
            volume = self.settings.get("sound_volume", 0.5)
            sound.set_volume(max(0.0, min(1.0, volume)))  # Clamp volume
            sound.play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled
    
    def set_volume(self, volume):
        """Set sound volume"""
        volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        self.settings.set("sound_volume", volume)
        
        # Update all loaded sounds
        for name, sound in self.assets.sounds.items():
            try:
                sound.set_volume(volume)
            except Exception as e:
                print(f"Error setting volume for {name}: {e}")