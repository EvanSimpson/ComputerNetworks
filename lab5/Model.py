from collections import defaultdict

def makePositionDict(word):
  dic = defaultdict(list)
  for i in range(len(word)):
    dic[word[i]].append(i)

  return dic

class Model():
  def __init__(self, text):
    self._word = text
    self.blanks = '_'*len(text)
    self._positions = makePositionDict(text)
    self._remaining = list(self._positions.keys())
    self.strikes = 0

  def checkPosition(self, letter):
    positions = self._positions.get(letter, False)
    if positions == False:
      self.strikes += 1
    else:
        for i in positions:
            self.blanks = ''.join([(x, letter)[i in positions] for i,x in enumerate(self.blanks)])
        self._remaining.remove(letter)
    return positions

  def didWin(self):
    return len(self._remaining) == 0

  def reset(self, newText):
    self._positions = makePositionDict(newText)
    self._remaining = list(self._positions.keys())
    self.strikes = 0


if __name__ == "__main__":
  model = Model("hello")
  print(model.checkPosition('e'))
  print(model.checkPosition('g'))
  print(model.strikes)
  print(model.didWin())
  model.reset('goodbye')
  print(model.checkPosition('o'))
  model.reset('g')
  print(model.checkPosition('g'))
  print(model.didWin())
