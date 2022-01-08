import csv
# word frequency list from https://www.kaggle.com/rtatman/english-word-frequency
# english word list from http://www.gwicks.net/dictionaries.htm

def gen_wordlist_by_length(length):
    word_list = []
    freq_list = []
    
    with open('unigram_freq.csv', 'r') as open_file:
        with open('english3.txt', 'r') as word_file:
            english_words = set(word_file.read().split('\n'))
            
            data = csv.reader(open_file)

            next(data)
            
            for row in data:
                word = row[0]
                freq = row[1]
                if len(word) == length and word in english_words:
                    word_list.append(word)
                    freq_list.append(freq)
                
    
    with open(f'unigram_freq_{length}.csv', 'w', newline='') as open_file:
        writer = csv.writer(open_file)
        writer.writerow(['word', 'frequency'])
        for idx, word in enumerate(word_list):
            writer.writerow([word, freq_list[idx]])
        
    
if __name__ == '__main__':
    gen_wordlist_by_length(5)