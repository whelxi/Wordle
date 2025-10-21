import pygame
import sys
import os

# Add the current directory to Python path so imports work
sys.path.append(os.path.dirname(__file__))

from assets_manager import AssetsManager
from settings import Settings
from audio import AudioManager
from game import WordleGame
from ui import WordleUI

class WordleApp:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Initialize managers
        self.assets = AssetsManager()
        self.settings = Settings()
        self.audio = AudioManager(self.assets, self.settings)
        
        # Set up display
        self.screen_width = 500
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Wordle Game")
        
        # Initialize game and UI
        self.game = WordleGame(self.assets)
        self.ui = WordleUI(self.assets, self.settings, self.audio)
        self.ui.setup_ui(self.screen_width, self.screen_height)
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle UI events
            ui_result = self.ui.handle_event(event)
            if ui_result == "restart":
                self.restart_game()
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard(event)
    
    def handle_keyboard(self, event):
        """Handle keyboard input"""
        if self.game.game_over:
            return
        
        if event.key == pygame.K_RETURN:
            if self.game.submit_guess():
                self.audio.play_sound('reveal')
                if self.game.game_over:
                    if self.game.won:
                        self.audio.play_sound('success')
                        self.ui.show_message("Congratulations! You won!")
                    else:
                        self.ui.show_message(f"Game Over! Word was: {self.game.target_word}")
                    
                    # Update statistics
                    self.settings.update_game_stats(self.game.won)
        
        elif event.key == pygame.K_BACKSPACE:
            self.game.remove_letter()
        
        elif event.unicode.isalpha() and len(event.unicode) == 1:
            letter = event.unicode.upper()
            self.game.add_letter(letter)
    
    def restart_game(self):
        """Restart the game"""
        self.game.reset_game()
        self.ui.hide_message()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            # Draw everything
            self.ui.draw_game(self.screen, self.game)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = WordleApp()
    app.run()