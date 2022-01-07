from WordleAI import WordleAI

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