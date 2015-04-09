from codes import *

def morse_up(bin_input):
  print("in morse up")
  b = bin2bytearray(bin_input)
  print("out")
  print(b)
  return b

def morse_down(bytearray_input):
  return bytearray2bin(bytearray_input)

def bytearray2bin(bytearray_message):
  '''
    takes a message as a bytearray and turns it into binary
  '''
  return message2bin(''.join([chr(b) for b in bytearray_message]))

def bin2bytearray(bin_message):
  '''
  takes a binary string and turns it into the message as a bytearray
  '''
  print("more 1")
  return bytearray([ord(c) for c in bin2message(bin_message)])

def bin2message(bin_message):
  '''
    bin is binary string which encodes the message
    returns the uncoded message
  '''
  print("more 2")
  words = bin_message.split("0"*7) #this should really be 7, when the other code is fixed
  if words[len(words)-1] == "":
      words.pop()
  bin_letters = [word.split('000') for word in words]

  return ' '.join(map(bin2morse, bin_letters))

def message2bin(message):
  '''
    input is a whole message
  '''
  message = message.upper()
  return '0000'.join(map(word2letters, message.split(' ')))+'0000'

def bin2morse(letters):
  '''
    letters is a list of binary letters
  '''
  print("more 3")
  print("letters: " + str(letters))
  print(["".join([binMorse[l] for l in letter.split('0')]) for letter in letters])
  return morse2letters(["".join([binMorse[l] for l in letter.split('0')]) for letter in letters])

def morse2bin(code):
  '''
    input is a full string code like "--."
  '''
  return ''.join([morseBin[x] for x in list(code)])

def morse2letters(morse):
  '''
    morse is a morse encoded message as a list of morse letters
  '''
  print("more 4")
  return letters2words([UNCODE[morse_letter] for morse_letter in morse])

def letter2morse(letter):
  # input is a single letter
  return morse2bin(CODE[letter])

def letters2words(letters):
  '''
    letters is a list of letters
  '''
  print("more 5")
  return ''.join(letters)

def word2letters(word):
  # input is a single word
  letters = list(word)
  to_remove = []
  for letter in letters:
    if letter not in CODE:
      to_remove.append(letter)
  
  for letter in to_remove:
    letters.remove(letter)

  return '00'.join(map(letter2morse, letters))+'00'

if __name__ == "__main__":
  binary = morse_down(bytearray("hello", encoding="UTF-8"))
  out = morse_up(binary)