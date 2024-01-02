import random
import json
import os

if os.path.exists('results.json'):
  with open('results.json', 'r') as f:
      results = json.load(f)
  score = results[-1]['score'] if results else 0
else:
  score = 0

def load_words():
 with open('words.txt', 'r') as f:
      words = f.read().splitlines()
 if not words:
      raise ValueError("No words found in the file.")
 return words

def choose_word(words):
 return random.choice(words)

def display_hangman(missed_letters):
 print(" _______")
 print(" |/ |")
 print(" | %s" % ("O" if "O" in missed_letters else ""))
 print(" | %s %s" % ("/" if "/" in missed_letters else "", "\\" if "\\" in missed_letters else ""))
 print(" | %s" % ("|" if "|" in missed_letters else ""))
 print("_|_______")

def check_letter(word, guessed_letters, letter):
 return letter in word

def choose_difficulty():
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

def check_score():
 if os.path.exists('results.json'):
     with open('results.json', 'r') as f:
         results = json.load(f)
     latest_score = score
     print("Your current score is: ", latest_score)
 else:
     print("No scores available yet.")

def get_user_input(word, guessed_letters, score):
 while True:
     guess = input("Guess a letter or type 'Score' to check your current score: ")
     guess = guess.lower() # Convert to lowercase
     if not guess.isalpha():
         print("Please enter a single letter or 'Score'.")
         continue
     elif guess.lower() == "score":
       check_score()
       continue
     return guess

def save_result(word, attempts, result, score):
 data = {
      "word": word,
      "attempts": attempts,
      "result": result,
      "score": score # Save score
  }

 if os.path.exists('results.json'):
     with open('results.json', 'r') as f:
         results = json.load(f)
 else:
     results = []

 results.append(data)

 with open('results.json', 'w') as f:
     json.dump(results, f)

def play_game():
 words = load_words()
 word = choose_word(words)
 guessed_letters = {}
 missed_letters = []
 displayed_word = "_" * len(word)
 max_attempts = choose_difficulty()
 global score
 
 while len(missed_letters) < max_attempts:
     display_hangman(missed_letters)
     print("Current word: ", displayed_word)
     guess = get_user_input(word, guessed_letters, score)
     if not guess.isalpha():
         print("Please enter a letter.")
         continue
     if guess in guessed_letters or guess in missed_letters:
         print("You have already guessed this letter.")
         continue
     if check_letter(word, guessed_letters, guess):
         guessed_letters[guess] = True
         for i in range(len(word)):
             if word[i] == guess:
               displayed_word = displayed_word[:i] + guess + displayed_word[i+1:]
         score += 1 # Increase score for correct guess
     else:
         missed_letters.append(guess)
         score -= 1 # Decrease score for incorrect guess

     if displayed_word == word:
         print("You won! The word was %s" % word)
         print("Your final score is %d" % score) # Display final score
         save_result(word, len(missed_letters), "won", score) # Save score
         break

 if len(missed_letters) == max_attempts:
     print("You lost! The word was %s" % word)
     print("Your final score is %d" % score) # Display final score
     save_result(word, len(missed_letters), "lost", score) # Save score

while True:
 play_game()
 restart = input("Do you want to play again? (yes/no): ")
 if restart.lower() != "yes":
     break