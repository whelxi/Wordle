import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# --- NEW: Initialize Mixer ---
try:
    pygame.mixer.init()
    mixer_initialized = True
except pygame.error as e:
    print(f"Warning: Mixer could not be initialized. Sound will be disabled. Error: {e}", file=sys.stderr)
    mixer_initialized = False

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750  # Increased height
GRID_SIZE = 5
GRID_ROWS = 6
CELL_SIZE = 60
CELL_MARGIN = 10
GRID_OFFSET_Y = 110 # Pushed grid down

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
DARK_GRAY = (58, 58, 60)

# --- Load word list from file ---
def load_words(filepath):
    """Loads and processes the word list from a file."""
    try:
        with open(filepath, 'r') as f:
            # Read all lines, strip whitespace, and convert to uppercase
            # Filter for 5-letter words and ensure they are alphabetic
            words = [
                line.strip().upper() 
                for line in f 
                if len(line.strip()) == 5 and line.strip().isalpha()
            ]
        if not words:
            # If no valid words are found, print an error and exit
            print(f"Error: No valid 5-letter words found in {filepath}", file=sys.stderr)
            sys.exit(1)
        return words
    except FileNotFoundError:
        print(f"Error: Word list file not found at {filepath}", file=sys.stderr)
        print("Please ensure 'word_list_5.txt' is in the 'data' directory.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while loading words: {e}", file=sys.stderr)
        sys.exit(1)

# Get the absolute path to the directory containing main.py (src/)
# __file__ is the path to the current script (main.py)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Handle cases where __file__ is not defined (e.g., interactive interpreter)
    script_dir = os.path.abspath(os.getcwd())

# Go up one level to the project root (WORDLE/)
project_root = os.path.dirname(script_dir)
# Construct the path to the word list
WORD_LIST_FILE = os.path.join(project_root, 'data', 'word_list_5.txt')

# Load the words
WORDS = load_words(WORD_LIST_FILE)

# --- NEW: Load Keypress Sound ---
keypress_sound = None
if mixer_initialized:
    try:
        # Assume a sound file 'keypress.wav' or 'keypress.ogg' is in the data folder
        # Pygame supports WAV and OGG best
        KEYPRESS_SOUND_FILE = os.path.join(project_root, 'data', 'keypress.mp3')
        if not os.path.exists(KEYPRESS_SOUND_FILE):
            # Try .ogg as a fallback
            KEYPRESS_SOUND_FILE = os.path.join(project_root, 'data', 'keypress.ogg')
        
        keypress_sound = pygame.mixer.Sound(KEYPRESS_SOUND_FILE)
    except pygame.error as e:
        print(f"Warning: Could not load sound file. Sound will be disabled. Error: {e}", file=sys.stderr)
        print(f"Please ensure 'keypress.wav' or 'keypress.ogg' is in the '{os.path.join(project_root, 'data')}' directory.", file=sys.stderr)
    except FileNotFoundError:
            print(f"Warning: Sound file not found. Sound will be disabled.", file=sys.stderr)
            print(f"Please ensure 'keypress.wav' or 'keypress.ogg' is in the '{os.path.join(project_root, 'data')}' directory.", file=sys.stderr)

# --- NEW: Load Enter Sound (as requested) ---
enter_sound = None
if mixer_initialized:
    try:
        ENTER_SOUND_FILE = os.path.join(project_root, 'data', 'keypress2.mp3')
        if not os.path.exists(ENTER_SOUND_FILE):
            # Try .wav as a fallback
            ENTER_SOUND_FILE = os.path.join(project_root, 'data', 'keypress2.wav')
        if not os.path.exists(ENTER_SOUND_FILE):
            # Try .ogg as a final fallback
            ENTER_SOUND_FILE = os.path.join(project_root, 'data', 'keypress2.ogg')
        
        enter_sound = pygame.mixer.Sound(ENTER_SOUND_FILE)
    except pygame.error as e:
        print(f"Warning: Could not load sound file 'keypress2'. Sound will be disabled. Error: {e}", file=sys.stderr)
        print(f"Please ensure 'keypress2.mp3', 'keypress2.wav', or 'keypress2.ogg' is in the '{os.path.join(project_root, 'data')}' directory.", file=sys.stderr)
    except FileNotFoundError:
            print(f"Warning: Sound file 'keypress2' not found. Sound will be disabled.", file=sys.stderr)
            print(f"Please ensure 'keypress2.mp3', 'keypress2.wav', or 'keypress2.ogg' is in the '{os.path.join(project_root, 'data')}' directory.", file=sys.stderr)


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wordle")
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 28, bold=True)
toggle_font = pygame.font.SysFont('Arial', 18)


