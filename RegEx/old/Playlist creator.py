import os
import requests
from re import findall as RegexFindall
from re import compile as Compile
from time import sleep
from random import uniform

UserFilter = '((?<=data-slug=")\w*)'
UserFilter = '((?<=href=")\w*)'
StreamFilter = '(https?://.*\.m3u8)' #'(https?://edge+[0-9]*\.stream\.highwebmedia\.com\/live.*\.m3u8)'
url = 'https://chaturbate.com/female-cams/'
url_root = 'https://chaturbate.com/'
wrkdir = '/home/joz/Workspace/RegEx/'
ext = '.html'

def get_users(url, pages):
    page = 0; users = []

    while page < pages:
        page += 1

        for usr in RegexFindall('((?<=data-slug=")\w*)', requests.get(url, params={'page': page}).text):
            users.append(usr)

        sleep(round(uniform(5.0, 6.0), 4))

    return users

def get_streams(url, users):
    strm_list = []
    unavailable_user = i = 0
    regex = Compile(r"(\\u[a-fA-F0-9]*)")

    if os.path.exists("Streams_.m3u8"):
        os.remove("Streams_.m3u8")
    f = open("Streams_.m3u8", encoding='utf-8', mode='w'); f.write("#EXTM3U\n")

    for user in users:
        user_page = url + user
        fl_out = wrkdir + user + ext

        r = requests.get(user_page); page_content = str(r.content, 'UTF-8'); r.close()
        strm_url = RegexFindall(StreamFilter, str(page_content))

        if strm_url:
            strm_url = strm_url[0]
            
            while regex.search(strm_url):
                ustr = regex.search(strm_url)
                strm_url = strm_url.replace(ustr[0], make_uchr(ustr[0]))

            f.write("#EXTINF:" + str(i) + "," + user + "\n" + strm_url + "\n")
            strm_list.append(strm_url)
            print(str(i) + ":", strm_url)
        else:                                                                                   # user not available. Increment e by 1
            unavailable_user += 1
            continue

        sleep(round(uniform(8.0, 10.0), 4)); i += 1

        if i == len(users) - unavailable_user:
            print("\nAll done!")
            break
 
    f.close()
    return strm_list

def make_uchr(code: str):
  return chr(int(code.lstrip("\\u").zfill(8), 16))

users = get_users(url, 2)
get_streams(url_root, users)
exit
