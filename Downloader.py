import os
import requests
import re
from time import sleep
from random import uniform

def num_users_to_go(value=0, decrement=0, str_out=''):
    for i in range(value):
        if i == 0:
            continue
        if decrement:
            print('{0}\r'.format(str_out + str(value - 1) + ' '), end='', flush=True)
            value = (value - 1)
        else:
            print ("\r" + str_out + "{}".format(i) + ' ', end="", flush=True)
        sleep(1.0)
    return

def get_users(url, pages):
    page = int()
    online_users = set()
    User_Filter = re.compile(u'((?<=data-slug=")\w*)')

    while page < pages:
        page += 1
        with requests.get(url, params={'page': page}) as r:
            [usr for usr in online_users.union((User_Filter.findall(r.text))) if usr not in online_users and not online_users.add('https://SomeSite.com/' + usr)]
            r.close()
        sleep(round(uniform(1.0, 2.0), 4))
    return list(online_users)

def get_streams(url, file_out, half_list=False):
    log_file = os.getcwd() + "/PlayListlog.txt"
    user_filter = re.compile(r'((?<=com/)\w*)')
    uChar_filter = re.compile(r'(\\u[a-fA-F0-9]*)')
    stream_filter = re.compile(r'(https?://.*\.m3u8)')
    
    if half_list == True:
        users_to_go = users_total = int(int(len(url)) / 2)
    else:
        users_to_go = users_total = int(len(url))

    current_users_in_list = 0
    too_many_requests = 429
    elapse_time = float()
    oke = 200
    
    save_file(file_out, '#EXTM3U', lnfeed=1, delete=1)

    for user_page in url:
        user = user_filter.search(user_page).group()
        next_request = int(round(uniform(10.2, 13.6), 2))
        Seperator = '============================================================================= - ' + user + ' - ============================================================================='

        with requests.get(user_page) as r:
            page_content = str(r.content, 'UTF-8')
            status = r.status_code
            header = r.headers
            r.close()

        if status == oke:
            strm_url = re.findall(stream_filter, str(page_content))

            if strm_url:
                current_users_in_list += 1
                users_to_go -= 1
                strm_url = strm_url[0]

                while uChar_filter.search(strm_url):
                    strm_url = strm_url.replace(uChar_filter.search(strm_url).group(), make_uchr(uChar_filter.search(strm_url).group()))

                if not users_to_go:
                    print("Finished!")
                else:
                    if users_total == current_users_in_list:
                        users_to_go = 0
                        print(Seperator + '\nFile out:   \t' + file_out + '\n\nCurrent users in list:\t' + str(current_users_in_list) +  '\nTotal users in list:\t' + str(users_total) + '\nTotal users to go:\t' + str(users_to_go) + '\n')
                        break

                    elapse_time += next_request

                    save_file(log_file, Seperator + '\nFile out:   \t' + file_out + '\nStream url: \t' + strm_url + '\n\nCurrent users in list:\t' + str(current_users_in_list) + '\nTotal users in list:\t' + str(users_total) + '\nTotal users to go:\t\t' + str(users_to_go) + "\nTime to next request:\t" + str(next_request) + '\nElapse time:\t\t\t' + str(round(elapse_time, 2)) + '\n')
                    save_file(file_out, '#EXTINF:' + str(current_users_in_list) + ',' + user + '\n' + strm_url + '\n')
                    
                    print(Seperator + '\nFile out:   \t' + file_out + '\n\nCurrent users in list:\t' + str(current_users_in_list) +  '\nTotal users in list:\t' + str(users_total) + '\nTotal users to go:\t' + str(users_to_go) + '\n')
                
            else:
                users_total -= 1
                continue
        else:
            users_total -= 1

            if status == too_many_requests:
                next_request = header['Retry-After']
                save_file(os.getcwd() + '/page_content.json', str(header), 0, 0)

                print('HTTP Error:\t'+str(status) + ' - Too many requests to the server.\nSeconds to wait before retry:\t' + str(next_request) + '\nelapse_time:\t\t' + str(elapse_time) + '\n')

            else:
                save_file(log_file, Seperator + '\n\nRESPONSE ERROR:\t' + str(status) + '\nUser name:\t\t' + user + '\n\n')

                print(Seperator + '\n\nRESPONSE ERROR:\t' + str(status) + '\nUser name:\t\t' + user + '\n\n')
        
        num_users_to_go(value=int(next_request), decrement=1, str_out='Next request in sec:\t')
        #print(next_request, end='\r', flush=True)

    save_file(log_file, '\n\n\nFinished writing playlist:\t' + file_out + "\nElapse time:\t\t\t\t" + str(round(elapse_time, 2)) + "\n")
    print('\n\n\nFinished writing playlist:\t' + file_out + "\nElapse time:\t\t\t" + str(round(elapse_time, 2)) + "\n")
    return

def make_uchr(code: str):
    return chr(int(code.lstrip('\\u').zfill(8), 16))

def save_file(file, txt, lnfeed=0, delete=0):
    if delete:
        if os.path.exists(file):
            os.remove(file)
    with open(file, encoding='utf-8', mode='a') as f:
        if not lnfeed:
            f.write(txt)
        else:
            f.write(txt + '\n')
        f.close()
    return

tags_url = []
save_dir = '/home/jos/Videos/PlayList'
tags_name_filter = re.compile(r'(?<=data-floatingnav>#)\w*')
tags_Filter = re.compile(r'((?<=tag/)\w*)')
root_urls = ['https://SomeSite.com/', 'https://SomeSite.com/tag/', 'https://SomeSite.com/tags/f/']
url = [root_urls[0]]

# get a collection of all the taggs. Store the url for each tag in list tags_url.
with requests.get(root_urls[2]) as r:
    for tag in tags_name_filter.findall(str(r.content, 'UTF-8')):
        tags_url.append(root_urls[1] + tag + '/f/')

tags_get = ["nasty"]  # tags_get = ["A", "B", "C"]

# Itirate through all urls in tags_url.
for page_link in tags_url:
    # start to compare each tag name in t with current url.
    for tag in tags_get:
        # If the tag name in t is the same as the one in current url.
        if tag == tags_Filter.search(page_link).group():
            # Then append it to list url[].
            url.append(page_link)
            print("\n______________________________________________________________________\n\n" + page_link)

for url_tagged in url:
    if url_tagged == root_urls[0]:
        if os.path.exists(os.getcwd() + "/PlayListlog.txt"):
            os.remove(os.getcwd() + "/PlayListlog.txt")
        continue
    get_streams(get_users(url_tagged, pages=1), save_dir + '/' + tags_Filter.search(url_tagged).group() + '.m3u8', half_list=True)
exit
