"""
Python 3 implementation of a popular 2022 word game by CMG Lee licensed under CC-BY-SA 4.0
"""

import random

DEFAULT_ANSWER         = None
FORMAT_KEYBOARD_MARK_L = [' {} ', '   ' , '<{}>', '[{}]'] ## 0=white, 1=grey, 2=amber, 3=green
FORMAT_GUESS_MARK_L    = [' {} ', ' {} ', '<{}>', '[{}]']
N_LETTER               = 5
FILE_ANSWER            = 'pyordle_answers.txt'
FILE_VALID             = 'pyordle_valid.txt'
KEYBOARD               = '''
 Q W E R T Y U I O P
 A S D F G H J K L
 Z X C V B N M'''
PRAISE_L               = ['Genius', 'Magnificent', 'Impressive', 'Splendid', 'Great', 'Phew']
n_guess                = len(PRAISE_L)

## Input guess for computer's word

def input_guess(i_guess, n_guess, valid_s):
  prompt_guess = 'Enter guess {} out of {}: '.format(i_guess, n_guess)
  while True:
    guess = raw_input('\n{}'.format(prompt_guess)).strip().upper()
    if guess in valid_s: break
    display_message('"{}" is not in the word list.'.format(guess))
  if i_guess == 1:
    print('\n[ ] = letter exactly right, < > = letter in wrong position')
  return guess

## Evaluate result for a given answer

def evaluate_guess(guess, answer):
  guess_mark_l = [1] * N_LETTER
  for (i_letter_answer, letter_answer) in enumerate(answer):
    ## Mark greens
    if guess[i_letter_answer] == letter_answer:
      guess_mark_l[i_letter_answer] = 3
    else:
      ## Mark ambers and greys
      for (i_letter_guess, letter_guess) in enumerate(guess):
        if letter_guess == letter_answer and guess_mark_l[i_letter_guess] < 2:
          guess_mark_l[i_letter_guess] = 2
          break
  return guess_mark_l

## TODO: Output result

def display_result(guess, i_guess, guess_mark_l, keyboard_mark_d):
  ## Update keyboard
  ## ...
  ## Print evaluation
  ## ...
  ## Print keyboard
  ## ...
  pass

## Output message

def display_message(message):
  print('\n{}'.format(message))


## Make compatible with both Python 2 and 3

try:              raw_input
except NameError: raw_input = input

## Read words

with open(FILE_ANSWER) as f:
  answer_s = set([line.strip().upper() for line in f.readlines()])
with open(FILE_VALID) as f:
  valid_s  = set([line.strip().upper() for line in f.readlines()]).union(answer_s)
# display_message([len(answer_s), len(valid_s), list(valid_s)[0]])

## Set puzzle

answer          = DEFAULT_ANSWER or random.choice(list(answer_s))
answer          = answer.upper()
i_guess         = 0
keyboard_mark_d = {letter:0 for letter in KEYBOARD if 'A' <= letter <= 'Z'}
status          = 0 ## 0=answer not found, 1=answer found

while i_guess < n_guess:
  i_guess += 1
  ## Get guess
  guess = input_guess(i_guess, n_guess, valid_s)

  ## Evaluate guess
  guess_mark_l = evaluate_guess(guess, answer)
  display_result(guess, i_guess, guess_mark_l, keyboard_mark_d)
  if guess_mark_l == [3] * N_LETTER:
    status = 1
    break

## TODO: Output final message
## ...
