# -*- coding: utf-8 -*-
'''
Created on 06.11.2013

@author: status
'''
translit_dict = {'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'e',
            'ё': 'e',
            'ж': 'zh',
            'з': 'z',
            'и': 'i',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': '',
            'ф': 'f',
            'х': 'kh',
            'ц': 'tc',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ъ': '',
            'ы': 'y',
            'ь': '',
            'э': 'e',
            'ю': 'i',
            'я': 'ia',}

def get_lang_digest(digest):
        if digest >= 'a' and digest <= 'z':
            return 'EN'
        elif (digest > 'z' and digest <= 'я') or digest == 'ё':
            return 'RU'
        else:
            return None

def translit(word,*args, **kwargs):
    word = word.lower()
    new_word = ''
    flag_ru = False
    flag_en = False
    flag_none = False
    for digest in word:
        if get_lang_digest(digest) == 'RU':
            flag_ru = True
            digest = translit_dict[digest]
        elif get_lang_digest(digest) == 'EN':
            flag_en = True
        else:
            flag_none = True
            digest = ''
        new_word += digest
    return new_word

def translit_simple(word):
    word = word.lower()
    new_word = ''
    for digest in word:
        if digest in translit_dict:
            digest = translit_dict[digest]
        new_word += digest
    return new_word
