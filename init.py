# -*- coding:utf-8 -*-
__author__ = 'wmydx'

import os

comment = '# set web dictionary\n'
cmd = 'alias webdict=' + '\'python ' + os.getcwd() + '/main.py\''

f = open('/home/wmydx/.bashrc', 'a')
f.write(comment + cmd)
f.close()

