"""
Python 3 implementation of a popular 2022 word game by CMG Lee licensed under CC-BY-SA 4.0

Usage: python3 pyordle.py [GAME_MODE] [0 for no GUI or 1 to use tkinter] [ANSWER for testing]

where GAME_MODE is one of

game:   Player guesses a word computer picks
hint:   Player guesses a word computer picks (possible words shown)
solver: Computer solves a word player or http://hellowordl.net picks
demo:   Computer plays against itself

TODO: Reimplement as a class
TODO: Improve error-handling
"""

import sys, time, random

DEFAULT_ANSWER         = None
DEFAULT_GAME_MODE      = 'game'
FIRST_GUESS            = 'RAISE'
LABEL_PX               = 70
COLOUR_BG              = 'white'
COLOUR_MARK_L          = ['white', 'grey', 'yellow', 'lime']
FREQUENCY_TIEBREAK_D   = {letter:i_letter * 0.01 for (i_letter, letter) in
                           enumerate('EARIOTNSLCUDPMHGBFYWKVXZJQ'[::-1])}
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

## Remove possible words not matching evaluation

def trim_possible(possible_s, guess, guess_mark_l):
  for word in possible_s.copy():
    if evaluate_guess(guess, word) != guess_mark_l:
      possible_s.remove(word)

## Choose next guess
## TODO: Implement a better algorithm using word commonness

def choose_guess(possible_s):
  n_possible = len(possible_s)
  ## Rank letters by descending frequency in possible_s
  frequency_d = {}
  for word in possible_s:
    for letter in word:
      if letter not in frequency_d: frequency_d[letter] = 0
      frequency_d[letter] += 1
  # print(sorted(frequency_d.items(), key=lambda x:x[1])[:9])
  ## Assign scores to words in possible_s
  score_d = {}
  for word in possible_s:
    score_d[word] = sum([frequency_d[letter] + FREQUENCY_TIEBREAK_D[letter]
                         for letter in word]) / (N_LETTER - len(set(word)) + 2)
  sorted_score_l = sorted(list(score_d), key=lambda word:score_d[word], reverse=True)
  print(', '.join(['{}:{:.2f}'.format(word, score_d[word]) for word in sorted_score_l][:5]))
  if is_gui:
    label_title.configure(text=','.join(['{}'.format(word) for word in sorted_score_l][:5]))
  return sorted_score_l[0]

## Input guess for computer's word

def input_guess(i_guess, n_guess, valid_s):
  global gui_input ## must set as global as value will be changed
  gui_input    = ''
  prompt_guess = 'Enter guess {} out of {}: '.format(i_guess, n_guess)
  if game_mode == 'GAME' or i_guess == 1:
    display_message(prompt_guess, False)
  while True:
    if is_gui:
      window.mainloop()
      guess = gui_input
    else:
      guess = raw_input('\n{}'.format(prompt_guess)).strip().upper()
    if guess in valid_s: break
    display_message('"{}" is not in the word list.'.format(guess))
  if i_guess == 1:
    print('\n[ ] = letter exactly right, < > = letter in wrong position')
  return guess

## Input results for computer's guess

def input_evaluation(guess):
  prompt_mark = '''
Play {} and then enter the result as 5 digits, such as 12231
where 1=totally wrong, 2=wrong position, 3=exactly right: '''.format(guess)
  return [int(mark) for mark in raw_input(prompt_mark).strip()]

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

## Animate letter

def animate_letter(label, i_fraction):
  label.configure(width=LABEL_PX * i_fraction // 5)
  label.update()
  time.sleep(0.03)

## Output result

def display_result(guess, i_guess, guess_mark_l, keyboard_mark_d):
  ## Update keyboard
  for (i_letter_guess, letter_guess) in enumerate(guess):
    if keyboard_mark_d[letter_guess] < guess_mark_l[i_letter_guess]:
      keyboard_mark_d[letter_guess] = guess_mark_l[i_letter_guess]
  ## Print evaluation
  output = '\n'
  for (i_letter, letter) in enumerate(guess):
    output += ' ' + FORMAT_GUESS_MARK_L[guess_mark_l[i_letter]].format(letter)
  print(output)
  ## Print keyboard
  output = KEYBOARD
  for letter in keyboard_mark_d:
    output = output.replace(letter, FORMAT_KEYBOARD_MARK_L[keyboard_mark_d[letter]].format(letter))
  print(output)

  if is_gui:
    for (i_letter, letter) in enumerate(guess):
      label = label_ll[i_guess][i_letter]
      for i_frame in range(5): animate_letter(label, 4.5 - i_frame)
      label.configure(bg=COLOUR_MARK_L[guess_mark_l[i_letter]])
      for i_frame in range(5): animate_letter(label, 1 + i_frame)
      button_d[letter].configure(bg=COLOUR_MARK_L[keyboard_mark_d[letter]])

## Output message

def display_message(message, is_print=True):
  if is_print:
    print('\n{}'.format(message))
  if is_gui:
    for length in range(len(message)):
      label_title.configure(text=message[:length + 1])
      label_title.update()
      time.sleep(0.01)


## Make compatible with both Python 2 and 3

try:              raw_input
except NameError: raw_input = input

## Set game mode (GAME by default)

game_mode = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GAME_MODE).upper()
print('PYORDLE IN {} MODE'.format(game_mode))

