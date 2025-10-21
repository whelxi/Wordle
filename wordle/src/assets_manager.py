import os
import pygame
import json
from pathlib import Path

class AssetsManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.assets_path = self.base_path / "assets"
        self.data_path = self.base_path / "data"
        
        # Create directories if they don't exist
        self._create_directories()
        
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.word_list = []
        
        self.load_assets()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.assets_path / "images",
            self.assets_path / "sounds", 
            self.assets_path / "fonts",
            self.data_path,
            self.base_path / "tests"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _create_placeholder_image(self, width, height, color):
        """Create a placeholder image if file is missing"""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface
    
    def _create_placeholder_sound(self):
        """Create a simple placeholder sound using pygame directly"""
        try:
            # Create a simple beep sound using pygame.mixer.Sound with bytes
            # This creates a very short silent sound as a placeholder
            sample_rate = 22050
            duration = 0.1  # 100ms
            samples = int(sample_rate * duration)
            
            # Create a simple square wave for a beep sound
            # Generate bytes for a simple tone
            sound_bytes = bytearray()
            for i in range(samples):
                # Simple square wave at 440Hz
                value = 128 + int(100 * (1 if (i // (sample_rate // 440)) % 2 else -1))
                sound_bytes.append(max(0, min(255, value)))
            
            # Convert to bytes and create sound
            sound_data = bytes(sound_bytes)
            sound = pygame.mixer.Sound(buffer=sound_data)
            return sound
        except Exception as e:
            print(f"Error creating placeholder sound: {e}")
            # Return a silent sound as ultimate fallback
            try:
                return pygame.mixer.Sound(buffer=bytes([128] * 1000))
            except:
                # If all else fails, return None and handle it elsewhere
                return None
    
    def load_assets(self):
        """Load all game assets"""
        # Load images
        self._load_images()
        
        # Load sounds
        self._load_sounds()
        
        # Load fonts
        self._load_fonts()
        
        # Load word list
        self._load_word_list()
    
    def _load_images(self):
        """Load image assets"""
        image_files = {
            'tile': 'images/tile.png',
            'logo': 'images/logo.png'
        }
        
        for key, path in image_files.items():
            full_path = self.assets_path / path
            try:
                if full_path.exists():
                    self.images[key] = pygame.image.load(str(full_path))
                else:
                    # Create placeholder
                    if key == 'tile':
                        self.images[key] = self._create_placeholder_image(60, 60, (200, 200, 200))
                    else:  # logo
                        self.images[key] = self._create_placeholder_image(200, 100, (50, 50, 150))
                    print(f"Created placeholder for missing image: {path}")
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                self.images[key] = self._create_placeholder_image(60, 60, (255, 0, 0))
    
    def _load_sounds(self):
        """Load sound assets"""
        sound_files = {
            'reveal': 'sounds/reveal.wav',
            'success': 'sounds/success.wav'
        }
        
        for key, path in sound_files.items():
            full_path = self.assets_path / path
            try:
                if full_path.exists():
                    self.sounds[key] = pygame.mixer.Sound(str(full_path))
                    print(f"Loaded sound: {path}")
                else:
                    placeholder = self._create_placeholder_sound()
                    if placeholder:
                        self.sounds[key] = placeholder
                        print(f"Created placeholder for missing sound: {path}")
                    else:
                        print(f"Failed to create placeholder for: {path}")
            except Exception as e:
                print(f"Error loading sound {path}: {e}")
                placeholder = self._create_placeholder_sound()
                if placeholder:
                    self.sounds[key] = placeholder
                else:
                    print(f"Could not create any sound for: {path}")
    
    def _load_fonts(self):
        """Load font assets"""
        font_path = self.assets_path / "fonts" / "game_font.ttf"
        try:
            if font_path.exists():
                self.fonts['main'] = pygame.font.Font(str(font_path), 36)
                self.fonts['small'] = pygame.font.Font(str(font_path), 24)
                print("Loaded custom font")
            else:
                # Use system font as fallback
                self.fonts['main'] = pygame.font.SysFont('Arial', 36, bold=True)
                self.fonts['small'] = pygame.font.SysFont('Arial', 24)
                print("Using system font as fallback")
        except Exception as e:
            print(f"Error loading font: {e}")
            self.fonts['main'] = pygame.font.SysFont('Arial', 36, bold=True)
            self.fonts['small'] = pygame.font.SysFont('Arial', 24)
    
    def _load_word_list(self):
        """Load the word list"""
        word_list_path = self.data_path / "word_list_5.txt"
        try:
            if word_list_path.exists():
                with open(word_list_path, 'r') as f:
                    self.word_list = [line.strip().upper() for line in f if line.strip()]
                print(f"Loaded word list with {len(self.word_list)} words")
            else:
                # Create a default word list
                self.word_list = [
                    "APPLE", "BRAVE", "CLIMB", "DREAM", "EARTH", "FLAME",
                    "GRAPE", "HONEY", "IVORY", "JUICE", "KNIGHT", "LIGHT",
                    "MAGIC", "NIGHT", "OCEAN", "PEARL", "QUICK", "RIVER",
                    "STONE", "TIGER", "ULTRA", "VOICE", "WATER", "YOUTH",
                    "ZEBRA", "ALBUM", "BEACH", "CANDY", "DANCE", "EAGLE"
                ]
                # Save the default word list
                with open(word_list_path, 'w') as f:
                    for word in self.word_list:
                        f.write(word + '\n')
                print("Created default word list")
        except Exception as e:
            print(f"Error loading word list: {e}")
            # Fallback word list
            self.word_list = ["APPLE", "BRAVE", "CLIMB", "DREAM", "EARTH"]
            print("Using fallback word list")