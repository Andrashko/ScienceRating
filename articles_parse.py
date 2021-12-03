import requests
import json
from bs4 import BeautifulSoup as BS

url = 'https://publons.com/api/v2/academic/publication/?academic=2007549'
headers = {"Authorization": "Token 01aa647bdc5658a42d90d629265b6d6443891e44", "Content-Type": "application/json"}
res = requests.get(url, headers=headers)
articles = json.loads(res.content)
for i in articles['results']:
    print(f'{i["publication"]["title"]}')
    print(f'Опубликовано: {i["publication"]["date_published"].replace("-", ".")} в {i["journal"]["name"]}\n')
