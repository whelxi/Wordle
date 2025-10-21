import unittest
import sys
import os

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.game import WordleGame, LetterState
from src.assets_manager import AssetsManager

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.assets = AssetsManager()
        self.game = WordleGame(self.assets)
    
    def test_initial_state(self):
        """Test initial game state"""
        self.assertEqual(len(self.game.guesses), 6)
        self.assertEqual(self.game.current_guess, 0)
        self.assertEqual(self.game.current_letter, 0)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.won)
    
    def test_add_letter(self):
        """Test adding letters to guess"""
        self.assertTrue(self.game.add_letter('A'))
        self.assertEqual(self.game.guesses[0], 'A')
        self.assertEqual(self.game.current_letter, 1)
    
    def test_remove_letter(self):
        """Test removing letters from guess"""
        self.game.add_letter('A')
        self.game.add_letter('B')
        self.assertTrue(self.game.remove_letter())
        self.assertEqual(self.game.guesses[0], 'A')
        self.assertEqual(self.game.current_letter, 1)
    
    def test_word_evaluation(self):
        """Test word evaluation logic"""
        # Set a known target word
        self.game.target_word = "APPLE"
        
        # Test correct guess
        self.game.guesses[0] = "APPLE"
        self.game.current_guess = 0
        self.assertTrue(self.game.submit_guess())
        self.assertTrue(self.game.won)
        self.assertTrue(self.game.game_over)
        
        # Check all letters are marked correct
        for state in self.game.letter_states[0]:
            self.assertEqual(state, LetterState.CORRECT)
    
    def test_keyboard_state(self):
        """Test keyboard state tracking"""
        self.game.target_word = "APPLE"
        self.game.guesses[0] = "APPLE"
        self.game.current_guess = 0
        self.game.submit_guess()
        
        keyboard_state = self.game.get_keyboard_state()
        self.assertEqual(keyboard_state['A'], LetterState.CORRECT)
        self.assertEqual(keyboard_state['P'], LetterState.CORRECT)
        self.assertEqual(keyboard_state['L'], LetterState.CORRECT)
        self.assertEqual(keyboard_state['E'], LetterState.CORRECT)

if __name__ == '__main__':
    unittest.main()