# --- NEW ---
# Custom event for endless mode reset
RESET_GAME_EVENT = pygame.USEREVENT + 1

# Game state
target_word = random.choice(WORDS)
current_row = 0
current_col = 0
grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_ROWS)]
colors = [[LIGHT_GRAY for _ in range(GRID_SIZE)] for _ in range(GRID_ROWS)]
keyboard_colors = {letter: LIGHT_GRAY for letter in "QWERTYUIOPASDFGHJKLZXCVBNM"}
game_over = False
message = ""
fullscreen = False

# --- NEW ---
# State for new UI elements
endless_mode = False
show_end_game_buttons = False
# We will define these rects in the draw functions so they are dynamic
continue_button_rect = pygame.Rect(0, 0, 0, 0)
exit_button_rect = pygame.Rect(0, 0, 0, 0)
endless_toggle_rect = pygame.Rect(0, 0, 0, 0)
endless_toggle_text_rect = pygame.Rect(0, 0, 0, 0)

# Keyboard layout (as a list of lists for easier processing)
keyboard_rows = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DEL']
]

# --- NEW FUNCTION ---
def reset_game():
    """Resets the game state for a new round."""
    global target_word, current_row, current_col, grid, colors, keyboard_colors
    global game_over, message, show_end_game_buttons
    
    # Stop any pending reset timers
    pygame.time.set_timer(RESET_GAME_EVENT, 0)
    
    target_word = random.choice(WORDS)
    current_row = 0
    current_col = 0
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_ROWS)]
    colors = [[LIGHT_GRAY for _ in range(GRID_SIZE)] for _ in range(GRID_ROWS)]
    # Reset keyboard colors for a fresh start
    keyboard_colors = {letter: LIGHT_GRAY for letter in "QWERTYUIOPASDFGHJKLZXCVBNM"}
    game_over = False
    message = ""
    show_end_game_buttons = False


