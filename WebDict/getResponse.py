# -*- coding:utf-8 -*-
__author__ = 'wmydx'

import urllib
import re
import urllib2
import time

class GetResponse:

    def __init__(self):
        self.url = 'http://www.iciba.com/'
        self.isEng = re.compile(r'(([a-zA-Z]*)(\s*))*$')
        self.group_pos = re.compile(r'<div class="group_pos">(.*?)</div>', re.DOTALL)
        self.net_paraphrase = re.compile(r'<div class="net_paraphrase">(.*?)</div>', re.DOTALL)
        self.sentence = re.compile(r'<dl class="vDef_list">(.*?)</dl>', re.DOTALL)

    def process_input(self, word):
        word = word.strip()
        word = word.replace(' ', '_')
        return word

    def get_data_from_web(self, word):
        headers = {'Referer': 'http://www.iciba.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
        request = urllib2.Request(self.url + word, headers=headers)
        while True:
            try:
                f = urllib2.urlopen(request).read()
                break
            except:
                pass
        return f

    def get_eng_from_chinese(self, word):
        word = self.process_input(word)
        word = urllib.quote(word)
        data = self.get_data_from_web(word)
        label_lst = re.compile(r'<span class="label_list">(.*?)</span>', re.DOTALL)
        label_itm = re.compile(r'<label>(?P<item>.*?)</a>(.*?)</label>', re.DOTALL)
        first = label_lst.search(data)
        data = data[first.start():first.end()]
        start_itm = 0
        res = []
        while 1:
            second = label_itm.search(data, start_itm)
            if not second:
                break
            word = self.get_sentence_from_dt(data[second.start('item'):second.end('item')])
            res.append(word)
            start_itm = second.end()
        return res

    def get_dict_data(self, word):
        englst = []
        res = []
        match = self.isEng.match(word)
        if not match:
            englst = self.get_eng_from_chinese(word)
        else:
            englst.append(word)
        for item in englst:
            word = self.process_input(item)
            data = self.get_data_from_web(word)
            if data.find('对不起，没有找到') != -1:
                res.append(-1)
            else:
                tmp_dict = self.analysis_eng_data(data)
                tmp_dict['word'] = word
                tmp_dict['times'] = 1
                res.append(tmp_dict)
        return res

    def analysis_eng_data(self, data):
        res = {}
        explain = self.group_pos.search(data)
        if explain:
            explain = data[explain.start():explain.end()]
            res['explain'] = self.generate_explain(explain)
        else:
            res['explain'] = -1
        net_explain = self.net_paraphrase.search(data)
        if net_explain:
            net_explain = data[net_explain.start():net_explain.end()]
            res['net_explain'] = self.generate_net_explain(net_explain)
        else:
            res['net_explain'] = -1
        sentence_start = 0
        sentence_end = len(data)
        sentence_lst = []
        while sentence_start < sentence_end:
            sentence = self.sentence.search(data, sentence_start)
            if sentence:
                sentence_str = data[sentence.start():sentence.end()]
            else:
                break
            sentence_lst.append(self.generate_sentence(sentence_str))
            sentence_start = sentence.end()
        res['sentence'] = "\n\n".join(sentence_lst)
        return res

    def generate_explain(self, target):
        start_word = 0
        end_word = len(target)
        meta_word = re.compile(r'<strong class="fl">(?P<meta_word>.*?)</strong>', re.DOTALL)
        label_lst = re.compile(r'<span class="label_list">(.*?)</span>', re.DOTALL)
        label_itm = re.compile(r'<label>(?P<item>.*?)</label>', re.DOTALL)
        res = ''
        while start_word < end_word:
            first = meta_word.search(target, start_word)
            if first:
                word_type = target[first.start('meta_word'):first.end('meta_word')]
            else:
                break
            res += word_type + ' '
            second = label_lst.search(target, first.end('meta_word'))
            start_label = second.start()
            end_label = second.end()
            while start_label < end_label:
                third = label_itm.search(target, start_label)
                if third:
                    res += target[third.start('item'):third.end('item')]
                    start_label = third.end()
                else:
                    break
            res += '\n'
            start_word = end_label
        return res



    def generate_net_explain(self, target):
        start_itm = 0
        end_itm = len(target)
        li_item = re.compile(r'<li>(?P<item>.*?)</li>', re.DOTALL)
        res = '网络释义： '
        while 1:
            first = li_item.search(target, start_itm)
            if first:
                res += target[first.start('item'):first.end('item')]
            else:
                break
            start_itm = first.end()
        return res

    def generate_sentence(self, target):
        res = ''
        english = re.compile(r'<dt>(?P<eng>.*?)</dt>', re.DOTALL)
        chinese = re.compile(r'<dd>(?P<chn>.*?)</dd>', re.DOTALL)
        first = english.search(target)
        second = chinese.search(target)
        res += self.get_sentence_from_dt(target[first.start('eng'):first.end('eng')]) + '\n'
        res += target[second.start('chn'):second.end('chn')]
        return res

    def get_sentence_from_dt(self, target):
        res = ''
        length = len(target)
        index = 0
        while index < length:
            if target[index] == '<':
                while target[index] != '>':
                    index += 1
            else:
                res += target[index]
            index += 1
        return res

if __name__ == '__main__':
    p = GetResponse()
    test = ['hello', 'computer', 'nothing', 'bad guy', 'someday']
    for item in test:
        res = p.get_dict_data(item)
        for key in res:
            for (k, v) in key.items():
                print "dict[%s]=" % k, v
            print
        time.sleep(3)




