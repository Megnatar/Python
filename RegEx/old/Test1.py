from re import findall as RegexFindall
from re import match as RegexMatch
from re import sub as RegexSub
import re
import requests
import os
import unicodedata as unc
import encodings
import codecs 
from time import sleep
from time import perf_counter
from random import uniform

# openfile = '/home/joz/Workspace/' file_content

i = 0; UserFilter = '((?<=data-slug=")\w*)'; StreamFilter = '(https?://edge+[0-9]*\.stream\.highwebmedia\.com\/live.*\.m3u8)'
pages = 1; query = {'page': pages}; headers = {'Content-Type': 'text/html',}; url = 'https://chaturbate.com/female-cams/'; url_root = 'https://chaturbate.com/'
wrkdir = '/home/joz/Workspace/RegEx/'; ext = '.html'


def get_users(url, parm):
  r = requests.get(url, params=parm)
  html = r.text
  r.close()
  sleep(round(uniform(1.0, 3.0), 4))
  return RegexFindall('((?<=data-slug=")\w*)', html)

def make_uchr(code: str):
    return chr(int(code.lstrip("\\u").zfill(8), 16))

# online_users = get_users(url, headers)

for user in get_users(url, query):
    user_page = url_root + user
    fl_out = wrkdir + user + ext

    r = requests.get(user_page)
    page_content = str(r.content, 'UTF-8')
    
    strm_url = RegexFindall(StreamFilter, str(page_content)); strm_url = strm_url[0]
    regex = re.compile(r"(\\u[a-fA-F0-9]*)")

    while regex.search(strm_url):
      ustr = regex.search(strm_url)
      strm_url = strm_url.replace(ustr[0], make_uchr(ustr[0]))
    
    print(strm_url)
    break


    if user == 0:
        break
exit