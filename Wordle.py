'''
0 = letter not in word
1 = correct letter wrong spot
2 = correct letter in correct spot
'''

class Wordle():
    def __init__(self, length, word=""):
        self.length = length
        self.guesses = []
        self.responses = []
        self.max_guesses = 6
        self.state = 'playing'
        if word == "":
            self.__gen_word()
        else:
            self.word = word
        
    def __gen_word(self):
        self.word = 'slump'
    
    def __update_state(self):
        if self.state == 'playing':
            if self.responses[-1] == [2] * 5:
                self.state = 'won'
            elif len(self.guesses) == self.max_guesses:
                self.state = 'lost'
        else:
            pass
    
        
    def format_responses(self):
        key = ['', '\033[93m', '\033[92m']
        endc = '\033[0m'
        out = ''
        for response, guess in zip(self.responses, self.guesses):
            for i in range(self.length):
                out += key[response[i]] + guess[i] + endc
            out += '\n'
        
        out = out.strip()
        
        return out
    
    def make_guess(self, word):
        assert len(word) == self.length
        
        self.guesses.append(word)
        response = []
        
        for idx, letter in enumerate(word):
            if letter in self.word: # correct letter
                if self.word[idx] == letter: # correct spot
                    response.append(2)
                else: # wrong spot
                    response.append(1)
            else:
                response.append(0)    
            
        self.responses.append(response)
        self.__update_state()
        
        return response
    
    def playing(self):
        """Returns true if game is in progress"""
        return self.state == 'playing'

if __name__ == '__main__':
    wordle = Wordle(5)
    
    while wordle.playing():
        guess = input('Enter a word: ').lower()
        res = wordle.make_guess(guess)
        print(wordle.format_responses())
    
    print(wordle.state)