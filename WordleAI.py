import csv
from random import choice

class WordleAI():
    def __init__(self, length, word_list):
        self.length = length
        self.guesses = []
        self.responses = []
        self.__load_word_list(word_list)

    def __load_word_list(self, word_list):
        with open(word_list, 'r') as open_file:
            data = csv.reader(open_file)
            next(data)
            words = []
            for row in data:
                word = row[0]
                freq = row[1]
                words.append((word, freq))
        
        self.words = words
    
    def __construct_letter_dict(self):
        # loop over all lowercase letters
        out = {}
        
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            out[letter] = {
                'count': 0,
                'exact_count': False,
                'correct_positions': set(),
                'wrong_positions': set()
            }
            
        return out
    
    def __gen_check_funcs(self, required_letters, forbidden_letters):
        # construct lambdas for checking if word contains required letters
            
        check_funcs = []
        
        for letter in required_letters:
            letter_obj = required_letters[letter]
            count = letter_obj['count']
            if count == 0:
                continue
            
            # print(f'{letter}: {letter_obj}')
            
            if letter_obj['exact_count']:
                check_funcs.append(lambda word, letter=letter, count=count: word.count(letter) == count)
            else:
                check_funcs.append(lambda word, letter=letter, count=count: word.count(letter) >= count)
                
            for position in letter_obj['correct_positions']:
                check_funcs.append(lambda word, letter=letter, position=position: word[position] == letter)
            for position in letter_obj['wrong_positions']:
                check_funcs.append(lambda word, letter=letter, position=position: word[position] != letter)
                
        
        for letter in forbidden_letters:
            check_funcs.append(lambda word, letter=letter : letter not in word)
        
        return check_funcs
    
    def search_word_list(self, required_letters, forbidden_letters):
        check_funcs = self.__gen_check_funcs(required_letters, forbidden_letters)
        
        for word in self.words:
            valid = True
            for check_func in check_funcs:
                if not check_func(word[0]):
                    valid = False
                    break
            if valid:
                yield word

    """
    Required letters: object of form [
        latter: {
            count: int
            exact_count: bool
            correct_positions: set(int, int, ...)
            wrong_positions: set(int, int, ...)
        }
    ]
    Forbidden letters: set(char, char, char...)
    """
        
    """
    Response in form: [int, int, int...]
    0 = letter not in word
    1 = correct letter wrong spot
    2 = correct letter in correct spot
    """
    def __parse_responses(self):
        required_letters = self.__construct_letter_dict()
        forbidden_letters = set()
        
        for response, guess in zip(self.responses, self.guesses):
            for idx in range(self.length):
                res = response[idx]
                letter = guess[idx]
                
                if res == 0:
                    if guess.count(letter) > 1: # horrible hack
                        num = 0
                        for i, l in enumerate(guess):
                            if l == letter:
                                num += 0 if response[i] == 0 else 1
                                
                        if num == 0:
                            forbidden_letters.add(letter)
                        else:
                            required_letters[letter]['wrong_positions'].add(idx)
                            required_letters[letter]['exact_count'] = True
                            required_letters[letter]['count'] = num
                            
                    else:
                        forbidden_letters.add(letter)
                    
                elif res == 1:
                    curr_info = required_letters[letter]
                    if len(curr_info['correct_positions']) == 0 and len(curr_info['wrong_positions']) == 0:
                        if not curr_info['exact_count']:
                            curr_info['count'] += 1
                    curr_info['wrong_positions'].add(idx)
                    if letter in forbidden_letters:
                        forbidden_letters.remove(letter)
                
                else:
                    assert res == 2
                    curr_info = required_letters[letter]
                    if idx not in curr_info['correct_positions'] and len(curr_info['wrong_positions']) == 0: # this means the correct position letter isn't in the count
                        if not curr_info['exact_count']:
                            curr_info['count'] += 1
                    curr_info['correct_positions'].add(idx)
                    if letter in forbidden_letters:
                        forbidden_letters.remove(letter)
        
        return required_letters, forbidden_letters
    
    def __choose_best_word(self, words):
        letter_freqs = {}
        for word in words:
            for letter in word[0]:
                letter_freqs[letter] = letter_freqs.get(letter, 0) + 1
                
        best_word = ""
        best_score = -1
        for word in words:
            seen = set()
            score = 0
            for letter in word[0]:
                if letter not in seen:
                    score += letter_freqs[letter]
                seen.add(letter)
                
            if score > best_score:
                best_word = word
                best_score = score
        return best_word
            
    
    def make_guess(self):
        required_letters, forbidden_letters = self.__parse_responses()
            
        valid_words = [x for x in self.search_word_list(required_letters, forbidden_letters)]
        if len(valid_words) == 0:
            raise Exception('No word found')
        else:
            return self.__choose_best_word(valid_words)
        
    def add_guess(self, guess):
        self.guesses.append(guess)
    
    def add_response(self, response):
        self.responses.append(response)
    
    def add_invalid_word(self, word):
        self.words.remove(word)
            
if __name__ == '__main__':
    word_list = 'unigram_freq_5.csv'
    ai = WordleAI(5, word_list)
    
    # word is slump
    ai.guesses = ['about', 'music', 'drums', 'plump']
    ai.responses = [
        [0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 2, 2, 1],
        [1, 2, 2, 2, 2]
    ]
    
    guess = ai.make_guess()
    print(guess)