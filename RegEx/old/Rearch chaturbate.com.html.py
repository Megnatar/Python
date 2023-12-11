import requests
import os
import json
from sys import getsizeof
from re import findall
from time import sleep
from time import perf_counter
from random import uniform
from urllib.request import urlopen
from lxml import etree


i = 0
pages = 1
StreamFilter = "(https?://edge+[0-9]*\.stream\.highwebmedia\.com\/live.*\.m3u8)"
UserFilter = "(?<=stopStreaming\(')(\w*)"
UserFilter1 = '(?<=data-room=.*").*\w'
UserFilter2 = '((?<=data-slug=")+\w*)'
UserFilter3 = '((?<=data-slug=")\w*)'
RequestClass = "<class 'requests.models.Response'>"

index = 1
xpath = '/html/body/div[2]/div[2]/div[5]/ul[1]/li[index]/a/img'   # /html/body/div[2]/div[2]/div[5]/ul[1]/li[90]/a/img


def get_users(url, parm):
  r = requests.get(url, params=parm)
  html = r.text
  r.close()
  sleep(round(uniform(1.0, 3.0), 4))
  return RegexFindall('((?<=data-slug=")\w*)', html)

def get_streams(url, users):
  strm_list = []
  unavailable_user = i = 0

  if os.path.exists("Streams.m3u8"):
    os.remove("Streams.m3u8")
  f = open("Streams.m3u8", encoding='utf-8', mode='w')
  f.write("#EXTM3U\n")

  for user in users:
    UserPage = page_content = StreamLink = r = strm_url = ""                                # reset variables
    StreamFilter = "(https?://edge+[0-9]*\.stream\.highwebmedia\.com\/live.*\.m3u8)"
    UserPage = url + user                                                                   # create link to user page
    
    r = requests.get(UserPage)                                                              # new request for the specific page
    page_content = r.content                                                                # store page data in page_content
    r.close()

    sleep(round(uniform(5.0, 7.0), 4))
    strm_url = RegexFindall(StreamFilter, str(page_content)); strm_url = strm_url[0]
    
    if strm_url:
      regex = re.compile(r"(\\u[a-fA-F0-9]*)")

      while regex.search(strm_url):
        ustr = regex.search(strm_url).groups()
        strm_url = strm_url.replace(ustr[0], make_uchr(ustr[0]))

      f.write("#EXTINF:" + str(i) + "," + user + "\n" + strm_url + "\n")
      strm_list.append(strm_url)
      print(str(i) + ":", strm_url)
    else:                                                                                   # user not available. Increment e by 1
      unavailable_user += 1
      continue

    i += 1
    if i == 1: # len(users) - unavailable_user:                                                  #  
      print("\nAll done!")
      break

  f.close()
  return strm_list

def make_uchr(code: str):
  return chr(int(code.lstrip("\\u").zfill(8), 16))

users = get_users(url0, headers)
get_streams(url, users)

exit
