from bj import *

CODE = {'A': '.-', 'B': '-...', 'C': '-.-.',
      'D': '-..', 'E': '.', 'F': '..-.',
      'G': '--.', 'H': '....', 'I': '..',
      'J': '.---', 'K': '-.-', 'L': '.-..', 
      'M': '--', 'N': '-.', 'O': '---',
      'P': '.--.', 'Q': '--.-', 'R': '.-.',
      'S': '...', 'T': '-', 'U': '..-',
      'V': '...-', 'W': '.--', 'X': '-..-',
      'Y': '-.--', 'Z': '--..',
      '0': '-----', '1': '.----', '2': '..---',
      '3': '...--', '4': '....-', '5': '.....',
      '6': '-....', '7': '--...', '8': '---..',
      '9': '----.'
}

UNCODE = {'.-': 'A', '-...':'B', '-.-.':'C',
      '-..': 'D', '.': 'E', '..-.': 'F',
      '--.': 'G', '....': 'H', '..': 'I',
      '.---': 'J', '-.-': 'K', '.-..': 'L', 
      '--': 'M', '-.': 'N', '---': 'O',
      '.--.': 'P', '--.-': 'Q', '.-.': 'R',
      '...': 'S', '-': 'T', '..-': 'U',
      '...-': 'V', '.--': 'W', '-..-': 'X',
      '-.--': 'Y', '--..': 'Z',
      '-----': '0', '.----': '1', '..---': '2',
      '...--': '3', '....-': '4', '.....': '5',
      '-....': '6', '--...': '7', '---..': '8',
      '----.': '9'
}

morseBin = {
  '.': '10',
  '-': '1110'
}

binMorse = {
  '1' : '.',
  '111' : '-',
  '10' : '.',
  '1110' : '-'
}

def bin2message(bin):
  '''
    bin is binary string which encodes the message
    returns the uncoded message
  '''
  words = bin.split("0"*7) #this should really be 7, when the other code is fixed
  if words[len(words)-1] == "":
      words.pop()
  print(words)
  letters = [word.split('000') for word in words] 
 
  return ' '.join(map(bin2words, letters))

 
def message2bin(message):
  # input is a whole message
  message = message.upper()
  return '0000'.join(map(word2letters, message.split(' ')))+'0000' 

def bin2words(letters):
  '''
    letters is a list of binary letters
  '''
  return morse2letters(["".join([binMorse[l] for l in letter.split('0')]) for letter in letters])

def morse2bin(code):
  # input is a full string code like "--."
  return ''.join([morseBin[x] for x in list(code)])
  
def morse2letters(morse):
  '''
    morse is a morse encoded message as a list of morse letters
  '''
  return letters2words([UNCODE[morse_letter] for morse_letter in morse])

def letter2morse(letter): 
  # input is a single letter
  return morse2bin(CODE[letter])

def letters2words(letters):
  '''
    letters is a list of letters
  '''
  return ''.join(letters)

def word2letters(word):
  # input is a single word
  return '00'.join(map(letter2morse, list(word)))+'00'


if __name__ == "__main__":
  bj_layer = BJ(message2bin, bin2message)
  stack = BJ_Stack([bj_layer])
 
  print(stack.ascend(stack.descend("what a pal")))