## TODO: Make GUI for solver mode
is_gui = game_mode != 'SOLVER' and (len(sys.argv) <= 2 or sys.argv[2] == '1')

## Set up GUI if needed
## TODO: Run all program logic in mainloop instead of starting and stopping it
## TODO: Make window resizable

if is_gui:
  try:                import tkinter as tk, tkinter.font as tkFont
  except ImportError: is_gui = False
if is_gui:
  window = tk.Tk(className='Pyordle')
  window.configure(bg=COLOUR_BG)
  window.resizable(False, False)
  window.bind_all('<Key>', lambda event:input_key(event.char))
  window.bind_all('<Control-c>', exit)
  tkFont.nametofont('TkDefaultFont').configure(family='Courier', size=18)
  frame_header = tk.Frame(master=window, bg=COLOUR_BG)
  frame_guess  = tk.Frame(master=window, bg=COLOUR_BG)
  frame_footer = tk.Frame(master=window, bg=COLOUR_BG, padx=20, pady=4)
  frame_header.pack()
  frame_guess .pack()
  frame_footer.pack()
  label_title = tk.Label(master=frame_header, font=('sans-serif', 10), bg=COLOUR_BG)
  label_title.pack()
  ## Draw guesses
  image_dummy = tk.PhotoImage()
  label_ll    = [None]
  for i_guess in range(n_guess):
    label_l = []
    for i_letter in range(N_LETTER):
      label = tk.Label(master=frame_guess, width=LABEL_PX, height=LABEL_PX, relief='groove',
                       image=image_dummy, compound=tk.CENTER, bg=COLOUR_BG, text=' ')
      label.grid(row=i_guess, column=i_letter, padx=2, pady=4)
      label_l.append(label)
    label_ll.append(label_l)
  ## Draw keyboard
  button_d       = {}
  button_label_d = {'ENTER':'\u21B5', 'BACKSPACE': '\u232B'}
  for (i_row, row) in enumerate(KEYBOARD.strip().split('\n')):
    i_column = i_row % 2
    if i_row == 2: row = 'ENTER {} BACKSPACE'.format(row)
    for (i_key, key) in enumerate(row.split()):
      columnspan = 3 if key in button_label_d else 2
      width      = 2 if key in button_label_d else 1
      button_d[key] = tk.Button(master=frame_footer, width=width, height=1, padx=1, pady=1,
                                relief='raised', bg=COLOUR_BG, text=button_label_d.get(key, key),
                                command=lambda key=key:input_key(key)) ## see Python closure
      button_d[key].grid(row=i_row, column=i_column, columnspan=columnspan, padx=2, pady=2)
      i_column += columnspan
  gui_input = '' ## input from GUI

def input_key(key): ## callback on keypress or click on GUI
  global gui_input ## must set as global as value will be changed
  key = key.upper()
  if   key == '\x1b': ## Escape
    exit()
  elif key == '\x08' or key == 'BACKSPACE':
    if len(gui_input) > 0:
      gui_input = gui_input[:-1]
      label_ll[i_guess][len(gui_input)].configure(text=' ') ## label shrinks if text=''
  elif key == '\x0d' or key == 'ENTER':
    window.quit()
  elif key >= 'A' and key <= 'Z' and len(gui_input) < N_LETTER:
    label_ll[i_guess][len(gui_input)].configure(text=key)
    gui_input += key


## Read words

with open(FILE_ANSWER) as f:
  answer_s = set([line.strip().upper() for line in f.readlines()])
with open(FILE_VALID) as f:
  valid_s  = set([line.strip().upper() for line in f.readlines()]).union(answer_s)
# print(len(answer_s), len(valid_s), valid_s[0])

## Set puzzle

if game_mode != 'SOLVER': answer = DEFAULT_ANSWER or random.choice(list(answer_s))
if len(sys.argv) > 3:     answer = sys.argv[3]
answer          = answer.upper()
i_guess         = 0
keyboard_mark_d = {letter:0 for letter in KEYBOARD if 'A' <= letter <= 'Z'}
status          = 0 ## 0=answer not found, 1=answer found, 2=results do not match possible answers

while i_guess < n_guess:
  i_guess += 1
  ## Get guess
  if game_mode != 'GAME':
    if i_guess == 1:
      guess      = FIRST_GUESS
      possible_s = valid_s.copy() ## set of words matching results so far
    else:
      trim_possible(possible_s, guess, guess_mark_l)
      n_possible = len(possible_s)
      print('\nPossible words left: {}'.format(n_possible))
      if n_possible < 1:
        status = 2
        break
      guess = choose_guess(possible_s)
  if game_mode in ['GAME', 'HINT']:
    guess = input_guess(i_guess, n_guess, valid_s)

  ## Evaluate guess
  if game_mode == 'SOLVER':
    guess_mark_l = input_evaluation(guess)
  else:
    guess_mark_l = evaluate_guess(guess, answer)
  display_result(guess, i_guess, guess_mark_l, keyboard_mark_d)
  if guess_mark_l == [3] * N_LETTER:
    status = 1
    break

if status == 0:
  display_message('Sorry, the answer is {}.'.format(answer))
elif status == 1:
  display_message('{}, got {} in {}!'.format(PRAISE_L[i_guess - 1], guess, i_guess))
else:
  display_message('No words fit the results above.')

## Wait until Esc is pressed or window is closed
## TODO: Disable backspace and letter keys
if is_gui: window.mainloop()
