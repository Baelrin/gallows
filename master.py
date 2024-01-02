from enum import Enum
import random
import json
import os

class DifficultyLevel(Enum):
   EASY = 10
   MEDIUM = 6
   HARD = 4

# Load the score from the results.json file if it exists, otherwise initialize it to 0
if os.path.exists('results.json'):
 with open('results.json', 'r') as f:
     results = json.load(f)
 score = results[-1]['score'] if results else 0
else:
 score = 0

def load_words() -> list:
 # Try to load words from the words.txt file
 try:
     with open('words.txt', 'r') as f:
         words = f.read().splitlines()
     if not words:
         raise ValueError("No words found in the file.")
     return words
 except FileNotFoundError:
     print("File 'words.txt' not found.")
     exit(1)
 except IOError:
     print("Error reading file 'words.txt'.")
     exit(1)
 except Exception as e:
     print(f"Unexpected error: {e}")
     exit(1)

def choose_word(words: list) -> str:
 # Choose a random word from the list of words
 return random.choice(words)

def display_hangman(missed_letters: list) -> None:
 # Display the hangman based on the number of missed letters
 print(" _______")
 print(" |/ |")
 print(" | %s" % ("O" if "O" in missed_letters else ""))
 print(" | %s %s" % ("/" if "/" in missed_letters else "", "\\" if "\\" in missed_letters else ""))
 print(" | %s" % ("|" if "|" in missed_letters else ""))
 print("_|_______")

def check_letter(word: str, guessed_letters: dict, letter: str) -> bool:
 # Check if the letter is in the word and has not been guessed yet
 return letter in word and letter not in guessed_letters

def choose_difficulty() -> int:
 # Ask the user to choose a difficulty level
 difficulty = input("Choose a difficulty level (easy, medium, hard): ")
 if difficulty.lower() == "easy":
     return 10
 elif difficulty.lower() == "medium":
     return 6
 elif difficulty.lower() == "hard":
     return 4
 else:
     print("Invalid choice. Defaulting to easy.")
     return 10

def check_score() -> None:
 # Check the current score
 if os.path.exists('results.json'):
     with open('results.json', 'r') as f:
         results = json.load(f)
     latest_score = results[-1]['score'] if results else 0
     print("Your current score is: ", latest_score)
 else:
     print("No scores available yet.")

def get_user_input(word: str, guessed_letters: dict, score: int) -> str:
 # Get the user's guess
 while True:
     guess = input("Guess a letter or type 'Score' to check your current score or 'Hint' to receive a hint (price: 5 score points): ")
     guess = guess.lower() # Convert to lowercase
     if not guess.isalpha():
         print("Please enter a single letter or 'Score'.")
         continue
     elif guess.lower() == "score":
         check_score()
         continue
     return guess

def save_result(word: str, attempts: int, result: str, score: int) -> None:
 # Save the result of the game
 data = {
     "word": word,
     "attempts": attempts,
     "result": result,
     "score": score # Save score
 }

 try:
     if os.path.exists('results.json'):
         with open('results.json', 'r') as f:
             results = json.load(f)
     else:
         results = []
         print("File 'results.json' has been created.")

     results.append(data)

     with open('results.json', 'w') as f:
         json.dump(results, f)
 except FileNotFoundError:
     print("File 'results.json' not found.")
     exit(1)
 except PermissionError:
     print("Permission denied to access 'results.json'.")
     exit(1)
 except Exception as e:
     print(f"Failed to save results: {e}")
     exit(1)
     
def hint(word: str, guessed_letters: dict, score: int) -> None:
  # Check if the user has enough points to use a hint
  if score >= 5:
    # Find a letter in the word that hasn't been guessed yet
    for letter in word:
      if letter not in guessed_letters:
        print("Hint: The word contains the letter '%s'" % letter)
        return
    print("No hints left.")
  else:
    print("Not enough points to use a hint.")

EASY_ATTEMPTS = 10
MEDIUM_ATTEMPTS = 6
HARD_ATTEMPTS = 4

def initialize_game(words: list) -> tuple:
   word = choose_word(words)
   guessed_letters = {}
   missed_letters = []
   displayed_word = "_" * len(word)
   max_attempts = choose_difficulty()
   return word, guessed_letters, missed_letters, displayed_word, max_attempts

def handle_user_input(word: str, guessed_letters: dict, score: int) -> str:
   while True:
       guess = input("Guess a letter or type 'Score' to check your current score or 'Hint' to receive a hint (price: 5 score points): ")
       guess = guess.lower() # Convert to lowercase
       if not guess.isalpha():
           print("Please enter a single letter or 'Score'.")
           continue
       elif guess.lower() == "score":
           check_score()
           continue
       return guess

def update_game_state(word: str, guessed_letters: dict, missed_letters: list, displayed_word: str, guess: str, score: int) -> tuple:
   if guess in guessed_letters or guess in missed_letters:
       print("You have already guessed this letter.")
       return guessed_letters, missed_letters, displayed_word, score
   if check_letter(word, guessed_letters, guess):
       guessed_letters[guess] = True
       for i in range(len(word)):
           if word[i] == guess:
               displayed_word = displayed_word[:i] + guess + displayed_word[i+1:]
       score += 1 # Increase score for correct guess
   else:
       missed_letters.append(guess)
       score -= 1 # Decrease score for incorrect guess
   return guessed_letters, missed_letters, displayed_word, score

def play_game() -> None:
   try:
       words = load_words()
       word, guessed_letters, missed_letters, displayed_word, max_attempts = initialize_game(words)
       global score

       while len(missed_letters) < max_attempts:
           display_hangman(missed_letters)
           print("Current word: ", displayed_word)
           guess = handle_user_input(word, guessed_letters, score)
           if guess.lower() == "hint":
               hint(word, guessed_letters, score)
               continue
           guessed_letters, missed_letters, displayed_word, score = update_game_state(word, guessed_letters, missed_letters, displayed_word, guess, score)

           if displayed_word == word:
               print("You won! The word was %s" % word)
               print("Your final score is %d" % score) # Display final score
               save_result(word, len(missed_letters), "won", score) # Save score
               break

           if len(missed_letters) == max_attempts:
               print("You lost! The word was %s" % word)
               print("Your final score is %d" % score) # Display final score
               save_result(word, len(missed_letters), "lost", score) # Save score
   except FileNotFoundError:
       print("File 'words.txt' not found.")
       exit(1)
   except PermissionError:
       print("Permission denied to access 'results.json'.")
       exit(1)
   except Exception as e:
       print(f"An error occurred during the game: {e}")
       exit(1)
while True:
   try:
       play_game()
       restart = input("Do you want to play again? (yes/no): ")
       if restart.lower() != "yes":
           break
   except Exception as e:
       print(f"An error occurred during the game loop: {e}")
       exit(1)

