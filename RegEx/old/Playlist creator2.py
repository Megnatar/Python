import os
import requests
from re import search
from re import findall as RegexFindall
from re import compile as Compile
from time import sleep
from random import uniform

IndexFilter = u'((?<=href=")[0-9]+)'                            #   <tr><td valign="top">&nbsp;</td><td><a href="2000/">2000/</a> 
urls =   [  'https://server9.mangovideo.pw/contents/videos/', 
            'https://60.mangovideo.pw/contents/videos/', 
            'https://new.mangovideo.pw/contents/videos/', 
            'https://31.mangovideo.pw/contents/videos/', 
            'https://183.mangovideo.pw/contents/videos/', 
            'https://45.mangovideo.pw/contents/videos/', 
            'https://98.mangovideo.pw/contents/videos/', 
            'https://46.mangovideo.pw/contents/videos/', 
            'https://server2.mangovideo.pw/contents/videos/', 
            'https://server217.mangovideo.pw/contents/videos/', 
            'https://234.mangovideo.pw/contents/videos/', 
            'https://s10.mangovideo.pw/contents/videos/',
            'https://68.mangovideo.pw/contents/videos/']

r = requests.get(urls[0])
i = 0
l1 = []
l2 = []
c = RegexFindall(IndexFilter, r.text)
for lnk in c:
    l1.append(urls[0] + lnk)
r.close

r = requests.get(l1[0])
c2 = RegexFindall(IndexFilter, r.text)
for lnk in c2:
    l2.append(l1[0] + "/" + lnk)
r.close

if os.path.exists(os.getcwd() + "/RegEx/mangovideo.m3u8"):
    os.remove(os.getcwd() + "/RegEx/mangovideo.m3u8")
f = open(os.getcwd() + "/RegEx/mangovideo.m3u8", encoding='utf-8', mode='w'); f.write("#EXTM3U\n")

print(l2)
exit

# url1 = https://68.mangovideo.pw/contents/videos/; url2 = https://98.mangovideo.pw/contents/videos/; url3 = https://server2.mangovideo.pw/contents/videos/; url4 = https://60.mangovideo.pw/contents/videos/; url5 = https://new.mangovideo.pw/contents/videos/; url6 = https://31.mangovideo.pw/contents/videos/; url7 = https://183.mangovideo.pw/contents/videos/; url8 = https://45.mangovideo.pw/contents/videos/; url9 = https://46.mangovideo.pw/contents/videos/; url10 = https://server217.mangovideo.pw/contents/videos/; url11 = https://server9.mangovideo.pw/contents/videos/; url12 = https://234.mangovideo.pw/contents/videos/; url13 = https://s10.mangovideo.pw/contents/videos/