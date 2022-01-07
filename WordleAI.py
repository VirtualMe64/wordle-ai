import csv

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
    
    def __gen_check_funcs(self, required_letters, forbidden_letters):
        # construct lambdas for checking if word contains required letters
        
        # print(required_letters)
        
        num_required = {}
        for letter_obj in required_letters:
            letter = letter_obj['letter']
            num_required[letter] = num_required.get(letter, 0) + 1
        
        check_funcs = []
        
        for letter in num_required:
            check_funcs.append(lambda word, letter=letter : word.count(letter) == num_required[letter])
        
        for letter_obj in required_letters:
            letter = letter_obj['letter']
            pos = letter_obj['position']
            if pos != -1:
                check_funcs.append(lambda word, letter=letter, pos=pos : word[pos] == letter)
        
        for letter in forbidden_letters:
            check_funcs.append(lambda word, letter=letter : letter not in word)
        
        # TODO TEMP DELETE LATER
        check_funcs.append(lambda word : len(set(word)) == len(word))
        check_funcs.append(lambda word : any([letter in 'aeiou' for letter in word]))
        
        return check_funcs
    
    def search_word_list(self, required_letters, forbidden_letters):
        """
        Required letters: object of form [
            {
                letter: char
                position: int, -1 if unknown
            }
        ]
        Forbidden letters: [char, char, char...]
        """
        check_funcs = self.__gen_check_funcs(required_letters, forbidden_letters)
        
        for word in self.words:
            if all([check_func(word[0]) for check_func in check_funcs]):
                return word
        
        return None
    
    """
    Response in form: [int, int, int...]
    0 = letter not in word
    1 = correct letter wrong spot
    2 = correct letter in correct spot
    """
     
    def make_guess(self):
        required_letters = []
        forbidden_letters = set()
        
        found_letters = []
        found_correct_letters = []
        
        for response, guess in zip(self.responses, self.guesses):
            '''
            Logic flow:
            1. if letter is wrong, add to forbidden_letters. Set so duplicates don't matter
            2. If letter is correct but wrong spot, this only matters if we haven't found the letter yet
            3. If letter is correct and correct spot, add to required_letters and remove wrong spot letter from required_letters
            4. Deal with words with duplicate letters somehow, TBD
            '''
            for idx in range(self.length):
                res = response[idx]
                letter = guess[idx]
                if res == 0:
                    forbidden_letters.add(letter)
                elif res == 1:
                    if letter not in found_letters: # prevent duplicates
                        required_letters.append({
                            'letter': letter,
                            'position': -1
                        })
                        found_letters.append(letter)
                        
                else:
                    assert res == 2
                    if letter not in found_correct_letters:
                        curr = {
                            'letter': letter,
                            'position': -1
                        }
                        index = required_letters.index(curr) if curr in required_letters else -1
                        if index == -1:
                            curr['position'] = idx
                            required_letters.append(curr)
                        else:
                            required_letters[index]['position'] = idx
                        found_letters.append(letter)
                        found_correct_letters.append(letter)
            
        guess = self.search_word_list(required_letters, forbidden_letters)
        if guess == None:
            raise Exception('No word found')
        else:
            return guess
        
    def add_guess(self, guess):
        self.guesses.append(guess)
    
    def add_response(self, response):
        self.responses.append(response)
            
if __name__ == '__main__':
    word_list = 'unigram_freq_5.csv'
    ai = WordleAI(5, word_list)
    
    # word is slump
    ai.guesses = ['about', 'music', 'drums']
    ai.responses = [
        [0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 2, 2, 1],
    ]
    
    guess = ai.make_guess()
    print(guess)