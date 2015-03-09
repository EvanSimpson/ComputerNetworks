blank = ('                    \n' +
        '      +------+      \n' +
        '      |      |      \n' +
        '      |             \n' +
        '      |             \n' +
        '      |             \n' +
        '    -----           \n')
one_hit = ('                    \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |             \n' +
          '      |             \n' +
          '    -----           \n')
two_hit = ('                    \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |      |      \n' +
          '      |             \n' +
          '    -----           \n')
thr_hit = ('                    \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |     /|      \n' +
          '      |             \n' +
          '    -----           \n')
for_hit = ('                    \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |     /|\     \n' +
          '      |             \n' +
          '    -----           \n')
fiv_hit = ('                    \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |     /|\     \n' +
          '      |     /       \n' +
          '    -----           \n')
six_hit = ('    GAME OVER       \n' +
          '      +------+      \n' +
          '      |      |      \n' +
          '      |      0      \n' +
          '      |     /|\     \n' +
          '      |     / \     \n' +
          '    -----           \n')
screens = [blank, one_hit, two_hit, thr_hit,
           for_hit, fiv_hit, six_hit]

class View():
  """
  Render the view of a hangman window in terminal
  """

  def __init__(self, word, guess, hits):
    """
    Takes a string window, the word (consisting of __s),
    a string for guessed letters, and an int for hits
    """
    self.window = ''
    self.word = word
    self.guess = guess
    self.hits = hits

    self.redraw_screen()
    self.print_screen()

  def redraw_screen(self):
    """
    When called, clears the window and redraws with
    the hit, known word, and possible guesses
    """
    self.window = ''
    self.window += screens[self.hits]
    self.window += self.word + '\n'
    self.window += 'Guessed: '
    for s in self.guess:
        self.window += s + ' '
    self.window += '\n'
    self.print_screen()

  def print_screen(self):
    """
    Prints out the string into the terminal.
    Python3 dictates print(,end=""), otherwise
    too many new lines
    """
    print(self.window)

  def game_over(self):
    """
    Game over screen which clears the window,
    draws a gameover hangman, then prints
    """
    self.window = ''
    self.window += gameover
    self.print_screen()
