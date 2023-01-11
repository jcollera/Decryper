import re

def generate_mask_from_dict(dictionary):
    mask = generate_dict_mask(dictionary)
    masked_list = []
    for key in dictionary:
        for word in dictionary[key]:
            masked_list.append(word)

    for key in mask:
        masked_list = [sub.replace(key, f'{mask[key]} ') for sub in masked_list]
    final_list = []
    return format_mask_list(masked_list)

def generate_mask_from_list(list_obj):
    mask = generate_list_mask(list_obj)
    print (f'mask: {mask}')
    masked_list = list_obj
    for key in mask:
        masked_list = [sub.replace(key, f'{mask[key]} ') for sub in masked_list]
    masked_list = list(dict.fromkeys(masked_list))
    return format_mask_list(masked_list)

def generate_list_mask(list_obj, count=1):
    mask = {}
    for word in list_obj:
            for letter in word:
                if letter not in mask:
                    mask[letter] = str(count)
                    count = count + 1
    return mask

def generate_dict_mask(dictionary, count=1):
    mask = {}
    for key in dictionary:
        mask[key] = str(count)
        count = count + 1

    for key in dictionary:
        list_of_words = dictionary[key]
        for word in list_of_words:
            for letter in word:
                if letter not in mask:
                    mask[letter] = str(count)
                    count = count + 1
    return mask

def format_mask_list(masked_list):
    new_list = []
    for key in masked_list:
        key = key.strip().split(' ')
        new_list.append(list(key))
    return new_list

def get_three_letter_words_from_masks(mask):
    words = []
    with open(f"3_letter_words/{mask}_masks.txt") as f:
        for line in f:
            line = line.replace('\n', '')
            words.append(line)
    return words
            



#rules:
'''
no two letter word is made of vowels
no two letter word starts with 'E', 'f', 'p', 'r', 'Y'
no two letter word ends in 'A', 'U', 'I', 'b', 'w', 'g', 'd'
letters that can be at beginning or end: 'm', 'O', 't', 's', 'n'
single use consts: 'w', 'g', 'd'
double use letters (start): 'b', 'm'
double use letters (end): 'n', 's', 't', 'f'
none of the 'a' words can be used and contractions

A: cannot be: b,h,r,p,f,d,g,w
E: cannot be: 
I: cannot be:
O: cannot be:
U: cannot be:
Y: cannot be:
'''
VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']

TWO_LETTER_WORD_LETTERS = ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'y']

COMMON_TWO_LETTER_WORDS = {'a': ['am', 'an', 'as', 'at'],
                            'e': ['be', 'he', 'me', 'we'],
                            'i': ['if', 'in', 'is', 'it'],
                            'o': ['of', 'on', 'or', 'do', 'go', 'no', 'so', 'to'],
                            'u': ['up', 'us'],
                            'y': ['by', 'my']}

UNRELATED_THREE_LETTER_WORDS = ['you', 'the', 'and', 'our', 'get', 'are']

TH_WORDS = {'a': ['that', 'than', 'thank'],
            'e': ['there', 'they', 'then', 'these', 'them', 'their'],
            'i': ['this', 'think'],
            'o': ['thought']
            }

COMMON_CONTRACTIONS = {'s': ['he', 'she', 'it', 'that', 'their'],
                        't': ['isn', 'don', 'won', 'can'],
                        'm': ['i'],
                        'd': ['you', 'he', 'she', 'i', 'they', 'we', 'that', 'it'],
                        'll': ['you', 'they', 'that', 'i', 'we', 'he', 'she'],
                        're': ['you', 'they', 'we']
                        }

THREE_LETTER_WORDS_CONTAINING_TWO_LETTER = {'beginning': ['any', 'and', 'too', 'now', 'not', 'one'],
                                            'ending': ['the', 'for', 'can', 'has', 'his', 'she', 'use', 'bus']}

THREE_LETTER_WORDS_AND_MASKS = {'abc':get_three_letter_words_from_masks('abc'),
                                'abb':get_three_letter_words_from_masks('abb'),
                                'aba':get_three_letter_words_from_masks('aba')}

TWO_LETTER_MASK = generate_mask_from_dict(COMMON_TWO_LETTER_WORDS)

#EXCEPTIONS
class double_value_error(Exception):
    '''
    raised during initialization of a MobileClient
    if a client with the specified serial number is not found
    '''
    pass

# wxqnwhrph ri dwawipw ja frownqy rp ij urlw. qjfwngilw ri qew aglw ja qyngiiy rp ij urnqsw. - ognny tjfdvgqwn