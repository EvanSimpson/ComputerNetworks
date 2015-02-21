class View():
  """
  Render the view of a hangman window in terminal
  """
  def __init__(self, window, word):
    self.window = window
    self.word = word
    self.default_screen()
    self.print_screen()

  def default_screen(self):
    # default view for hangman
    self.window.append(
                  '                    \n' + 
                  '  +----+            \n' + 
                  '  |    |            \n' + 
                  '  |                 \n' + 
                  '  |                 \n' + 
                  '  |                 \n' +
                  '-----               \n' +
                  '                    \n' +
                  '                    \n')

  def print_screen(self):
    for i in self.window:
      print (i)

if __name__ == '__main__':
  View([], 'test')