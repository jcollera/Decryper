import re
from collections import Counter
from consts import COMMON_TWO_LETTER_WORDS, VOWELS, double_value_error, TWO_LETTER_WORD_LETTERS, TWO_LETTER_MASK, generate_mask_from_list, generate_dict_mask, VOWELS, THREE_LETTER_WORDS_AND_MASKS
from util import _get_two_letter_words_starting_with_consts, _get_list_of_words, _get_two_letter_words, _get_two_letter_words_ending_with_consts, _get_three_letter_words

class Three_letter_obj():

    def __init__(self, raw_text, dictionary_key, two_letter_possibilities, blacklist_dictionary, solved_values):
        print('Running THREE letter algs')
        self.raw_text = raw_text
        self.dictionary_key = dictionary_key
        self.two_letter_possibilities = two_letter_possibilities
        self.blacklist_dictionary = blacklist_dictionary
        self.solved_values = solved_values
        self.three_letter_words = self._get_three_letter_words()
        self._fill_three_letter_words()
        #letter map {abc, aba, abb, aab}
        #const map {cvc, cvv, vcc, ccv, vvc, vcv}
        #find if any of ther three letter words appear in two letter ones, then map in consts
        #

    def _get_three_letter_words(self):
        list_of_letters = _get_list_of_words(self.raw_text)
        three_letter_words = _get_three_letter_words(list_of_letters)
        three_letter_words = list(dict.fromkeys(three_letter_words))
        print (f'Three Letter Words: {three_letter_words}')
        return three_letter_words 
        
    def _fill_three_letter_words(self):
        for i in self.three_letter_words:
            for j in self.solved_values:
                if j in i:
                    print (i)
        
    def _get_possible_words_from_masks():
        #if a work has one solved value (exe: wIz), you can pass in [1,i] and it should return all three letter words with an i in the middle
        pass

def main():
    with TestCase() as context:
        context.execute()

if __name__ == "__main__":
    main()