from sys import intern
from WordleAI import WordleAI
from Wordle import Wordle
from GetWords import get_wordlist

def external_game():
    ai = WordleAI(5)

    done = False

    while not done:
        guess = ai.make_guess()
        print(guess)
        response = input('Enter response: ')
        if response == 'invalid':
            ai.add_invalid_word(guess)
            continue
        response = [int(x) for x in response]
        ai.add_guess(guess)
        ai.add_response(response)
        if response == [2] * ai.length:
            done == True
    
def internal_game(word, verbose=False):
    turns = 0
    ai = WordleAI(5)
    game = Wordle(5, word=word, max_guesses=20)
    
    while game.playing():
        guess = ai.make_guess()
        turns += 1
        response = game.make_guess(guess)
        if verbose:
            print(guess)
            print(game.format_responses())
        ai.add_guess(guess)
        ai.add_response(response)

    return turns

def challenge_ai():
    wordle = Wordle(5)
    
    turns = 0
    
    while wordle.playing():
        guess = input('Enter a word: ').lower()
        wordle.make_guess(guess)
        print(wordle.format_responses())
        
        turns += 1
    
    print('Now the AI will go!')
    
    ai_turns = internal_game(wordle.word, verbose=True)
    print(f"It took the ai {ai_turns} turns")
    

if __name__ == '__main__':
    import random
    
    n = 2
    
    if n == 0:
        results = {}
        words = get_wordlist()
        chosen_words = random.sample(words, 1000)
        for word in chosen_words:
            turns = internal_game(word, verbose=False)
            results[word] = turns
            
        print(results)
        print(f'Avg: {sum(results.values()) / len(results)}')
        print(f'Success %: {sum([1 for x in results.values() if x <= 6]) / len(results)}')
        
    elif n == 1:
        word = input('Enter a word: ').lower()
        print(internal_game(word, verbose=True))
        
    elif n == 2:
        external_game()
    
    elif n == 3:
        challenge_ai()