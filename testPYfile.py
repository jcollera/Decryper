import re
from collections import Counter
from consts import COMMON_TWO_LETTER_WORDS, VOWELS, double_value_error, TWO_LETTER_WORD_LETTERS, TWO_LETTER_MASK, generate_mask_from_list, generate_dict_mask, VOWELS
from util import _get_two_letter_words_starting_with_consts, _get_list_of_words, _get_two_letter_words, _get_two_letter_words_ending_with_consts

class one_letter_obj():
    def __init__(self, raw_text, dictionary_key, solved_values):
        print("Running ONE letter...")
        self.raw_text = raw_text
        self.dictionary_key = dictionary_key
        self.solved_values = solved_values
        #if either 'A' or 'I' is solved then we can return
        #A cannot be fallowed by a verb
        #rules for A and I in 2-3 letter words:
            #A or I cannot be at the end of a two letter word
            #A cannot be at the beginning of a two letter word
            #A cannot be in a one or two letter contaction
            
        #if rules fail, it is okay to return the option. it will be used in the two letter
            
        