import random
from enum import Enum

class LetterState(Enum):
    CORRECT = "correct"      # Green - correct letter in correct position
    PRESENT = "present"      # Yellow - correct letter in wrong position
    ABSENT = "absent"        # Gray - letter not in word
    EMPTY = "empty"          # Default state
    TYPING = "typing"        # Currently being typed

class WordleGame:
    def __init__(self, assets_manager):
        self.assets = assets_manager
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        self.target_word = random.choice(self.assets.word_list).upper()
        self.guesses = [""] * 6  # 6 empty guesses
        self.current_guess = 0
        self.current_letter = 0
        self.game_over = False
        self.won = False
        self.letter_states = [[LetterState.EMPTY for _ in range(5)] for _ in range(6)]
        
        print(f"Target word: {self.target_word}")  # For debugging
    
    def add_letter(self, letter):
        """Add a letter to the current guess"""
        if self.game_over or self.current_guess >= 6:
            return False
        
        if self.current_letter < 5:
            if len(self.guesses[self.current_guess]) <= self.current_letter:
                self.guesses[self.current_guess] += letter
            else:
                # Replace existing letter
                guess_list = list(self.guesses[self.current_guess])
                guess_list[self.current_letter] = letter
                self.guesses[self.current_guess] = "".join(guess_list)
            
            self.current_letter += 1
            return True
        return False
    
    def remove_letter(self):
        """Remove the last letter from current guess"""
        if self.game_over or self.current_guess >= 6:
            return False
        
        if self.current_letter > 0:
            self.current_letter -= 1
            guess_list = list(self.guesses[self.current_guess])
            guess_list[self.current_letter] = ""
            self.guesses[self.current_guess] = "".join(guess_list)
            return True
        return False
    
    def submit_guess(self):
        """Submit the current guess and evaluate it"""
        if (self.game_over or self.current_guess >= 6 or 
            len(self.guesses[self.current_guess]) != 5):
            return False
        
        guess = self.guesses[self.current_guess].upper()
        
        # Validate guess is in word list
        if guess not in self.assets.word_list:
            print(f"Word '{guess}' not in word list!")
            return False
        
        # Evaluate the guess
        self._evaluate_guess(guess)
        
        # Check if won
        if guess == self.target_word:
            self.game_over = True
            self.won = True
            print("You won!")
        elif self.current_guess == 5:  # Last guess (6 attempts: 0-5)
            self.game_over = True
            self.won = False
            print(f"Game over! The word was: {self.target_word}")
        else:
            self.current_guess += 1
            self.current_letter = 0
        
        return True
    
    def _evaluate_guess(self, guess):
        """Evaluate the guess and set letter states according to Wordle rules"""
        target_letters = list(self.target_word)
        guess_letters = list(guess)
        result = [LetterState.ABSENT] * 5
        
        # First pass: mark correct letters (green)
        for i in range(5):
            if guess_letters[i] == target_letters[i]:
                result[i] = LetterState.CORRECT
                target_letters[i] = None  # Mark as used
        
        # Second pass: mark present letters (yellow)
        for i in range(5):
            if result[i] == LetterState.CORRECT:
                continue  # Skip already correct letters
            
            if guess_letters[i] in target_letters:
                # Find the first occurrence in target that hasn't been used
                for j in range(5):
                    if target_letters[j] == guess_letters[i]:
                        result[i] = LetterState.PRESENT
                        target_letters[j] = None  # Mark as used
                        break
        
        # Update the letter states for the current guess
        for i in range(5):
            self.letter_states[self.current_guess][i] = result[i]
    
    def get_keyboard_state(self):
        """Get the state of each letter on the keyboard"""
        keyboard_state = {}
        
        for guess_idx in range(self.current_guess + 1):
            for letter_idx in range(5):
                if guess_idx < len(self.guesses) and letter_idx < len(self.guesses[guess_idx]):
                    letter = self.guesses[guess_idx][letter_idx].upper()
                    state = self.letter_states[guess_idx][letter_idx]
                    
                    # Only update if we have a better state
                    if letter not in keyboard_state:
                        keyboard_state[letter] = state
                    else:
                        # CORRECT > PRESENT > ABSENT
                        current_state = keyboard_state[letter]
                        if (state == LetterState.CORRECT or 
                            (state == LetterState.PRESENT and current_state == LetterState.ABSENT)):
                            keyboard_state[letter] = state
        
        return keyboard_state
    
    def can_submit(self):
        """Check if current guess can be submitted"""
        return (not self.game_over and 
                self.current_guess < 6 and 
                len(self.guesses[self.current_guess]) == 5)
    
    def is_valid_word(self, word):
        """Check if a word is in the valid word list"""
        return word.upper() in self.assets.word_list