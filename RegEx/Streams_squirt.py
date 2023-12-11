import os
import requests
from re import search
from re import findall as RegexFindall
from re import compile as Compile
from time import sleep
from random import uniform

url = ['https://chaturbate.com/', 'https://chaturbate.com/tag/dildo/f/', 'https://chaturbate.com/tag/squirt/f/', 'https://chaturbate.com/tag/hairy/f/', 'https://chaturbate.com/tag/bbw/f/']
link_name_filter = u'((?<=tag/)\w*)'
save_dir = '/home/joz/Videos/PlayList'
p = 1
html_tag = RegexFindall(link_name_filter, url[1])
html_tag = html_tag[0]
file_out = save_dir + '/' + html_tag + '_' + str(p) + '.m3u8'

# wrkdir = os.getcwd() + '/RegEx/'; ext = '.html'

def get_users(url, pages):
    page = 0; users = []; UserFilter = u'((?<=data-slug=")\w*)'
    while page < pages:
        page += 1
        for usr in RegexFindall(UserFilter, requests.get(url, params={'page': page}).text):
            users.append(usr)
        sleep(round(uniform(1.0, 2.0), 4))
    return users

def get_streams(url, users):
    unavailable_user = len(users)
    StreamFilter = '(https?://.*\.m3u8)'
    regex = Compile(r'(\\u[a-fA-F0-9]*)')
    pages = len(users) // 90; p = 1
    save_dir = '/home/joz/Videos/PlayList'
    file_out = save_dir + '/Streams_squirt_' + str(p) + '.m3u8'
    too_many_requests = '429'
    oke = '200'
    i = 0
    if os.path.exists(file_out):
        os.remove(file_out)
    with open(file_out, encoding='utf-8', mode='a') as Playlist:
        Playlist.write('#EXTM3U\n')
    for user in users:
        Seperator =  '=============================================================================== - ' + user + ' - ==============================================================================='
        user_page = url + user
        with requests.get(user_page) as r:
            page_content = str(r.content, 'UTF-8')
            status = r.status_code
            header = r.headers
        if str(status) == oke:
            strm_url = ""
            if RegexFindall(StreamFilter, str(page_content)): strm_url
                strm_url = RegexFindall(StreamFilter, str(page_content))
                strm_url = strm_url[0]

                while regex.search(strm_url):
                    ustr = regex.search(strm_url)
                    strm_url = strm_url.replace(ustr[0], make_uchr(ustr[0]))
                print(Seperator + '\nStream url:\t' + strm_url + '\nFile:\t\t' + file_out + '\nPlaylist count: ' + str(i) + '\nTotal users:\t' + str(unavailable_user))
                with open(file_out, encoding='utf-8', mode='a') as Playlist:
                    Playlist.write('#EXTINF:' + str(i) + ',' + user + '\n' + strm_url + '\n')
                    i += 1
                if i == 90:
                    with open(file_out, encoding='utf-8', mode='a') as Playlist:
                        Playlist.write('#EXTINF:' + str(i) + ',' + user + '\n' + strm_url + '\n')
                    i = 0; p += 1; file_out = save_dir + '/Streams_squirt_' + str(p) + '.m3u8'
                    if p <= pages:
                        if os.path.exists(file_out):
                            os.remove(file_out)
                        with open(file_out, encoding='utf-8', mode='a') as Playlist:
                            Playlist.write('#EXTM3U\n')
            else:
                unavailable_user -= 1
                continue
        elif str(status) != oke:
            if str(status) == too_many_requests:
                with open(os.getcwd() + '/page_content.txt', encoding='utf-8', mode='a') as file:
                    file.write(str(header))
                print('Status not oke:', status)
                sleep(round(uniform(15.0, 16.0), 4))
                break
            else:
                unavailable_user -= 1
                print('\n\nRESPONSE ERROR:\t' + str(status) + 'User name:\t\t' + user + '\n')
        sleep(round(uniform(15.0, 16.0), 2))
    print(Seperator + '\n\nAll done!\n')
    Playlist.close()
    return

def make_uchr(code: str):
  return chr(int(code.lstrip('\\u').zfill(8), 16))

for lnk in url:
    if lnk == url[0]:
        n = 0
        continue
    n += 1, get_streams(url[0], get_users(lnk, 2))
    file_out = save_dir + '/' + RegexFindall(link_name_filter, lnk) + '_' + str(p) + '.m3u8'