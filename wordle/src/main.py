import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750  # Increased height
GRID_SIZE = 5
GRID_ROWS = 6
CELL_SIZE = 60
CELL_MARGIN = 10
# GRID_OFFSET_X removed - will be calculated dynamically
GRID_OFFSET_Y = 110 # Pushed grid down
# KEYBOARD_OFFSET_Y removed - will be calculated dynamically

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
DARK_GRAY = (58, 58, 60)

# Word list (simplified for this example)
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

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wordle")
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

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

# Keyboard layout (as a list of lists for easier processing)
keyboard_rows = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DEL']
]

# --- MODIFIED FUNCTION ---
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
    # Define sizes specifically for the keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40      # Width for regular keys
    special_key_width = 65 # Width for ENTER and DEL

    # Calculate dynamic Y offset to position keyboard near the bottom
    keyboard_offset_y = current_screen_height - (key_height + key_margin) * 3 - 20 # 20px padding from bottom

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
            
            # Determine key color
            color = LIGHT_GRAY
            if key in keyboard_colors:
                color = keyboard_colors[key]

            # Draw key background
            pygame.draw.rect(screen, color, (x, y, key_width, key_height))
            # Draw key border
            pygame.draw.rect(screen, GRAY, (x, y, key_width, key_height), 2)
            
            # Draw letter
            text = small_font.render(key, True, BLACK)
            text_rect = text.get_rect(center=(x + key_width // 2, y + key_height // 2))
            screen.blit(text, text_rect)
            
            # Move x for the next key in the row
            x += key_width + key_margin

# --- MODIFIED FUNCTION ---
def draw_message(current_screen_width):
    if message:
        text = small_font.render(message, True, BLACK)
        # Center message horizontally, place it at a fixed position below the title
        text_rect = text.get_rect(center=(current_screen_width // 2, 80)) # Changed Y position
        screen.blit(text, text_rect)

# --- MODIFIED FUNCTION ---
def draw_title(current_screen_width):
    title_font = pygame.font.SysFont('Arial', 40, bold=True)
    title = title_font.render("WORDLE", True, BLACK)
    # Center title horizontally, place it at the top
    title_rect = title.get_rect(center=(current_screen_width // 2, 40))
    screen.blit(title, title_rect)

def check_guess():
    global current_row, current_col, game_over, message
    
    # Check if the current row is complete
    if current_col != GRID_SIZE:
        message = "Word too short"
        return
    
    guess = "".join(grid[current_row])
    
    # Check if the guess is a valid word
    if guess not in WORDS:
        message = "Not in word list"
        return
    
    # Check each letter in the guess
    target_letters = list(target_word)
    guess_letters = list(guess)
    
    # First pass: mark correct letters (green)
    for i in range(GRID_SIZE):
        if guess_letters[i] == target_letters[i]:
            colors[current_row][i] = GREEN
            keyboard_colors[guess_letters[i]] = GREEN
            target_letters[i] = None  # Mark as used
    
    # Second pass: mark present but wrong position letters (yellow)
    for i in range(GRID_SIZE):
        if colors[current_row][i] != GREEN:  # If not already green
            if guess_letters[i] in target_letters:
                colors[current_row][i] = YELLOW
                if keyboard_colors[guess_letters[i]] != GREEN:  # Don't override green
                    keyboard_colors[guess_letters[i]] = YELLOW
                # Remove the first occurrence of this letter from target
                target_letters[target_letters.index(guess_letters[i])] = None
            else:
                colors[current_row][i] = DARK_GRAY
                if keyboard_colors[guess_letters[i]] not in [GREEN, YELLOW]:
                    keyboard_colors[guess_letters[i]] = DARK_GRAY
    
    # Check for win or loss
    if guess == target_word:
        message = "You Win!"
        game_over = True
    elif current_row == GRID_ROWS - 1:
        message = f"Game Over! The word was: {target_word}"
        game_over = True
    else:
        current_row += 1
        current_col = 0
        message = ""

def handle_key_press(key):
    global current_row, current_col, message
    
    if game_over:
        return
    
    # Check for alphabet keys
    if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and len(key) == 1 and current_col < GRID_SIZE:
        grid[current_row][current_col] = key
        current_col += 1
        message = ""
    # Check for Backspace (physical) or DEL (on-screen)
    elif (key == "BACKSPACE" or key == "DEL") and current_col > 0:
        current_col -= 1
        grid[current_row][current_col] = ""
        message = ""
    # Check for Return (physical) or ENTER (on-screen)
    elif key == "RETURN" or key == "ENTER":
        check_guess()

def get_keyboard_key(pos, current_screen_width, current_screen_height):
    # Use the same dimensions as in draw_keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40
    special_key_width = 65

    # Use the *exact same* dynamic Y offset calculation as draw_keyboard
    keyboard_offset_y = current_screen_height - (key_height + key_margin) * 3 - 20

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
            if x <= pos[0] <= x + key_width and y <= pos[1] <= y + key_height:
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:
                toggle_fullscreen()
            elif event.key == pygame.K_BACKSPACE:
                handle_key_press("BACKSPACE")
            elif event.key == pygame.K_RETURN:
                handle_key_press("RETURN")
            elif event.unicode.isalpha():
                handle_key_press(event.unicode.upper())
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
    draw_keyboard(current_screen_width, current_screen_height)
    draw_message(current_screen_width)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()