def draw_grid(current_screen_width):
    # Calculate the dynamic horizontal offset to center the grid
    grid_total_width = (CELL_SIZE + CELL_MARGIN) * GRID_SIZE - CELL_MARGIN
    grid_offset_x = (current_screen_width - grid_total_width) // 2
    
    for row in range(GRID_ROWS):
        for col in range(GRID_SIZE):
            # Use the dynamically calculated offset
            x = grid_offset_x + col * (CELL_SIZE + CELL_MARGIN)
            y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_MARGIN)
            
            # Draw cell background
            pygame.draw.rect(screen, colors[row][col], (x, y, CELL_SIZE, CELL_SIZE))
            
            # Draw cell border
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 2)
            
            # Draw letter if present
            if grid[row][col]:
                text = font.render(grid[row][col], True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

# --- MODIFIED FUNCTION ---
def draw_keyboard(current_screen_width, current_screen_height):
    # Do not draw the keyboard if the end-game buttons are showing
    if show_end_game_buttons:
        return
        
    # Define sizes specifically for the keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40      # Width for regular keys
    special_key_width = 65 # Width for ENTER and DEL

    # Calculate dynamic Y offset to position keyboard near the bottom
    keyboard_offset_y = current_screen_height - (key_height + key_margin) * 3 - 60 # Adjusted padding

    for row_idx, row in enumerate(keyboard_rows):
        # Calculate the total width of the current row
        row_width = 0
        for key_idx, key in enumerate(row):
            if key in ["ENTER", "DEL"]:
                row_width += special_key_width
            else:
                row_width += key_size_x
            if key_idx < len(row) - 1:
                row_width += key_margin
        
        # Calculate starting x to center the row (using current width)
        x = (current_screen_width - row_width) // 2
        y = keyboard_offset_y + row_idx * (key_height + key_margin)
        
        for key in row:
            # Determine key width
            key_width = special_key_width if key in ["ENTER", "DEL"] else key_size_x
            
            # --- NEW: Define key_rect here ---
            key_rect = pygame.Rect(x, y, key_width, key_height)
            
            # Determine key color
            color = LIGHT_GRAY
            if key in keyboard_colors:
                color = keyboard_colors[key]

            # --- NEW: Creative drawing logic for split colors ---
            if isinstance(color, tuple) and color == (GREEN, YELLOW):
                # Split key design
                left_width = key_rect.width // 2
                right_width = key_rect.width - left_width # Handle odd widths
                
                left_half_rect = pygame.Rect(key_rect.left, key_rect.top, left_width, key_rect.height)
                right_half_rect = pygame.Rect(key_rect.left + left_width, key_rect.top, right_width, key_rect.height)
                
                # Draw left half (GREEN)
                pygame.draw.rect(screen, GREEN, left_half_rect, 
                                 border_top_left_radius=5, border_bottom_left_radius=5)
                # Draw right half (YELLOW)
                pygame.draw.rect(screen, YELLOW, right_half_rect, 
                                 border_top_right_radius=5, border_bottom_right_radius=5)
            else:
                # Draw key background (with rounded corners) - normal single color
                pygame.draw.rect(screen, color, key_rect, border_radius=5)
            # --- END NEW LOGIC ---
            
            # Draw letter
            text = small_font.render(key, True, BLACK)
            text_rect = text.get_rect(center=key_rect.center) # Use key_rect.center
            screen.blit(text, text_rect)
            
            # Move x for the next key in the row
            x += key_width + key_margin

def draw_message(current_screen_width):
    if message:
        text = small_font.render(message, True, BLACK)
        # Center message horizontally, place it at a fixed position below the title
        text_rect = text.get_rect(center=(current_screen_width // 2, 80)) # Changed Y position
        screen.blit(text, text_rect)

def draw_title(current_screen_width):
    title_font = pygame.font.SysFont('Arial', 40, bold=True)
    title = title_font.render("WORDLE", True, BLACK)
    # Center title horizontally, place it at the top
    title_rect = title.get_rect(center=(current_screen_width // 2, 40))
    screen.blit(title, title_rect)


# --- NEW FUNCTION ---
def draw_end_game_buttons(current_screen_width, current_screen_height):
    """Draws the Continue and Exit buttons if the game is over and not in endless mode."""
    global continue_button_rect, exit_button_rect
    
    if not show_end_game_buttons:
        return

    button_width = 150
    button_height = 50
    button_margin = 20
    
    # Calculate Y position (e.g., below the grid)
    # Use the grid's bottom edge as a reference
    grid_bottom_y = GRID_OFFSET_Y + (CELL_SIZE + CELL_MARGIN) * GRID_ROWS
    button_y = grid_bottom_y + 40 # 40px padding below grid
    
    # Calculate X positions to center them
    total_width = button_width * 2 + button_margin
    start_x = (current_screen_width - total_width) // 2
    
    # Continue Button
    continue_x = start_x
    continue_button_rect = pygame.Rect(continue_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GREEN, continue_button_rect, border_radius=8)
    text = button_font.render("Continue", True, WHITE)
    text_rect = text.get_rect(center=continue_button_rect.center)
    screen.blit(text, text_rect)

    # Exit Button
    exit_x = start_x + button_width + button_margin
    exit_button_rect = pygame.Rect(exit_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, DARK_GRAY, exit_button_rect, border_radius=8)
    text = button_font.render("Exit", True, WHITE)
    text_rect = text.get_rect(center=exit_button_rect.center)
    screen.blit(text, text_rect)

# --- NEW FUNCTION ---
def draw_endless_mode_toggle(current_screen_width, current_screen_height):
    """Draws the 'Endless Mode' checkbox at the bottom."""
    global endless_toggle_rect, endless_toggle_text_rect
    
    box_size = 20
    text_padding = 10
    
    # Position at the bottom-center
    y = current_screen_height - 30 # 30px from bottom
    
    # Render text to get its width
    text = toggle_font.render("Endless Mode", True, BLACK)
    text_width = text.get_width()
    
    total_width = box_size + text_padding + text_width
    start_x = (current_screen_width - total_width) // 2
    
    # Checkbox Rect
    box_x = start_x
    endless_toggle_rect = pygame.Rect(box_x, y - box_size // 2, box_size, box_size)
    
    # Text Rect
    text_x = box_x + box_size + text_padding
    endless_toggle_text_rect = text.get_rect(centery=y)
    endless_toggle_text_rect.left = text_x
    
    # Draw the text
    screen.blit(text, endless_toggle_text_rect)
    
    # Draw the box
    pygame.draw.rect(screen, BLACK, endless_toggle_rect, 2) # Border
    if endless_mode:
        # Draw a tick (simple lines)
        p1 = (endless_toggle_rect.left + 3, endless_toggle_rect.centery)
        p2 = (endless_toggle_rect.centerx - 2, endless_toggle_rect.bottom - 4)
        p3 = (endless_toggle_rect.right - 4, endless_toggle_rect.top + 4)
        pygame.draw.line(screen, GREEN, p1, p2, 3)
        pygame.draw.line(screen, GREEN, p2, p3, 3)


# --- MODIFIED FUNCTION ---
def check_guess():
    global current_row, current_col, game_over, message, show_end_game_buttons
    
    # Check if the current row is complete
    if current_col != GRID_SIZE:
        message = "Word too short"
        return
    
    guess = "".join(grid[current_row])
    
    # Check if the guess is a valid word
    if guess not in WORDS:
        message = "Not in word list"
        return
    
    # --- Check logic (Grid coloring) ---
    target_letters = list(target_word)
    guess_letters = list(guess)
    
    # First pass: mark correct letters (green)
    for i in range(GRID_SIZE):
        if guess_letters[i] == target_letters[i]:
            colors[current_row][i] = GREEN
            
            # --- NEW KEYBOARD LOGIC (GREEN) ---
            letter = guess_letters[i]
            # Upgrade to split-color if it was yellow
            if keyboard_colors[letter] == YELLOW:
                keyboard_colors[letter] = (GREEN, YELLOW) 
            # Otherwise, set to green (overwrites gray or green)
            else:
                keyboard_colors[letter] = GREEN
            # --- END NEW LOGIC ---
            
            target_letters[i] = None  # Mark as used
    
    # Second pass: mark present but wrong position letters (yellow)
    for i in range(GRID_SIZE):
        if colors[current_row][i] != GREEN:  # If not already green
            letter = guess_letters[i]
            if letter in target_letters:
                colors[current_row][i] = YELLOW
                
                # --- NEW KEYBOARD LOGIC (YELLOW) ---
                # Upgrade to split-color if it was green
                if keyboard_colors[letter] == GREEN:
                    keyboard_colors[letter] = (GREEN, YELLOW)
                # Only set to yellow if it's currently gray
                elif keyboard_colors[letter] == LIGHT_GRAY or keyboard_colors[letter] == DARK_GRAY:
                    keyboard_colors[letter] = YELLOW
                # --- END NEW LOGIC ---
                
                # Remove the first occurrence of this letter from target
                target_letters[target_letters.index(letter)] = None
            else:
                colors[current_row][i] = DARK_GRAY
                
                # --- NEW KEYBOARD LOGIC (GRAY) ---
                # Only set to dark gray if it's light gray
                if keyboard_colors[letter] == LIGHT_GRAY:
                    keyboard_colors[letter] = DARK_GRAY
                # --- END NEW LOGIC ---
    # --- End of check logic ---

    
    # --- MODIFIED End-game logic ---
    is_win = (guess == target_word)
    is_loss = (current_row == GRID_ROWS - 1)

    if is_win or is_loss:
        game_over = True
        if is_win:
            message = "You Win!"
        else: # is_loss
            message = f"Game Over! Word: {target_word}"
        
        if endless_mode:
            # If in endless mode, set a timer to auto-reset
            pygame.time.set_timer(RESET_GAME_EVENT, 2000) # 2-second delay
        else:
            # Otherwise, show the continue/exit buttons
            show_end_game_buttons = True
    else:
        # Not game over, move to next row
        current_row += 1
        current_col = 0
        message = ""

def handle_key_press(key):
    global current_row, current_col, message
    
    # Don't allow key presses if game is over (buttons or timer active)
    if game_over:
        return
    
    # Check for alphabet keys
    if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and len(key) == 1 and current_col < GRID_SIZE:
        grid[current_row][current_col] = key
        current_col += 1
        message = ""
        # --- NEW: Play sound on successful letter press ---
        if keypress_sound:
            keypress_sound.play()
    # Check for Backspace (physical) or DEL (on-screen)
    elif (key == "BACKSPACE" or key == "DEL") and current_col > 0:
        current_col -= 1
        grid[current_row][current_col] = ""
        message = ""
        # --- NEW: Play sound on successful delete ---
        if keypress_sound:
            keypress_sound.play()
    # Check for Return (physical) or ENTER (on-screen)
    elif key == "RETURN" or key == "ENTER":
        # --- NEW: Play Enter sound as requested ---
        if enter_sound:
            enter_sound.play()
        check_guess()

def get_keyboard_key(pos, current_screen_width, current_screen_height):
    # Don't check keyboard if buttons are showing
    if show_end_game_buttons:
        return None
        
    # Use the same dimensions as in draw_keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40
    special_key_width = 65

    # Use the *exact same* dynamic Y offset calculation as draw_keyboard
    keyboard_offset_y = current_screen_height - (key_height + key_margin) * 3 - 60

    for row_idx, row in enumerate(keyboard_rows):
        # Calculate row width (same as draw_keyboard)
        row_width = 0
        for key_idx, key in enumerate(row):
            if key in ["ENTER", "DEL"]:
                row_width += special_key_width
            else:
                row_width += key_size_x
            if key_idx < len(row) - 1:
                row_width += key_margin
        
        # Calculate starting x and y (same as draw_keyboard)
        x = (current_screen_width - row_width) // 2
        y = keyboard_offset_y + row_idx * (key_height + key_margin)
        
        for key in row:
            key_width = special_key_width if key in ["ENTER", "DEL"] else key_size_x
            
            # Check if the click position (pos) is within this key's bounds
            key_rect = pygame.Rect(x, y, key_width, key_height)
            if key_rect.collidepoint(pos):
                if key == "DEL":
                    return "DEL" # Return "DEL" for the on-screen button
                if key == "ENTER":
                    return "ENTER" # Return "ENTER" for the on-screen button
                return key # Return the letter
            
            # Move x for the next key
            x += key_width + key_margin
            
    return None # Click was not on any key

def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        # Return to the default windowed size
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Get current screen dimensions at the start of each frame
    current_screen_width = screen.get_width()
    current_screen_height = screen.get_height()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # --- NEW ---
        # Handle auto-reset timer for endless mode
        elif event.type == RESET_GAME_EVENT:
            reset_game()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:
                toggle_fullscreen()
            # Pass key presses to the handler (it will check for game_over)
            elif event.key == pygame.K_BACKSPACE:
                handle_key_press("BACKSPACE")
            elif event.key == pygame.K_RETURN:
                handle_key_press("RETURN")
            elif event.unicode.isalpha():
                handle_key_press(event.unicode.upper())
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # --- MODIFIED ---
            # 1. Check for Endless Mode toggle first (always active)
            # We check both the box and the text for easier clicking
            if endless_toggle_rect.collidepoint(event.pos) or \
               endless_toggle_text_rect.collidepoint(event.pos):
                endless_mode = not endless_mode
                # If we toggle this while buttons are showing, hide them
                if show_end_game_buttons:
                    show_end_game_buttons = False
                    game_over = False # Allow playing again
                    reset_game() # Or just reset
                
            # 2. Check for end-game buttons (only if showing)
            elif show_end_game_buttons:
                if continue_button_rect.collidepoint(event.pos):
                    reset_game()
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
                    
            # 3. Check for keyboard (only if game is not over)
            elif not game_over:
                # Pass current dimensions to the click handler
                key = get_keyboard_key(event.pos, current_screen_width, current_screen_height)
                if key:
                    handle_key_press(key)
                    
        # Handle window resize event
        elif event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                # Update the screen surface to the new size
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    
    # Draw everything
    screen.fill(WHITE)
    
    # Pass current dimensions to all drawing functions
    draw_title(current_screen_width)
    draw_grid(current_screen_width)
    
    # --- MODIFIED DRAW ORDER ---
    draw_keyboard(current_screen_width, current_screen_height)
    draw_end_game_buttons(current_screen_width, current_screen_height) # Draw this *after* grid
    draw_endless_mode_toggle(current_screen_width, current_screen_height) # Draw this last
    
    draw_message(current_screen_width) # Draw message on top of all
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()