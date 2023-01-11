import re
from collections import Counter
from consts import COMMON_TWO_LETTER_WORDS, VOWELS, double_value_error, TWO_LETTER_WORD_LETTERS

def _get_list_of_words(raw_text):
    message_and_name = raw_text.split('  ~  ')
    message = re.sub("[^A-Z' ]",'', message_and_name[0])
    message = message.split('  ')
    name = message_and_name[1].split('  ')
    all_words = sorted(message, key=len)
    print (f'name: {name}\n')
    return all_words

def _get_two_letter_words(list_of_letters):
    two_letter_list = []
    for word in list_of_letters:
        if len(word) == 2:
            two_letter_list.append(word)
        elif '\'' in word:
            split_word = word.split("\'")
            if len(split_word[0]) == 2:
                two_letter_list.append(word)
    return two_letter_list
    
def _get_three_letter_words(list_of_letters):
    three_letter_list = []
    for word in list_of_letters:
        if len(word) == 3:
            three_letter_list.append(word)
        elif '\'' in word:
            split_word = word.split("\'")
            if len(split_word[0]) == 3:
                three_letter_list.append(word)
    return three_letter_list

def _get_two_letter_words_with_consts(const):
    word_matches = []
    for key in COMMON_TWO_LETTER_WORDS:
        for word in COMMON_TWO_LETTER_WORDS[key]:
            if const.lower() in word:
                word_matches.append(word)
    return word_matches 


def _get_two_letter_words_ending_with_consts(const):
    char_matches = []
    word_matches = _get_two_letter_words_with_consts(const)
    for word in word_matches:
        if word.endswith(const):
            char_matches.append(word)
    return char_matches


def _get_two_letter_words_starting_with_consts(const):
    char_matches = []
    word_matches = _get_two_letter_words_with_consts(const)
    for word in word_matches:
        if word.startswith(const):
            char_matches.append(word)
    return char_matches