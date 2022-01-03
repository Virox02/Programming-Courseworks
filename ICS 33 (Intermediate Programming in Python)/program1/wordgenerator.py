# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
from goody import irange
import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    corpus_dict = {}
    word_list = [word for word in word_at_a_time(file)]
    for i in range(len(word_list)-os):
        if tuple(word_list[i+c] for c in range(os)) in corpus_dict.keys():
            if word_list[i+os] not in corpus_dict[tuple(word_list[i+c] for c in range(os))]:
                corpus_dict[tuple(word_list[i+c] for c in range(os))].append(word_list[i+os])
        else:
            corpus_dict[tuple(word_list[i+c] for c in range(os))] = [word_list[i+os]]
    return corpus_dict
    
    


def corpus_as_str(corpus : {(str):[str]}) -> str:
    corpus_str= ''
    for words, follow in sorted(corpus.items()):
        corpus_str += '  ' + str(words) + ' can be followed by any of ' + str(follow) + '\n'
    lengths = [len(follows) for follows in corpus.values()]
    corpus_str += 'min/max list lengths = ' + str(min(lengths)) + '/' + str(max(lengths)) + '\n'
    return corpus_str


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    result = start.copy()
    while count > 0:
        words = tuple(word for word in start)
        if words in corpus.keys():
            new_word = choice(corpus[words])
            result.append(new_word)
            start.append(new_word)
            start.pop(0)
            count -= 1
        else:
            result.append(None)
            break
    return result
    




        
if __name__ == '__main__':
    order_stat = prompt.for_int('Input an order statistic', None, (lambda x: x > 0), 'Illegal: Please enter a positive integer')
    text_file = goody.safe_open('Input the file name detailing the text to read', 'r', 'Illegal file name')
    corpus = read_corpus(order_stat, text_file)
    text_file.close()
    print('Corpus')
    print(corpus_as_str(corpus))
    print()
    print('Input ' + str(order_stat) + ' words at the start of the list')
    start_words = []
    for i in irange(order_stat):
        start_words.append(prompt.for_string(f'Input word {i}'))
    num_words = prompt.for_int('Input # of words to append to the end of the list', None, (lambda x: x > 0), 'Illegal: Please enter a positive integer')
    print('Random text = ' + str(produce_text(corpus, start_words, num_words)))
    
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
