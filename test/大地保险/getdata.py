#-*- coding:utf-8 -*-
import re
import requests

url = 'http://www.95590.cn//ebiz/jcaptcha?temp=jfxjt02r'


for i in range(1,50):
    print(i)
    try:
        pic= requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print('【错误】当前图片无法下载')
        continue
    string = '/Users/diamond/PycharmProjects/bishe/test/大地保险/train/'+str(i) + '.jpg'
    fp = open(string,'wb')
    fp.write(pic.content)
    fp.close()
    i += 1