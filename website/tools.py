import re
import codecs
from bs4 import BeautifulSoup as bs

def find_all_css_lines_in_file(filename):
    with open("./templates/{}".format(filename),'r') as f:
        soup = bs(f.read(),'lxml')
    print(soup.prettify())
    print(soup.find_all('link'))

find_all_css_lines_in_file('index.html')
