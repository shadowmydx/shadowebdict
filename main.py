# -*- coding:utf-8 -*-
__author__ = 'wmydx'

from LocalDB import LocalDIct
from WebDict import getResponse

def show_result(ans):
    names = ['word', 'explain', 'net_explain', 'sentence', 'times']
    for item in ans:
        for key in names:
            print key + ': \n' + str(item[key])
        if item['times'] > 1:
            print 'CAREFUL!! this is a hard word!!'

def show_hard_word(ans):
    for item in ans:
        print item['word'] + '\n'

def main():
    db = LocalDIct.LocalDict()
    response = getResponse.GetResponse()
    input_word = ''
    try:
        while True:
            input_word = raw_input("plz input words: ")
            if input_word == str(-1):
                break
            if input_word == '#':
                ans = db.get_hard_word()
                show_hard_word(ans)
            else:
                ans = db.get_eng_word_from_db(input_word)
                if not ans:
                    print 'here'
                    ans = response.get_dict_data(input_word)
                    for item in ans:
                        db.insert_word_to_db(item, 'words')
                else:
                    for item in ans:
                        item['times'] += 1
                        db.update_word_times(item)
                        if db.is_a_hard_word(item):
                            db.insert_word_to_db(item, 'hard')
                show_result(ans)
        db.turn_off_db()
        print 'END.'
    except:
        db.turn_off_db()

main()

