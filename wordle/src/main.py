import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 700
GRID_SIZE = 5
GRID_ROWS = 6
CELL_SIZE = 60
CELL_MARGIN = 10
GRID_OFFSET_X = (SCREEN_WIDTH - (CELL_SIZE + CELL_MARGIN) * GRID_SIZE) // 2
GRID_OFFSET_Y = 80
KEYBOARD_OFFSET_Y = 520

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
DARK_GRAY = (58, 58, 60)

# Word list (simplified for this example)
WORDS = [
    'ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE', 'ADMIT', 'ADOPT', 'ADULT',
    'AFTER', 'AGAIN', 'AGENT', 'AGREE', 'AHEAD', 'ALARM', 'ALBUM', 'ALERT',
    'ALIKE', 'ALIVE', 'ALLOW', 'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGER',
    'ANGLE', 'ANGRY', 'APART', 'APPLE', 'APPLY', 'ARENA', 'ARGUE', 'ARISE',
    'ARRAY', 'ASIDE', 'ASSET', 'AUDIO', 'AUDIT', 'AVOID', 'AWARD', 'AWARE',
    'AWFUL', 'BADLY', 'BAKER', 'BASES', 'BASIC', 'BASIS', 'BEACH', 'BEGAN',
    'BEGIN', 'BEGUN', 'BEING', 'BELOW', 'BENCH', 'BIRTH', 'BLACK', 'BLAME',
    'BLIND', 'BLOCK', 'BLOOD', 'BOARD', 'BOOST', 'BOOTH', 'BOUND', 'BRAIN',
    'BRAND', 'BREAD', 'BREAK', 'BREED', 'BRIEF', 'BRING', 'BROAD', 'BROKE',
    'BROWN', 'BUILD', 'BUILT', 'BURST', 'BUYER', 'CABLE', 'CARRY', 'CATCH',
    'CAUSE', 'CHAIN', 'CHAIR', 'CHART', 'CHASE', 'CHEAP', 'CHECK', 'CHEST',
    'CHIEF', 'CHILD', 'CHINA', 'CHOSE', 'CIVIL', 'CLAIM', 'CLASS', 'CLEAN',
    'CLEAR', 'CLICK', 'CLOCK', 'CLOSE', 'CLOWN', 'COACH', 'COAST', 'COULD',
    'COUNT', 'COURT', 'COVER', 'CRAFT', 'CRASH', 'CREAM', 'CRIME', 'CROSS',
    'CROWD', 'CROWN', 'CRUEL', 'CURVE', 'CYCLE', 'DAILY', 'DANCE', 'DATED',
    'DEALT', 'DEATH', 'DEBUT', 'DELAY', 'DEPTH', 'DIRTY', 'DOING', 'DOUBT',
    'DOZEN', 'DRAFT', 'DRAMA', 'DRAWN', 'DREAM', 'DRESS', 'DRILL', 'DRINK',
    'DRIVE', 'DROVE', 'DYING', 'EAGER', 'EARLY', 'EARTH', 'EIGHT', 'ELITE',
    'EMPTY', 'ENEMY', 'ENJOY', 'ENTER', 'ENTRY', 'EQUAL', 'ERROR', 'ESSAY',
    'EVENT', 'EVERY', 'EXACT', 'EXIST', 'EXTRA', 'FAITH', 'FALSE', 'FAULT',
    'FAVOR', 'FEAST', 'FIBER', 'FIELD', 'FIFTH', 'FIFTY', 'FIGHT', 'FINAL',
    'FIRST', 'FIXED', 'FLAME', 'FLASH', 'FLEET', 'FLOOR', 'FLUID', 'FOCUS',
    'FORCE', 'FORTH', 'FORTY', 'FORUM', 'FOUND', 'FRAME', 'FRANK', 'FRAUD',
    'FRESH', 'FRONT', 'FRUIT', 'FULLY', 'FUNNY', 'GIANT', 'GIVEN', 'GLASS',
    'GLOBE', 'GOING', 'GRACE', 'GRADE', 'GRAIN', 'GRAND', 'GRANT', 'GRASS',
    'GRAVE', 'GREAT', 'GREEN', 'GROSS', 'GROUP', 'GROWN', 'GUARD', 'GUESS',
    'GUEST', 'GUIDE', 'HABIT', 'HAPPY', 'HARRY', 'HEART', 'HEAVY', 'HENCE',
    'HONEY', 'HORSE', 'HOTEL', 'HOUSE', 'HUMAN', 'IDEAL', 'IMAGE', 'INDEX',
    'INNER', 'INPUT', 'ISSUE', 'JOINT', 'JUDGE', 'JUICE', 'KNOWN', 'LABEL',
    'LARGE', 'LASER', 'LATER', 'LAUGH', 'LAYER', 'LEARN', 'LEASE', 'LEAST',
    'LEAVE', 'LEGAL', 'LEVEL', 'LIGHT', 'LIMIT', 'LINKS', 'LOCAL', 'LOGIC',
    'LOOSE', 'LOWER', 'LUCKY', 'LUNCH', 'LYING', 'MAGIC', 'MAJOR', 'MAKER',
    'MARCH', 'MATCH', 'MAYBE', 'MAYOR', 'MEANT', 'MEDIA', 'METAL', 'MIGHT',
    'MINOR', 'MINUS', 'MIXED', 'MODEL', 'MOIST', 'MONEY', 'MONTH', 'MORAL',
    'MOTOR', 'MOUNT', 'MOUSE', 'MOUTH', 'MOVIE', 'MUSIC', 'NEEDS', 'NEVER',
    'NEWLY', 'NIGHT', 'NOISE', 'NORTH', 'NOTED', 'NOVEL', 'NURSE', 'OCCUR',
    'OCEAN', 'OFFER', 'OFTEN', 'ONSET', 'OPERA', 'ORDER', 'OTHER', 'OUGHT',
    'OWNER', 'PAINT', 'PANEL', 'PAPER', 'PARTY', 'PEACE', 'PENNY', 'PHASE',
    'PHONE', 'PHOTO', 'PIECE', 'PILOT', 'PITCH', 'PLACE', 'PLAIN', 'PLANE',
    'PLANT', 'PLATE', 'POINT', 'POUND', 'POWER', 'PRESS', 'PRICE', 'PRIDE',
    'PRIME', 'PRINT', 'PRIOR', 'PRIZE', 'PROOF', 'PROUD', 'PROVE', 'QUEEN',
    'QUEST', 'QUICK', 'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE', 'RAPID',
    'RATIO', 'REACH', 'REACT', 'READY', 'REFER', 'RIGHT', 'RIVAL', 'RIVER',
    'ROCKY', 'ROMAN', 'ROUGH', 'ROUND', 'ROUTE', 'ROYAL', 'RURAL', 'SCALE',
    'SCENE', 'SCOPE', 'SCORE', 'SENSE', 'SERVE', 'SEVEN', 'SHALL', 'SHAME',
    'SHAPE', 'SHARE', 'SHARP', 'SHEET', 'SHELF', 'SHELL', 'SHIFT', 'SHINE',
    'SHINY', 'SHIRT', 'SHOCK', 'SHOOT', 'SHOPS', 'SHORT', 'SHOUT', 'SHOWN',
    'SIGHT', 'SILLY', 'SINCE', 'SIXTH', 'SIXTY', 'SIZED', 'SKILL', 'SKIRT',
    'SLEEP', 'SLIDE', 'SLOPE', 'SMALL', 'SMART', 'SMILE', 'SMOKE', 'SNAKE',
    'SOLAR', 'SOLID', 'SOLVE', 'SORRY', 'SOUND', 'SOUTH', 'SPACE', 'SPARE',
    'SPEAK', 'SPEED', 'SPEND', 'SPENT', 'SPLIT', 'SPOKE', 'SPORT', 'SPOTS',
    'STAFF', 'STAGE', 'STAKE', 'STAND', 'START', 'STATE', 'STEAM', 'STEEL',
    'STEEP', 'STICK', 'STILL', 'STOCK', 'STONE', 'STOOD', 'STORE', 'STORM',
    'STORY', 'STRAW', 'STRIP', 'STUCK', 'STUDY', 'STUFF', 'STYLE', 'SUGAR',
    'SUITE', 'SUNNY', 'SUPER', 'SWEET', 'TABLE', 'TAKEN', 'TASTE', 'TAXES',
    'TEACH', 'TEAMS', 'TEETH', 'TENSE', 'TENTH', 'TEXAS', 'THANK', 'THEFT',
    'THEIR', 'THEME', 'THERE', 'THESE', 'THICK', 'THIEF', 'THING', 'THINK',
    'THIRD', 'THOSE', 'THREE', 'THREW', 'THROW', 'THUMB', 'TIGHT', 'TIMER',
    'TIMES', 'TIRED', 'TITLE', 'TODAY', 'TOKEN', 'TOPIC', 'TOTAL', 'TOUCH',
    'TOUGH', 'TOWER', 'TOXIC', 'TRACK', 'TRADE', 'TRAIL', 'TRAIN', 'TREAT',
    'TREND', 'TRIAL', 'TRIBE', 'TRICK', 'TRIED', 'TRIES', 'TRUCK', 'TRULY',
    'TRUST', 'TRUTH', 'TWICE', 'TWIST', 'UNCLE', 'UNDER', 'UNDUE', 'UNION',
    'UNITY', 'UNTIL', 'UPPER', 'UPSET', 'URBAN', 'USAGE', 'USUAL', 'VALID',
    'VALUE', 'VIDEO', 'VIRUS', 'VISIT', 'VITAL', 'VOICE', 'WASTE', 'WATCH',
    'WATER', 'WEARY', 'WEIGH', 'WHEEL', 'WHERE', 'WHICH', 'WHILE', 'WHITE',
    'WHOLE', 'WHOSE', 'WIDER', 'WOMAN', 'WORLD', 'WORRY', 'WORSE', 'WORST',
    'WORTH', 'WOULD', 'WOUND', 'WRITE', 'WRONG', 'WROTE', 'YIELD', 'YOUNG',
    'YOUTH'
]

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

