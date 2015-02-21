from collections import defaultdict

def makePositionDict(word):
  dic = defaultdict(list)
  for i in range(len(word)):
    dic[word[i]].append(i)

  return dic

class Model():
  def __init__(self, text):
    self._positions = makePositionDict(text)
    self.strikes = 0

  def checkPosition(self, letter):
    positions = self._positions.get(letter, False)
    if positions == False:
      self.strikes += 1
    return positions

  def reset(self, newText):
    self._positions = makePositionDict(newText)
    self.strikes = 0


if __name__ == "__main__":
  model = Model("hello")
  print(model.checkPosition('e'))
  print(model.checkPosition('g'))
  print(model.strikes)
  model.reset('goodbye')
  print(model.checkPosition('o'))
