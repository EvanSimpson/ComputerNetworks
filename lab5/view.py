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
six_hit = ('                    \n' + 
          '      +------+      \n' + 
          '      |      |      \n' + 
          '      |      0      \n' + 
          '      |     /|\     \n' + 
          '      |     / \     \n' +
          '    -----           \n')

class View():
  """
  Render the view of a hangman window in terminal
  """
  def __init__(self, window, word):
    self.window = window
    self.word = word
    self.redraw_screen()
    self.draw_blanks()
    self.print_screen()

  def redraw_screen(self):
    # default view for hangman
    self.window = ''
    self.window += blank

  def draw_blanks(self):
    self.window += ' __ '*len(self.word) + '\n'

  def print_screen(self):
    for i in self.window:
      print (i, end="")

if __name__ == '__main__':
  View([], 'test')