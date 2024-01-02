import random

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
   print(" |/   |")
   print(" |    %s" % ("O" if "O" in missed_letters else ""))
   print(" |  %s %s" % ("/" if "/" in missed_letters else "", "\\" if "\\" in missed_letters else ""))
   print(" |    %s" % ("|" if "|" in missed_letters else ""))
   print("_|_______")

def check_letter(word, guessed_letters, letter):
   if letter in word:
       return True
   else:
       return False

def play_game():
  words = load_words()
  word = choose_word(words)
  guessed_letters = {}
  missed_letters = []
  displayed_word = "_" * len(word)

  while len(missed_letters) < 6:
      display_hangman(missed_letters)
      print("Current word: ", displayed_word)
      guess = input("Guess a letter: ")
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
      else:
          missed_letters.append(guess)

  if len(missed_letters) == 6:
      print("You lost! The word was %s" % word)
  else:
      print("You won! The word was %s" % word)

play_game()