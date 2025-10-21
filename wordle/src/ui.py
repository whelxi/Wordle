import pygame
from game import LetterState

class WordleUI:
    def __init__(self, assets_manager, settings, audio_manager):
        self.assets = assets_manager
        self.settings = settings
        self.audio = audio_manager
        
        # Colors - Wordle-inspired color scheme
        self.colors = {
            'background': (18, 18, 19),
            'empty_tile': (58, 58, 60),
            'absent': (58, 58, 60),
            'present': (181, 159, 59),
            'correct': (83, 141, 78),
            'text': (255, 255, 255),
            'border': (86, 86, 86),
            'key_bg': (129, 131, 132),
            'header_bg': (30, 30, 32),
            'button_bg': (83, 141, 78),
            'button_hover': (101, 169, 95),
            'button_text': (255, 255, 255)
        }
        
        # UI dimensions for larger window
        self.tile_size = 70
        self.tile_margin = 8
        self.grid_width = 5 * (self.tile_size + self.tile_margin) - self.tile_margin
        self.grid_height = 6 * (self.tile_size + self.tile_margin) - self.tile_margin
        
        # Keyboard layout
        self.keyboard_rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        # Button and UI element rectangles
        self.restart_button_rect = None
        self.message = ""
        self.message_timer = 0
        self.message_duration = 3000  # 3 seconds
        
        # Store keyboard button positions for click detection
        self.key_rects = {}
        self.enter_rect = None
        self.backspace_rect = None
    
    def setup_ui(self, screen_width, screen_height):
        """Setup UI elements"""
        # Setup restart button position
        button_width, button_height = 150, 50
        self.restart_button_rect = pygame.Rect(
            screen_width // 2 - button_width // 2,
            800, # Positioned 10px below the keyboard
            button_width,
            button_height
        )
    
    def draw_game(self, screen, game):
        """Draw the entire game interface"""
        # Draw background
        screen.fill(self.colors['background'])
        
        # Draw header
        header_rect = pygame.Rect(0, 0, screen.get_width(), 100)
        pygame.draw.rect(screen, self.colors['header_bg'], header_rect)
        
        # Draw title
        self._draw_title(screen)
        
        # Draw the grid
        self._draw_grid(screen, game)
        
        # Draw the keyboard with proper spacing
        self._draw_keyboard(screen, game)
        
        # Draw game stats
        self._draw_stats(screen)
        
        # Draw restart button
        self._draw_restart_button(screen)
        
        # Draw message if active
        if self.message and pygame.time.get_ticks() < self.message_timer:
            self._draw_message(screen)
    
    def _draw_title(self, screen):
        """Draw the game title"""
        title_font = pygame.font.SysFont('Arial', 48, bold=True)
        title_text = title_font.render("WORDLE", True, self.colors['text'])
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_text, title_rect)
    
    def _draw_grid(self, screen, game):
        """Draw the word grid"""
        # Position grid higher to leave space for keyboard
        start_x = (screen.get_width() - self.grid_width) // 2
        start_y = 120  # Moved up slightly to create more space
        
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
        pygame.draw.rect(screen, color, tile_rect, border_radius=6)
        
        # Draw border for empty/typing tiles
        if state in [LetterState.EMPTY, LetterState.TYPING]:
            pygame.draw.rect(screen, self.colors['border'], tile_rect, 2, border_radius=6)
        
        # Draw letter if present
        if letter:
            # Use a bold font for letters
            letter_font = pygame.font.SysFont('Arial', 36, bold=True)
            text_surface = letter_font.render(letter.upper(), True, self.colors['text'])
            text_rect = text_surface.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
            screen.blit(text_surface, text_rect)
    
    def _draw_keyboard(self, screen, game):
        """Draw the on-screen keyboard with proper spacing from the grid"""
        keyboard_state = game.get_keyboard_state()
        key_width = 50  # Slightly smaller keys for better spacing
        key_height = 60
        key_margin = 5
        
        # Position keyboard lower with more space from the grid
        start_y = 600  # Increased to create space between grid and keyboard
        
        # Clear previous key positions
        self.key_rects.clear()
        
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
                    color = self.colors['key_bg']
                
                # Draw key background
                key_rect = pygame.Rect(x, y, key_width, key_height)
                pygame.draw.rect(screen, color, key_rect, border_radius=5)
                
                # Store key position for click detection
                self.key_rects[key] = key_rect
                
                # Draw key letter
                key_font = pygame.font.SysFont('Arial', 18, bold=True)
                text_surface = key_font.render(key, True, self.colors['text'])
                text_rect = text_surface.get_rect(center=(x + key_width // 2, y + key_height // 2))
                screen.blit(text_surface, text_rect)
        
        # Draw Enter and Backspace keys
        # Note: 'start_x' now holds the start_x of the last row ("ZXCVBNM")
        
        enter_width = key_width * 1.6
        # Position Enter key to the left of 'Z', accounting for its own width and margin
        enter_x = start_x - enter_width - key_margin 
        
        backspace_x = start_x + len(self.keyboard_rows[2]) * (key_width + key_margin)
        last_row_y = start_Y = 600  # Increased to create space between grid and keyboard
        
        # Clear previous key positions
        self.key_rects.clear()
        
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
                    color = self.colors['key_bg']
                
                # Draw key background
                key_rect = pygame.Rect(x, y, key_width, key_height)
                pygame.draw.rect(screen, color, key_rect, border_radius=5)
                
                # Store key position for click detection
                self.key_rects[key] = key_rect
                
                # Draw key letter
                key_font = pygame.font.SysFont('Arial', 18, bold=True)
                text_surface = key_font.render(key, True, self.colors['text'])
                text_rect = text_surface.get_rect(center=(x + key_width // 2, y + key_height // 2))
                screen.blit(text_surface, text_rect)
        
        # Draw Enter and Backspace keys
        # Note: 'start_x' now holds the start_x of the last row ("ZXCVBNM")
        
        enter_width = key_width * 1.6
        # Position Enter key to the left of 'Z', accounting for its own width and margin
        enter_x = start_x - enter_width - key_margin 
        
        backspace_x = start_x + len(self.keyboard_rows[2]) * (key_width + key_margin)
        last_row_y = start_y + 2 * (key_height + key_margin)
        
        # Enter key
        enter_rect = pygame.Rect(enter_x, last_row_y, enter_width, key_height)
        pygame.draw.rect(screen, self.colors['key_bg'], enter_rect, border_radius=5)
        enter_font = pygame.font.SysFont('Arial', 14, bold=True)
        enter_text = enter_font.render("ENTER", True, self.colors['text'])
        enter_text_rect = enter_text.get_rect(center=enter_rect.center)
        screen.blit(enter_text, enter_text_rect)
        self.enter_rect = enter_rect
        
        # Backspace key
        backspace_rect = pygame.Rect(backspace_x, last_row_y, key_width * 1.6, key_height)
        pygame.draw.rect(screen, self.colors['key_bg'], backspace_rect, border_radius=5)
        backspace_font = pygame.font.SysFont('Arial', 14, bold=True)
        backspace_text = backspace_font.render("DELETE", True, self.colors['text'])
        backspace_text_rect = backspace_text.get_rect(center=backspace_rect.center)
        screen.blit(backspace_text, backspace_text_rect)
        self.backspace_rect = backspace_rect
        
        # REMOVED: separator line
    
    def _draw_stats(self, screen):
        """Draw game statistics"""
        stats_text = f"Played: {self.settings.get('games_played', 0)} | " \
                     f"Won: {self.settings.get('games_won', 0)} | " \
                     f"Current Streak: {self.settings.get('current_streak', 0)}"
        
        stats_font = pygame.font.SysFont('Arial', 16)
        text_surface = stats_font.render(stats_text, True, self.colors['text'])
        # Positioned 10px below the button
        screen.blit(text_surface, (20, 860))
    
    def _draw_restart_button(self, screen):
        """Draw the restart button"""
        # Draw button background
        pygame.draw.rect(screen, self.colors['button_bg'], self.restart_button_rect, border_radius=8)
        
        # Draw button text
        button_font = pygame.font.SysFont('Arial', 18, bold=True)
        button_text = button_font.render("NEW GAME", True, self.colors['button_text'])
        button_text_rect = button_text.get_rect(center=self.restart_button_rect.center)
        screen.blit(button_text, button_text_rect)
    
    def _draw_message(self, screen):
        """Draw a message on the screen"""
        message_font = pygame.font.SysFont('Arial', 22, bold=True)
        message_surface = message_font.render(self.message, True, self.colors['text'])
        message_rect = message_surface.get_rect(center=(screen.get_width() // 2, 500))  # Positioned in the space between grid and keyboard
        
        # Draw message background
        bg_rect = message_rect.inflate(20, 10)
        pygame.draw.rect(screen, self.colors['header_bg'], bg_rect, border_radius=5)
        pygame.draw.rect(screen, self.colors['border'], bg_rect, 2, border_radius=5)
        
        screen.blit(message_surface, message_rect)
    
    def show_message(self, message, duration=3000):
        """Show a temporary message"""
        self.message = message
        self.message_timer = pygame.time.get_ticks() + duration
    
    def hide_message(self):
        """Hide the message"""
        self.message = ""
    
    def handle_event(self, event):
        """Handle UI events"""
        # Handle mouse clicks on virtual keyboard and buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = event.pos
            result = self._handle_mouse_click(mouse_pos)
            if result:
                return result
            
            # Check restart button
            if self.restart_button_rect and self.restart_button_rect.collidepoint(mouse_pos):
                return "restart"
        
        return None
    
    def _handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks on the virtual keyboard"""
        # Check letter keys
        for key, rect in self.key_rects.items():
            if rect.collidepoint(mouse_pos):
                return f"key_{key}"
        
        # Check Enter key
        if self.enter_rect and self.enter_rect.collidepoint(mouse_pos):
            return "enter"
        
        # Check Backspace key
        if self.backspace_rect and self.backspace_rect.collidepoint(mouse_pos):
            return "backspace"
        
        return None