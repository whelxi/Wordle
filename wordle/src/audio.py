import pygame

class AudioManager:
    def __init__(self, assets_manager, settings):
        self.assets = assets_manager
        self.settings = settings
        self.sounds_enabled = True
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sounds_enabled or sound_name not in self.assets.sounds:
            return
        
        try:
            sound = self.assets.sounds[sound_name]
            sound.set_volume(self.settings.get("sound_volume", 0.5))
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
        for sound in self.assets.sounds.values():
            sound.set_volume(volume)