def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_SIZE):
            x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_MARGIN)
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

def draw_keyboard():
    # Define sizes specifically for the keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40       # Width for regular keys
    special_key_width = 65 # Width for ENTER and DEL

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
        
        # Calculate starting x to center the row
        x = (SCREEN_WIDTH - row_width) // 2
        y = KEYBOARD_OFFSET_Y + row_idx * (key_height + key_margin)
        
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

def draw_message():
    if message:
        text = small_font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, GRID_OFFSET_Y - 30))
        screen.blit(text, text_rect)

def draw_title():
    title_font = pygame.font.SysFont('Arial', 40, bold=True)
    title = title_font.render("WORDLE", True, BLACK)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
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

def get_keyboard_key(pos):
    # Use the same dimensions as in draw_keyboard
    key_height = 50
    key_margin = 6
    key_size_x = 40
    special_key_width = 65

    for row_idx, row in enumerate(keyboard_rows):
        # Calculate row width
        row_width = 0
        for key_idx, key in enumerate(row):
            if key in ["ENTER", "DEL"]:
                row_width += special_key_width
            else:
                row_width += key_size_x
            if key_idx < len(row) - 1:
                row_width += key_margin
        
        # Calculate starting x and y
        x = (SCREEN_WIDTH - row_width) // 2
        y = KEYBOARD_OFFSET_Y + row_idx * (key_height + key_margin)
        
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
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
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
            key = get_keyboard_key(event.pos)
            if key:
                handle_key_press(key)
    
    # Draw everything
    screen.fill(WHITE)
    draw_title()
    draw_grid()
    draw_keyboard()
    draw_message()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()