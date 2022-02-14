# -*- coding: utf-8 -*-
'''
Created on 06.11.2013

@author: status
'''
translit_dict = {u'а': u'a',
            u'б': u'b',
            u'в': u'v',
            u'г': u'g',
            u'д': u'd',
            u'е': u'e',
            u'ё': u'e',
            u'ж': u'zh',
            u'з': u'z',
            u'и': u'i',
            u'й': u'i',
            u'к': u'k',
            u'л': u'l',
            u'м': u'm',
            u'н': u'n',
            u'о': u'o',
            u'п': u'p',
            u'р': u'r',
            u'с': u's',
            u'т': u't',
            u'у': u'u',
            u'ф': u'f',
            u'х': u'kh',
            u'ц': u'tc',
            u'ч': u'ch',
            u'ш': u'sh',
            u'щ': u'shch',
            u'ъ': u'',
            u'ы': u'y',
            u'ь': u'',
            u'э': u'e',
            u'ю': u'iu',
            u'я': u'ia',}

def get_lang_digest(digest):
        if digest >= u'a' and digest <= u'z':
            return 'EN'
        elif (digest > u'z' and digest <= u'я') or digest == u'ё':
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
    new_word = u''
    for digest in word:
        if digest in translit_dict:
            digest = translit_dict[digest]
        new_word += digest
    return new_word
