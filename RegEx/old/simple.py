from requests import get as HttpGet
from re import findall as RegexFindall


url = 'https://chaturbate.com/female-cams/'
headers = {'Content-Type': 'text/html',}
UserFilter = '((?<=data-slug=")\w*)'




u = RegexFindall(UserFilter, HttpGet(url, headers, timeout=1.000).text)
print(len(u))



'''
local_file = 'Streams1.html'

with open(local_file, 'w') as f:
    f.write(html)



htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)

t2 = round(perf_counter(), 4)
# n = round(uniform(1.0, 6.0), 4)

sleep("n" = round(uniform(1.0, 6.0), 4))

t3 = round(perf_counter(), 4)

print(n, "\n")
print(round(t3-t2, 4), "\n")

'''



