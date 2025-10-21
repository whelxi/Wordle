import pygame
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now import from src
try:
    from src.assets_manager import AssetsManager
    from src.settings import Settings
    from src.audio import AudioManager
    from src.game import WordleGame
    from src.ui import WordleUI
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying direct imports...")
    # Fallback to direct imports
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
        
        # Set up larger display
        self.screen_width = 800
        self.screen_height = 900
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
            elif ui_result and ui_result.startswith("key_"):
                # Virtual keyboard letter pressed
                letter = ui_result[4:]  # Remove "key_" prefix
                self.game.add_letter(letter)
            elif ui_result == "enter":
                self.submit_guess()
            elif ui_result == "backspace":
                self.game.remove_letter()
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard(event)
    
    def handle_keyboard(self, event):
        """Handle keyboard input"""
        if self.game.game_over:
            return
        
        if event.key == pygame.K_RETURN:
            self.submit_guess()
        
        elif event.key == pygame.K_BACKSPACE:
            self.game.remove_letter()
        
        elif event.unicode.isalpha() and len(event.unicode) == 1:
            letter = event.unicode.upper()
            self.game.add_letter(letter)
    
    def submit_guess(self):
        """Submit the current guess"""
        if self.game.submit_guess():
            self.audio.play_sound('reveal')
            if self.game.game_over:
                if self.game.won:
                    self.audio.play_sound('success')
                    self.ui.show_message("Congratulations! You won!")
                else:
                    self.ui.show_message(f"Game Over! The word was: {self.game.target_word}")
                
                # Update statistics
                self.settings.update_game_stats(self.game.won)
        else:
            # Show error message if word is invalid
            current_guess = self.game.guesses[self.game.current_guess]
            if len(current_guess) == 5 and not self.game.is_valid_word(current_guess):
                self.ui.show_message("Word not in dictionary!")
    
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