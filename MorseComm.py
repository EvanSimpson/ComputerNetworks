import time
import RPi.GPIO as GPIO

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
  '1110' : '-',
  '' : ''
}

class Safeguards:
  def __enter__(self):
    return self
  def __exit__(self,*rabc):
    GPIO.cleanup()
    print("Safe exit succeeded")
    return not any(rabc)

def prepare_pin(pin=17):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin,GPIO.OUT)

def turn_high(pin):
    GPIO.output(pin,GPIO.HIGH)

def turn_down(pin):
    GPIO.output(pin,GPIO.LOW)
  
def delay(duration):
  time.sleep(duration)
  
def morse2bin(code):
  # input is a full string code like "--."
  return ''.join([morseBin[x] for x in list(code)])

def letter2morse(letter): 
  # input is a single letter
  return morse2bin(CODE[letter])

def word2letters(word):
  # input is a single word
  return '00'.join(map(letter2morse, list(word)))+'00'

def message2bin(message):
  # input is a whole message
  print('0000'.join(map(word2letters, message.split(' ')))+'0000') 
  return '0000'.join(map(word2letters, message.split(' ')))+'0000' 

def bin2blink(binary):
  #input is a binary string
  prepare_pin()
  blink_off(.5)
  for char in binary:
    if char=="1":
      blink_on(.1)
    elif char=="0":
      blink_off(.1)
  blink_off(.1)
      
def blink_on(duration=1, for_what=17):
  turn_high(for_what)
  delay(duration)

def blink_off(duration=1, for_what=17):
  turn_down(for_what)
  delay(duration*2)

def bin2message(bin):
  '''
  	bin is binary string which encodes the message
    returns the uncoded message
  '''
  words = bin.split("0"*5) #this should really be 7, when the other code is fixed
  letters = [word.split('000') for word in words] 
  
  print(' '.join(map(bin2words, letters)))
  return ' '.join(map(bin2words, letters))

def bin2words(letters):
	'''
		letters is a list of binary letters
	'''
	return morse2letters(["".join([binMorse[l] for l in letter.split('0')]) for letter in letters])

def morse2letters(morse):
  '''
  	morse is a morse encoded message as a list of morse letters
  '''
  return letters2words([UNCODE[morse_letter] for morse_letter in morse])

def letters2words(letters):
  '''
  	letters is a list of letters
  '''
  return ''.join(letters)

def blink(pin=17):
  prepare_pin(pin)
  message2bin(raw_input('Message to be sent:\n'))

if __name__ == "__main__":
  with Safeguards():
    bin2blink(message2bin("4 ACES"))
