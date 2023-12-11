import requests
import os

url = 'https://w3schools.com/python/demopage.asp'
gurl = 'https://chaturbate.com/marrygrayes/'
#use the 'headers' parameter to set the HTTP headers:
x = requests.get(gurl, headers = {"HTTP_HOST": "SomeHost"})

print(x.text)

if os.path.exists("RequestText.txt"):
  os.remove("RequestText.txt")

f = open("RequestText.txt", "w")
f.write(x.text)
f.close()

#the 'demopage.asp' prints all HTTP Headers