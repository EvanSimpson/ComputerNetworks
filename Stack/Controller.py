import sys
import JoeSocket 
import Model
import View

class Hangman(object):

    # IP and port need to be assigned in the super
    def __init__(self,IP,port):
        self.socket, self.AF_INET, self.SOCK_DGRAM, self.timeout = JoeSocket.JoeSocket, JoeSocket.AF_INET, JoeSocket.SOCK_DGRAM, JoeSocket.timeout
        self.ownIP = IP
        self.ownPort = port
        #self.view = view.view
        self.maxStrikes = 6
        self.gameState = "setup"
        self.guessed = []
        self.mode = "uninitialized"
        self.state = "uninitialized"

    def becomeHost(self):
        self.mode = 'host'
        self.state = 'initialized'

    def becomeClient(self):
        self.mode = 'client'
        self.state = 'initialized'

    def addWordToModel(self, word):
        if self.model:
            self.model.reset(word)
        else:
            self.model = Model(word)

    def sendWordToClient(self, word):
        byteWord = bytearray(word, encoding="UTF-8")
        return self.sock.sendto(byteWord, self.clientAddress)

    def sendLetterToHost(self, letter):
        byteLetter = bytearray(letter, encoding="UTF-8")
        return self.sock.sendto(byteLetter, self.hostAddress)

    def verifyEndGame(self):
        pass

    def sendReady(self):
        msg = 'READY'
        byteMsg = bytearray(msg, encoding="UTF-8")
        return self.sock.sendto(byteMsg, self.hostAddress)


    def play(self):
        print("Welcome to Hangman 3000!\n")
        while True:

            # Setup client or host mode
            if self.mode == "uninitialized":
                initialInput = input("To start a new game, type 1 followed by the enter key.\nTo join an existing game, type 2 followed by the enter key.\n")
                if initialInput == '1':
                    self.becomeHost()
                elif initialInput == '2':
                    self.becomeClient()
                elif initialInput == 'q':
                    sys.exit(0)
                else:
                    print("\nPlease enter a valid option")

            elif self.mode == 'host':
                with self.socket(self.AF_INET, self.SOCK_DGRAM) as sock:
                    self.sock = sock
                    # Get input word
                    while True:
                        self.sock.bind((self.ownIP, self.ownPort))
                        print(self.state)
                        self.sock.settimeout(2.0)

                        # Wait for client to connect
                        while self.state == 'initialized':
                            try:
                                input_from_client, clientAddress = sock.recvfrom(1024)
                                client_message = input_from_client.decode("UTF-8")
                                print(client_message)
                                if client_message == "{Error: 0}":
                                    self.state = 'ready'
                                    self.clientAddress = clientAddress

                            except:
                                continue

                        while self.state == 'ready':
                            inputWord = input("Enter the word to be guessed:\n")
                            if not inputWord.isalpha():
                                print('The word must only contain the letters a-z.')
                                continue

                            self.model = Model.Model(inputWord.lower())
                            self.view = View.View('_'*len(inputWord), [], 0)
                            self.sendWordToClient(inputWord.lower())
                            self.state = 'play'

                        # Begin play mode
                        while self.state == 'play':
                            try:
                                input_letter_bits, client_address = sock.recvfrom(1024)
                                input_letter = input_letter_bits.decode("UTF-8")

                                if len(input_letter) == 1:
                                    if input_letter not in self.guessed:
                                        self.guessed.append(input_letter)
                                        newPositions = self.model.checkPosition(input_letter)
                                        self.view.guess = self.guessed
                                        self.view.hits = self.model.strikes
                                        self.view.word = self.model.blanks
                                        if self.model.strikes == self.maxStrikes:
                                            self.state = 'win'
                                        elif self.model.didWin():
                                            self.state = 'lose'
                                        self.view.redraw_screen()
                                        continue
                                elif input_letter == "quit":
                                    print('Partner has left.')
                                    sys.exit(0)

                            except:
                                continue

                        break

            elif self.mode == 'client':
                with self.socket(self.AF_INET, self.SOCK_DGRAM) as sock:
                    self.sock = sock

                    # Get user to manually input host IP/port
                    while self.state == 'initialized':
                        inputIP = input('Please input the host IP Address\n')
                        inputPort = input('Please input the host Port\n')
                        self.hostAddress = (inputIP, int(inputPort))
                        self.sendReady()
                        self.state = 'ready'

                    # Wait for input word to come from host
                    while self.state == 'ready':
                        try:
                            inputWord, hostAddress = sock.recvfrom(1024)
                            self.view = View.View('_'*len(inputWord), [], 0)
                            self.model = Model.Model(inputWord.decode("UTF-8"))
                            self.state = 'play'
                        except:
                            continue

                    # Begin game
                    while self.state == 'play':
                        inputLetter = input('Enter a letter to guess or type `quit` to quit:\n')
                        self.sendLetterToHost(inputLetter)

                        if len(inputLetter) == 1:
                            if inputLetter not in self.guessed:
                                self.guessed.append(inputLetter)
                                newPositions = self.model.checkPosition(inputLetter)
                                self.view.guess = self.guessed
                                self.view.hits = self.model.strikes
                                self.view.word = self.model.blanks
                                if self.model.strikes == self.maxStrikes:
                                    self.state = 'lose'
                                elif self.model.didWin():
                                    self.state = 'win'
                                self.view.redraw_screen()
                                continue
                        elif inputLetter == "quit":
                            print('Quitting...')
                            sys.exit(0)

            if self.state == 'win':
                print("You win!")
                break

            if self.state == 'lose':
                print("You lose!")
                break

if __name__ == "__main__":
   IP = 'localhost'
   port = "19"
   host = Hangman(IP, port)
   host.play()
