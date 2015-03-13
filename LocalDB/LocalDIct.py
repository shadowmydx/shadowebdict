# -*- coding:utf-8 -*-
__author__ = 'wmydx'

import sqlite3

class LocalDict:
    def __init__(self):
        self.con = None
        self.limit = 4
        self.setup_connect()

    def setup_connect(self):
        self.con = sqlite3.connect('./word.db')
        create_table = '''CREATE TABLE IF NOT EXISTS words
        (
            word text,
            explain text,
            net_explain text,
            sentence text,
            times int
        );
        '''
        self.con.execute(create_table)
        create_table = '''CREATE TABLE IF NOT EXISTS hard
        (
            word text,
            explain text,
            net_explain text,
            sentence text,
            times int
        );
        '''
        self.con.execute(create_table)
        self.con.text_factory = str

    def is_a_hard_word(self, diction):
        print diction['times'] == self.limit
        return diction['times'] == self.limit   # prevent mutiple insert, so use == instead of >=

    def update_word_times(self, diction):
        curs = self.con.cursor()
        update_sql = '''
            UPDATE words SET times=? WHERE word=?
        '''
        curs.execute(update_sql,(diction['times'], diction['word']))

    def get_hard_word(self):
        curs = self.con.cursor()
        select_sql = '''
            SELECT word FROM hard;
        '''
        curs.execute(select_sql)
        names = [d[0] for d in curs.description]
        rows = [dict(zip(names, row)) for row in curs.fetchall()]
        return rows

    def get_eng_word_from_db(self, word):
        curs = self.con.cursor()
        select_sql = '''
            SELECT * FROM words WHERE word=\'%s\';
        ''' % word
        curs.execute(select_sql)
        names = [d[0] for d in curs.description]
        rows = [dict(zip(names, row)) for row in curs.fetchall()]
        return rows

    def process_dict(self, diction):
        for key in diction.keys():
            if diction[key] == -1:
                diction[key] = ''
        return diction

    # before pass diction to this method, u need to add word and times in diction
    def insert_word_to_db(self, diction, table):
        diction = self.process_dict(diction)
        insert_sql = '''
            INSERT INTO %s (word,explain,net_explain,sentence,times) VALUES
            (?,?,?,?,?);
        ''' % table
        self.con.execute(insert_sql, (diction['word'], diction['explain'],
                                      diction['net_explain'], diction['sentence'], diction['times']))

    def turn_off_db(self):
        self.con.commit()
        self.con.close()


if __name__ == '__main__':
    db = LocalDict()
    db.setup_connect()
