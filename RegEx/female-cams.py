import os
import requests
from re import search
from re import findall as RegexFindall
from re import compile as Compile
from time import sleep
from random import uniform

url = ['https://chaturbate.com/', 'https://chaturbate.com/female-cams/', 'https://chaturbate.com/tag/dildo/f/', 'https://chaturbate.com/tag/squirt/f/', 'https://chaturbate.com/tag/hairy/f/']
wrkdir = os.getcwd() + '/RegEx/'; ext = '.html'

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
    save_dir = '/home/joz/Videos/PlayList'
    pages = len(users) // 90; p = 1
    too_many_requests = '429'
    oke = '200'
    i = 0
    if os.path.exists(save_dir + '/Streams_Female_' + str(p) + '.m3u8'):
        os.remove(save_dir + '/Streams_Female_' + str(p) + '.m3u8')
    with open(save_dir + '/Streams_Female_' + str(p) + '.m3u8', encoding='utf-8', mode='a') as Playlist:
        Playlist.write('#EXTM3U\n')
    for user in users:
        Seperator =  '=============================================================================== - ' + user + ' - ==============================================================================='
        user_page = url + user
        # fl_out = wrkdir + user + ext
        with requests.get(user_page) as r:
            page_content = str(r.content, 'UTF-8')
            status = r.status_code
            header = r.headers
        if str(status) == oke:
            strm_url = RegexFindall(StreamFilter, str(page_content))
            if strm_url:
                strm_url = strm_url[0]
                while regex.search(strm_url):
                    ustr = regex.search(strm_url)
                    strm_url = strm_url.replace(ustr[0], make_uchr(ustr[0]))
                print(Seperator + '\nStream url:\t' + strm_url + '\nPlaylist count: ' + str(i) + '\nTotal users:\t' + str(unavailable_user))
                with open(save_dir + '/Streams_Female_' + str(p) + '.m3u8', encoding='utf-8', mode='a') as Playlist:
                    Playlist.write('#EXTINF:' + str(i) + ',' + user + '\n' + strm_url + '\n')
                    i += 1
                if i == 90:
                    p += 1; i = 0
                    if p <= pages:
                        Playlist.close()
                        if os.path.exists(save_dir + '/Streams_Female_' + str(p) + '.m3u8'):
                            os.remove(save_dir + '/Streams_Female_' + str(p) + '.m3u8')
                        with open(save_dir + '/Streams_Female_' + str(p) + '.m3u8', encoding='utf-8', mode='a') as Playlist:
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
    print(Seperator + '\n\nAll done!\nTotal number of links in the playlist:\t' + str(i) + '\nUnavailable users:\t\t\t' + str(unavailable_user))
    Playlist.close()
    return

def make_uchr(code: str):
  return chr(int(code.lstrip('\\u').zfill(8), 16))

# users = get_users(url[4], 2)
get_streams(url[0], get_users(url[1], 2))
