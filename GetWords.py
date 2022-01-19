import json

def get_valid_guesses():
    with open('words/valid_guesses.json', 'r') as open_file:
        valid_words = json.load(open_file)
    
    return valid_words + get_wordlist()

def get_wordlist():
    with open('words/wordlist.json', 'r') as open_file:
        return json.load(open_file)