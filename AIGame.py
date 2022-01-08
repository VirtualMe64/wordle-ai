from sys import intern
from WordleAI import WordleAI
from Wordle import Wordle

def external_game():
    ai = WordleAI(5, 'unigram_freq_5.csv')

    done = False

    while not done:
        guess = ai.make_guess()
        print(guess)
        response = [int(x) for x in input('Enter response: ')]
        ai.add_guess(guess[0])
        ai.add_response(response)
        if response == [2] * ai.length:
            done == True
    
def internal_game(word, verbose=False):
    turns = 0
    ai = WordleAI(5, 'unigram_freq_5.csv')
    game = Wordle(5, word=word)
    
    while game.playing():
        guess = ai.make_guess()
        turns += 1
        response = game.make_guess(guess[0])
        if verbose:
            print(guess)
            print(game.format_responses())
        ai.add_guess(guess[0])
        ai.add_response(response)
    
    if game.state == 'lost':
        turns = -1
    
    if verbose:
        print(game.state)
    return turns
    
if __name__ == '__main__':
    import csv
    import random
    
    n = 0
    
    if n == 0:
        with open('unigram_freq_5.csv', 'r') as open_file:
            data = csv.reader(open_file)
            next(data)
            words = []
            for row in data:
                word = row[0]
                freq = row[1]
                words.append((word, freq))
        
        results = {}
        chosen_words = random.sample(words, 100)
        for word in chosen_words:
            turns = internal_game(word[0], verbose=False)
            results[word[0]] = turns
            
        print(results)
        print(f'Avg: {sum([x for x in results.values() if x != -1]) / len(results)}')
        print(f'Success %: {sum([1 for x in results.values() if x != -1]) / len(results)}')
    elif n == 1:
        print(internal_game('slums', verbose=True))
    elif n == 2:
        external_game()