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
    
def internal_game(word):
    turns = 0
    ai = WordleAI(5, 'unigram_freq_5.csv')
    game = Wordle(5, word=word)
    
    while game.playing():
        guess = ai.make_guess()
        turns += 1
        print(guess)
        response = game.make_guess(guess[0])
        print(game.format_responses())
        ai.add_guess(guess[0])
        ai.add_response(response)
    
    print(game.state)
    return turns
    
if __name__ == '__main__':
    internal_game('swirl')
    '''
    import csv
    import random
    
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
        print('-' * 20)
        print(word)
        turns = internal_game(word[0])
        results['word'] = word[0]
        
    print(results)
    print(f'Avg: {sum(results.values()) / len(results)}')
    '''