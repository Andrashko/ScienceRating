from bs4 import BeautifulSoup as BS
import requests


res = requests.get('https://scholar.google.com.ua/citations?user=F2H2VvwAAAAJ')
html = BS(res.content, 'html.parser')

for i in html.find_all('span', class_='gsc_g_t'):
    print(i.text)

for i in html.find_all('span', class_='gsc_g_al'):
    print(i.text)