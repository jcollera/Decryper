import re
from collections import Counter
from consts import COMMON_TWO_LETTER_WORDS, VOWELS, double_value_error, TWO_LETTER_WORD_LETTERS, TWO_LETTER_MASK, generate_mask_from_list, generate_dict_mask, VOWELS
from util import _get_two_letter_words_starting_with_consts, _get_list_of_words, _get_two_letter_words, _get_two_letter_words_ending_with_consts

class Two_letter_obj():
    def __init__(self, raw_text, dictionary_key, solved_values, blacklist_dictionary):
    #TODO: needs a way to manually eliminate letters
        print ('Running TWO Letter...')
        self.raw_text = raw_text
        self.solved_values = solved_values
        self.blacklist_dictionary = blacklist_dictionary
        self.dictionary_key = dictionary_key
        self.two_letter_chars = ''
        self.vowels = []
        self.consts = []
        self.two_letter_words = self._get_all_two_letter_words()
        self.letter_tracker = self.run_initial_solver_on_all_letters(self.raw_text)
        print(f'letter tracker: {self.letter_tracker}')
        self.format_solved_letters()
        #self.print_letter_tracker()
        self.run_option_cleaner()
        #self.print_letter_tracker()
        self.run_option_cleaner()
        print ('\n')
        self.print_letter_tracker()

    def _get_letter_map(self, letter):
        letter = letter.lower()
        letter_matches = []
        for key in COMMON_TWO_LETTER_WORDS:
            letter_list = COMMON_TWO_LETTER_WORDS[key]
            for word in letter_list:
                if letter in word:
                    letter_matches.append(word)
        count = {'starting': 0, 'ending': 0}
        for word in letter_matches:
            if word.startswith(letter):
                count['starting'] = count['starting']+1     
            else:
                count['ending'] = count['ending']+1
        return count

    def _get_all_two_letter_words(self):
        list_of_letters = _get_list_of_words(self.raw_text)
        two_letter_words = _get_two_letter_words(list_of_letters)
        two_letter_words = list(dict.fromkeys(two_letter_words))
        print (f'Two Letter Words: {two_letter_words}')
        return two_letter_words 

    #gets the initial possibilities only using Mask Logic
    def run_initial_solver_on_all_letters(self, text):
        letter_dict = {}
        full_string = ""
        for word in self.two_letter_words:
            full_string  += word
        unique_str = "".join(set(full_string))
        unique_str = sorted(unique_str)
        print (f'All letters in Two letter words: {unique_str}')
        self.two_letter_chars = unique_str
        for char in unique_str:
            letter_dict[char] = self.get_letter_possibilities(char)
        return letter_dict

    def get_letter_possibilities(self, letter):
        possible_letters = [] #possible letters for char that was entered
        words_containing_letter = []
        for word in self.two_letter_words:
            if letter in word:
                words_containing_letter.append(word)
        print (f'words_containing_letter: {words_containing_letter}')
        count = {'starting': 0, 'ending': 0}
        for word in words_containing_letter:
            if word.startswith(letter):
                count['starting'] = count['starting']+1
            else:
                count['ending'] = count['ending']+1
        for char in TWO_LETTER_WORD_LETTERS:
            map_count = self._get_letter_map(char)
            #print(f'letter: {char}')
            #print(f'map_count: {map_count}')
            #print(f'main_count: {count}\n')
            if map_count['starting'] >= count['starting'] and map_count['ending'] >= count['ending']:
                #removes blacklisted letters
                if (char.upper() not in self.blacklist_dictionary[letter]):
                    possible_letters.append(char)
        print (f'possible matches for char: {letter} are {possible_letters}\n')
        return possible_letters 


    def format_solved_letters(self):
        for key in self.letter_tracker:
            if self.dictionary_key[key]:
                self.letter_tracker[key] = list(self.dictionary_key[key].lower())
        print(self.letter_tracker)
        
    def _remove_all_consts(self, key):
        #print(key)
        letters = self.letter_tracker[key]
        letters_to_rm = []
        for letter in letters:
            if letter not in VOWELS:
                letters_to_rm.append(letter)
        for l in letters_to_rm: 
            self.letter_tracker[key].remove(l)

    def _remove_all_vowels(self, key):
        #print(key)
        letters = self.letter_tracker[key]
        letters_to_rm = []
        for letter in letters:
            if letter in VOWELS:
                letters_to_rm.append(letter)
        for l in letters_to_rm: 
            self.letter_tracker[key].remove(l)

    def _is_key_a_vowel(self, key):
        list_of_letters = self.letter_tracker[key]
        for char in list_of_letters:
            if char not in VOWELS:
                return False
        return True

    def _is_key_a_const(self, key):
        list_of_letters = self.letter_tracker[key]
        for char in list_of_letters:
            if char in VOWELS:
                return False
        return True

    def _update_consts(self):
        for vowel in self.vowels:
            for word in self.two_letter_words:
                if vowel in word:
                    if word.startswith(vowel):
                        if word[-1] not in self.consts:
                            self.consts.append(word[-1])

    def _update_vowels(self):
        for const in self.consts:
            for word in self.two_letter_words:
                if const in word:
                    if word.startswith(const):
                        if word[-1] not in self.vowels:
                            self.vowels.append(word[-1])
                    elif word[0] not in self.vowels:
                        self.vowels.append(word[0])


    def get_vowels_and_consts(self):
        for key in self.letter_tracker:
            if self._is_key_a_vowel(key):
                if key not in self.vowels:
                    self.vowels.append(key)
            elif self._is_key_a_const(key):
                if key not in self.consts:
                    self.consts.append(key)
        print(f'vowels: {self.vowels}')
        print(f'consts: {self.consts}')
        self._update_consts()
        self._update_vowels()

    def _get_possible_words_that_start_with(self, char):
        if char in VOWELS:
            words_containing_letter = COMMON_TWO_LETTER_WORDS[char]
        else:
            words_containing_letter = _get_two_letter_words_starting_with_consts(char)
        list_of_possible_words = []
        for word in words_containing_letter:
            if word.startswith(char):
                list_of_possible_words.append(word)
        #print(f'possible words for {char} are {list_of_possible_words}')
        return list_of_possible_words   

    def _get_possible_words_that_end_with(self, char):
        if char in VOWELS:
            words_containing_letter = COMMON_TWO_LETTER_WORDS[char]
        else:
            words_containing_letter = _get_two_letter_words_ending_with_consts(char)
        #print(f'xyz: {words_containing_letter}')
        list_of_possible_words = [] 
        for word in words_containing_letter:
            if word.endswith(char):
                list_of_possible_words.append(word)
        #print(f'possible words for {char} are {list_of_possible_words}')
        return list_of_possible_words   


    def _cut_letters_from_list(self, target_letter, possible_letters_for_key):
        text = self.letter_tracker[target_letter]
        letters_to_rm = []
        for char in text:
            if char not in possible_letters_for_key:
                letters_to_rm.append(char)
        for l in letters_to_rm:
            self.letter_tracker[target_letter].remove(l)
        if target_letter == 'M':
            print(f'Cutting letters: {letters_to_rm} from the list of {possible_letters_for_key}')
        print (self.letter_tracker)


    def _run_solving_cleaner(self):
        #TODO: Rm the options of letters that have been solved
        #if one is set in stone remove the possibility from the others
        for key in self.dictionary_key:
            if len(self.dictionary_key[key]) == 1:
                # if key in self.letter_tracker.keys():
                for solved_key in self.letter_tracker:
                    if solved_key != key:
                        if self.dictionary_key[key].lower() in self.letter_tracker[solved_key]:
                            #print(f'Removing letter: {self.dictionary_key[key].lower()} from solved_key: {solved_key}')
                            self.letter_tracker[solved_key].remove(self.dictionary_key[key].lower())


    def _run_vowel_const_cleaner(self):    
        #evaluate if a letter is a vowel/const
        #TODO: have this function repeat until nothing changes
        self.get_vowels_and_consts()
        self.get_vowels_and_consts()
        self.get_vowels_and_consts()
        for v in self.vowels:
            self._remove_all_consts(v)
        for c in self.consts:
            self._remove_all_vowels(c)

    def _get_target_letter(self, word, key):
        if word.startswith(key):
            return word[-1]
        return word[0]

    def can_key_letter_match_w_key(self, key_letter, key, start=False):
        # print (f'key: {key}')
        # print (f'key_letter: {key_letter}')
        list_of_keys_to_rm = []
        for possible_letter in self.letter_tracker[key_letter]:
            #print (f'possible_letter: {possible_letter}')
            mock_word = ''
            if start:
                mock_word+=key.lower()
                mock_word+=possible_letter
                words = self._get_possible_words_that_start_with(key.lower())
            else:
                mock_word+=possible_letter
                mock_word+=key.lower()
                words = self._get_possible_words_that_end_with(key.lower())
            # print (f'words that start with key: {words}')
            # print(f'mock word: {mock_word}')
            if mock_word not in words:
                list_of_keys_to_rm.append(possible_letter)
        return list_of_keys_to_rm

    def remove_matching_letters(self, removals, key):
        #print(f'key123: {key}')
        chars_to_rm = []
        for char in removals[0]:
            remove = True
            #print (f'char: {char}')
            for _list in removals:
                if char not in _list:
                    remove = False
            #print(f'Should we remove char: {char}?  {remove}')
            if remove:
                chars_to_rm.append(char)
        #print(f'key: {self.letter_tracker[key]}')
        for char in chars_to_rm:
            self.letter_tracker[key].remove(char)



    def _run_letter_tracking_cleaner(self):
        #order letter tracker by length of key

        #TODO make work with consts
        ordered_keys = sorted(self.letter_tracker, key = lambda key: len(self.letter_tracker[key]))
        print (ordered_keys)
        print ('match hunting')
        for key in ordered_keys:
            #key will be a letter from the list of two letter chars. 
            if len(self.letter_tracker[key]) <= 3:
                words_with_key = []
                #Find all words that contain the key
                for word in self.two_letter_words:
                    # print(f'word: {word}')
                    # print(f'key: {key}')
                    if key in word:
                        words_with_key.append(word)
                        possible_letters_for_key = []
                        target_word = word
                        target_letter = self._get_target_letter(target_word, key)
                        # print(f'target_letter: {target_letter}')
                        # print(f'self.letter_tracker[key]: {self.letter_tracker[key]}')
                #print (f'Words containing {key} are {words_with_key}')
                #loop through all possible letters for the key
                for key_word in words_with_key:
                    #loop through all the words containing the key
                    potentail_removals = []
                    for possible_letter in self.letter_tracker[key]:
                        #print(f'possible letter for {key} is {possible_letter}')
                        mock_letter = possible_letter
                        #print(f'mock letter: {mock_letter}')
                        if key_word.startswith(key):
                            key_letter = key_word[1]
                            # print(f'KEY LETTER: {key_letter}')
                            # print(f'POSSIBLE LETTER: {possible_letter}')
                            # print(f'{self.can_key_letter_match_w_key(key_letter, possible_letter, start=True)}')
                            potentail_removals.append(self.can_key_letter_match_w_key(key_letter, possible_letter, start=True))
                        else:
                            key_letter = key_word[0]
                            #print(self.can_key_letter_match_w_key(key_letter, possible_letter))
                            potentail_removals.append(self.can_key_letter_match_w_key(key_letter, possible_letter))
                    #print(f'POTENTAL REMOVALS: {potentail_removals}\n')
                    self.remove_matching_letters(potentail_removals, key_letter)
                    #             words = self._get_possible_words_that_end_with(key_letter)
                    #             print(f'words for ending: {words}')
                    #             for w in words:
                    #                 self._can_letter_be_removed(w[0])
                    #                 if w[0].upper() not in self.solved_values:
                    #                     possible_letters_for_key.append(w[0])
                    #     print (f'possible letters for letter: {target_letter} are {possible_letters_for_key}')
                    #     self._cut_letters_from_list(target_letter, possible_letters_for_key)



    def run_option_cleaner(self): 
        #go through the master dict and removed the solved letter from the options
        self._run_solving_cleaner()
        #evaluate if a letter is a vowel or const
        self._run_vowel_const_cleaner()
        self._run_solving_cleaner()
        self.print_letter_tracker()
        #look for pattern matches in the default dictionary and rm other options
        self._run_letter_tracking_cleaner()
        self._run_solving_cleaner()
        print(self.letter_tracker)

    def print_letter_tracker(self):
        for key in self.letter_tracker:
            print (f'Possibilities for letter: {key} are: {self.letter_tracker[key]}')

    def run_two_opt_cleaner(self):
        #actually subs in letters and runs checks
        #grab the shortes array and run algs
        pass

def main():
    with TestCase() as context:
        context.execute()

if __name__ == "__main__":
    main()