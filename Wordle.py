'''
0 = letter not in word
1 = correct letter wrong spot
2 = correct letter in correct spot
'''

import random
import GetWords

class Wordle():
    def __init__(self, length, word="", max_guesses=6):
        self.length = length
        self.guesses = []
        self.responses = []
        self.max_guesses = max_guesses
        self.state = 'playing'
        
        self.__load_word_lists()
        
        if word == "":
            self.__gen_word()
        else:
            if word not in self.wordlist:
                print('invalid word')
                self.__gen_word
            else:
                self.word = word
        
    def __gen_word(self):
        self.word = random.choice(self.wordlist)

    def __load_word_lists(self):
        self.valid_guesses = GetWords.get_valid_guesses()
        self.wordlist = GetWords.get_wordlist()
        
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
        word = word.lower()
        
        assert len(word) == self.length, 'Invalid guess length'
        assert word in self.valid_guesses, 'Invalid guess'
        
        self.guesses.append(word)
        response = [0] * self.length
        found_letters = {}
        
        # correct spot and letter scan
        for idx, letter in enumerate(word):
            if self.word[idx] == letter: # correct letter in correct spot
                response[idx] = 2
                found_letters[letter] = found_letters.get(letter, 0) + 1
        
        # correct letter scan
        for idx, letter in enumerate(word):
            if letter in self.word and self.word[idx] != letter: # correct letter in wrong spot
                if found_letters.get(letter, 0) < self.word.count(letter):
                    found_letters[letter] = found_letters.get(letter, 0) + 1
                    response[idx] = 1
                    
        self.responses.append(response)
        self.__update_state()
        
        return response
    
    def playing(self):
        """Returns true if game is in progress"""
        return self.state == 'playing'

if __name__ == '__main__':
    wordle = Wordle(5, 'slump')
    
    while wordle.playing():
        guess = input('Enter a word: ').lower()
        res = wordle.make_guess(guess)
        print(wordle.format_responses())
    
    print(wordle.state)