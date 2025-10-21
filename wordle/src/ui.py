import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel

# Import from our game module
from .game import LetterState

class WordleUI:
    def __init__(self, assets_manager, settings, audio_manager):
        self.assets = assets_manager
        self.settings = settings
        self.audio = audio_manager
        
        # Colors
        self.colors = {
            'background': (18, 18, 19),
            'empty_tile': (58, 58, 60),
            'absent': (58, 58, 60),
            'present': (181, 159, 59),
            'correct': (83, 141, 78),
            'text': (255, 255, 255),
            'border': (86, 86, 86)
        }
        
        # UI dimensions
        self.tile_size = 62
        self.tile_margin = 5
        self.grid_width = 5 * (self.tile_size + self.tile_margin) - self.tile_margin
        self.grid_height = 6 * (self.tile_size + self.tile_margin) - self.tile_margin
        
        # Keyboard layout
        self.keyboard_rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        self.manager = None
        self.restart_button = None
        self.message_label = None
    
    def setup_ui(self, screen_width, screen_height):
        """Setup the pygame_gui manager and elements"""
        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        
        # Create restart button
        button_width, button_height = 120, 40
        self.restart_button = UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - button_width // 2, 
                 screen_height - 80),
                (button_width, button_height)
            ),
            text='New Game',
            manager=self.manager
        )
        
        # Create message label
        self.message_label = UILabel(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 150, 20),
                (300, 40)
            ),
            text='',
            manager=self.manager
        )
        self.message_label.visible = False
    
    def draw_game(self, screen, game):
        """Draw the entire game interface"""
        screen.fill(self.colors['background'])
        
        # Draw the grid
        self._draw_grid(screen, game)
        
        # Draw the keyboard
        self._draw_keyboard(screen, game)
        
        # Draw game stats
        self._draw_stats(screen)
        
        # Update UI manager
        if self.manager:
            self.manager.update(pygame.time.get_ticks() / 1000.0)
            self.manager.draw_ui(screen)
    
    def _draw_grid(self, screen, game):
        """Draw the word grid"""
        start_x = (screen.get_width() - self.grid_width) // 2
        start_y = 100
        
        for row in range(6):
            for col in range(5):
                # Calculate position
                x = start_x + col * (self.tile_size + self.tile_margin)
                y = start_y + row * (self.tile_size + self.tile_margin)
                
                # Get letter and state
                letter = ""
                state = LetterState.EMPTY
                
                if row < len(game.guesses) and col < len(game.guesses[row]):
                    if game.guesses[row]:
                        if col < len(game.guesses[row]):
                            letter = game.guesses[row][col]
                
                if row < game.current_guess:
                    state = game.letter_states[row][col]
                elif row == game.current_guess and col < game.current_letter:
                    state = LetterState.TYPING
                
                # Draw the tile
                self._draw_tile(screen, x, y, letter, state)
    
    def _draw_tile(self, screen, x, y, letter, state):
        """Draw a single tile"""
        # Determine tile color based on state
        if state == LetterState.CORRECT:
            color = self.colors['correct']
        elif state == LetterState.PRESENT:
            color = self.colors['present']
        elif state == LetterState.ABSENT:
            color = self.colors['absent']
        elif state == LetterState.TYPING:
            color = self.colors['empty_tile']
        else:  # EMPTY
            color = self.colors['empty_tile']
        
        # Draw tile background
        tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        pygame.draw.rect(screen, color, tile_rect, border_radius=4)
        
        # Draw border for empty/typing tiles
        if state in [LetterState.EMPTY, LetterState.TYPING]:
            pygame.draw.rect(screen, self.colors['border'], tile_rect, 2, border_radius=4)
        
        # Draw letter if present
        if letter:
            text_surface = self.assets.fonts['main'].render(letter.upper(), True, self.colors['text'])
            text_rect = text_surface.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
            screen.blit(text_surface, text_rect)
    
    def _draw_keyboard(self, screen, game):
        """Draw the on-screen keyboard"""
        keyboard_state = game.get_keyboard_state()
        key_width = 40
        key_height = 55
        key_margin = 5
        
        start_y = 500
        
        for row_idx, row in enumerate(self.keyboard_rows):
            row_width = len(row) * (key_width + key_margin) - key_margin
            start_x = (screen.get_width() - row_width) // 2
            
            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (key_width + key_margin)
                y = start_y + row_idx * (key_height + key_margin)
                
                # Determine key color based on state
                state = keyboard_state.get(key, LetterState.EMPTY)
                if state == LetterState.CORRECT:
                    color = self.colors['correct']
                elif state == LetterState.PRESENT:
                    color = self.colors['present']
                elif state == LetterState.ABSENT:
                    color = self.colors['absent']
                else:
                    color = (129, 131, 132)
                
                # Draw key background
                key_rect = pygame.Rect(x, y, key_width, key_height)
                pygame.draw.rect(screen, color, key_rect, border_radius=4)
                
                # Draw key letter
                text_surface = self.assets.fonts['small'].render(key, True, self.colors['text'])
                text_rect = text_surface.get_rect(center=(x + key_width // 2, y + key_height // 2))
                screen.blit(text_surface, text_rect)
        
        # Draw Enter and Backspace keys
        enter_x = start_x - (key_width + key_margin)
        backspace_x = start_x + len(self.keyboard_rows[2]) * (key_width + key_margin)
        last_row_y = start_y + 2 * (key_height + key_margin)
        
        # Enter key
        enter_rect = pygame.Rect(enter_x, last_row_y, key_width * 1.5, key_height)
        pygame.draw.rect(screen, (129, 131, 132), enter_rect, border_radius=4)
        enter_text = self.assets.fonts['small'].render("ENTER", True, self.colors['text'])
        enter_text_rect = enter_text.get_rect(center=enter_rect.center)
        screen.blit(enter_text, enter_text_rect)
        
        # Backspace key
        backspace_rect = pygame.Rect(backspace_x, last_row_y, key_width * 1.375, key_height)
        pygame.draw.rect(screen, (129, 131, 132), backspace_rect, border_radius=4)
        backspace_text = self.assets.fonts['small'].render("DEL", True, self.colors['text'])
        backspace_text_rect = backspace_text.get_rect(center=backspace_rect.center)
        screen.blit(backspace_text, backspace_text_rect)
    
    def _draw_stats(self, screen):
        """Draw game statistics"""
        stats_text = f"Games: {self.settings.get('games_played', 0)} | " \
                    f"Won: {self.settings.get('games_won', 0)} | " \
                    f"Streak: {self.settings.get('current_streak', 0)}"
        
        text_surface = self.assets.fonts['small'].render(stats_text, True, self.colors['text'])
        screen.blit(text_surface, (20, 20))
    
    def show_message(self, message, duration=2000):
        """Show a temporary message"""
        if self.message_label:
            self.message_label.set_text(message)
            self.message_label.visible = True
            # In a real implementation, you'd set a timer to hide it
    
    def hide_message(self):
        """Hide the message"""
        if self.message_label:
            self.message_label.visible = False
    
    def handle_event(self, event):
        """Handle UI events"""
        if self.manager:
            self.manager.process_events(event)
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.restart_button:
                        return "restart"
        
        return None