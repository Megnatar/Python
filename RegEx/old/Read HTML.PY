import urllib3
import requests

from bs4 import BeautifulSoup

# Fetch the html file
r = requests.get('http://tutorialspoint.com/python/python_overview.htm')
html_doc = r.text
print(html_doc)
#response1 = requests.get('http://tutorialspoint.com/python/python_overview.htm')
#html_doc1 = response1.text()

# Parse the html file
#soup = BeautifulSoup(html_doc, 'html.parser')

# Format the parsed html file
#strhtm = soup.prettify()

# Print the first few characters
#print(strhtm[:225])