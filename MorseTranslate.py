import time
import RPi.GPIO as GPIO

binMorse = {
    "1": ".",
    "111": "-",
    "":""
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

class Safeguards:
    def __enter__(self):
        return self
    def __exit__(self,*rabc):
        GPIO.cleanup()
        print("Safe exit succeeded")
        return not any(rabc)

def prepare_pin(pin=23):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin,GPIO.IN)

def read_pin(pin):
    return GPIO.input(pin)

def delay(duration):
    time.sleep(duration)

def receive(duration=.0025, pin=23):
    prepare_pin(pin)
    bin_string = ""
    buffer = []
    msg_start = False
    zero_cnt = 0
    while 1:
        if read_pin(pin):
            msg_start = True
            buffer.append(1)
            zero_cnt = 0
            delay(duration)
        elif msg_start:
            zero_cnt+=1
            if zero_cnt > 100:
                msg_start = False
                break
            buffer.append(0)
            delay(duration)
    zeroes = 0
    ones = 0
    if buffer[0] == 1:
        ones = 1
    else:
        zeroes = 1
    for i in range(len(buffer) - 1):
        if buffer[i+1] == buffer[i]:
            if buffer[i+1] == 0:
                zeroes += 1
            else:
                ones += 1
        else:
            if buffer[i+1] == 0:
                zeroes = 1
                if ones > 8:
                    bin_string += "111"
                else:
                    bin_string += "1"
                ones = 0
            else:
                ones = 1
                if zeroes <= 8:
                    bin_string += "0"
                elif zeroes > 8 and zeroes <= 26:
                    bin_string += "000"
                else:
                    bin_string += "0000000"
                zeroes = 0      
    print(bin2message(bin_string))
    return bin2message(bin_string)
    
                
def bin2message(bin):
  '''
    bin is binary string which encodes the message
    returns the uncoded message
  '''
  letters = [word.split('000') for word in bin.split("0"*7)]
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

if __name__ == "__main__":
  with Safeguards():
     receive()
