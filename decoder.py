import re
from collections import Counter
from consts import COMMON_TWO_LETTER_WORDS, VOWELS, double_value_error, TWO_LETTER_WORD_LETTERS, TWO_LETTER_MASK, generate_mask_from_list, generate_dict_mask
from two_letter_obj import Two_letter_obj
from three_letter_obj import Three_letter_obj
from util import _get_list_of_words

#private functions

'''
unsolved keys
rbt jmmk cks mrbtp lthtqrdch emsdtq qbmuhs et iptt imp txnhmpcrdmk cks uqt ey chh lmukrpdtq. km lmukrpy qbmuhs et ntpjdrrts rm csvcklt c lhcdj mi qmvtptdakry. - hyksmk e. fmbkqmk

'''

#start up functions
def _get_all_values(dictionary):
    solved_letters = []
    list_of_letters = list(dictionary.values())
    for val in list_of_letters:
        if val:
            if val in solved_letters:
                raise double_value_error(f'ERROR: Letter {val} exists twice!')
            solved_letters.append(val)
    return sorted(solved_letters)

def _get_solved_letters(dictionary):
    list_of_keys = []
    for i in dictionary:
        if dictionary[i]:
            list_of_keys.append(i)
    return sorted(list_of_keys)

def get_raw_text():
    f = open("codes.txt", "r")
    raw_text = f.read()
    raw_text = raw_text.replace(' ', '  ')
    raw_text = raw_text.replace('-', '~')
    return raw_text.upper()

def get_text_key():
    dictionary = {}
    with open("key.txt") as f:
        for line in f:
            line = line.replace('\n', '')
            line_array = line.split(": ")
            if line_array[-1] == "-":
                dictionary[line_array[0]] = ''
            else:
                char = line_array[-1]
                dictionary[line_array[0]] = char.upper()
    # dictionary = _sanitize_key(dictionary)
    return dictionary

def _get_blacklist_key():
    dictionary = {}
    with open("letter_blacklist.txt") as f:
        for line in f:
            line = line.replace('\n', '')
            line_array = line.split(": ")
            
            if line_array[-1] == "-":
                dictionary[line_array[0]] = ''
            else:
                #A letter cannot be blacklisted twice
                #A letter cannot be set to something it is blacklisted as
                char = line_array[-1].upper().split(" ")
                dictionary[line_array[0]] = char
    return dictionary
                
                
def substitute_string(raw_text, dictionary_key, semi_hidden=False):
    for key in dictionary_key:
        if dictionary_key[key]:
            raw_text = raw_text.replace(key, dictionary_key[key].lower())
    if semi_hidden:
        return  raw_text
    hidden_string = re.sub('[A-Z]','-', raw_text)
    return hidden_string


#algorithmic functions
def print_letter_stats(raw_text):
    all_letters = 'ABCDEFGHIJKLMNOPQURSTUVWXYZ'
    counting_dict = {}
    for char in all_letters:
        count = 0
        for letter in raw_text:
            if letter == char:
                count = count + 1
        counting_dict[char] = count
    # print (f'unordered letter counts: {counting_dict}\n')
    a = sorted(counting_dict.items(), key=lambda x: x[1])    
    print(f'ordered letter counts: {a}\n')


def print_word_stats(raw_text, extra=True):
    all_words = _get_list_of_words(raw_text)
    print(f'full list of words: {all_words}')
    if extra:
        word_length_counter={}
        word_counter = []
        word_length=0
        for word in all_words:
            if word_length != len(word):
                word_length_counter[word_length] = word_counter
                word_counter = []
                word_length = len(word)
                word_counter.append(word)
            else:
                word_counter.append(word)
        word_length_counter[word_length] = word_counter
        print(f'count: {word_length_counter}\n')





#get all dynamic vars
raw_text = get_raw_text() #the raw encoded string
dictionary_key = get_text_key() #the dictionary generated from key.txt
solved_values = _get_all_values(dictionary_key) #the list of values that have been solved 
solved_keys = _get_solved_letters(dictionary_key) #the list of keys that have been solved
blacklist_dictionary = _get_blacklist_key()
substituted_string_hidden = substitute_string(raw_text, dictionary_key)
substituted_string_open = substitute_string(raw_text, dictionary_key, True)

#run algorithms
print ('ALGORITHMS\n')
print_letter_stats(raw_text)
print_word_stats(raw_text)
Twoletter = Two_letter_obj(raw_text, dictionary_key, solved_values, blacklist_dictionary)
print(f'obj letter tracker: {Twoletter.letter_tracker}')
Threeletter = Three_letter_obj(raw_text, dictionary_key, Twoletter.letter_tracker, blacklist_dictionary, solved_keys)
print('\n')

#print vars
# print (f'raw_text: {raw_text}\n')
print ('VARS\n')
print (f'dictionary_key: {dictionary_key}\n')
print (f'solved_values: {solved_values}\n')
print (f'solved_keys: {solved_keys}\n\n')
print (f'substituted_string (ordered open): {sorted(substituted_string_open.split("  "), key=len)}\n')
print (f'substituted_string (ordered hidden): {sorted(substituted_string_hidden.split("  "), key=len)}\n')
print (f'substituted_string open: {substituted_string_open}\n')
print (f'substituted_string hidden: {substituted_string_hidden}\n')