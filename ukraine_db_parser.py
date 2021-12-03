import requests
from bs4 import BeautifulSoup as BS

from data.Standart import db_session
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.ukraine_universities import Ukraine_Universities


db_session.global_init("db/database.db")

db_sess = db_session.create_session()
scientists_site = []
scientists_db = []


# Всего страниц в БД учёных: 2769
def parse_db(start, end):
    global scientists_site

    for i in range(start, end + 1):
        try:
            req = requests.get(
                'http://www.nbuviap.gov.ua/bpnu/index.php?familie=&ustanova=0&gorod=0&vidomstvo=%C2%F1%B3&napryam=0'
                f'&napryam_google=0&hirsh_lt=&order=Google&page={i}')
            html = BS(req.content, 'html.parser')
            tables = html.find_all('table')[4]
            tr3 = tables.find_all('tr')[2]
            links = tr3.find_all('a')
            all_info = []
            appnd = []

            links = [i['href'].strip() for i in links]

            for j in tr3:
                for text in j.stripped_strings:
                    appnd.append(text)

            while appnd:
                all_info.append(appnd[:8])
                del appnd[:8]

            for j in range(len(all_info)):
                del all_info[j][6]
                del all_info[j][0]

            for j in range(len(all_info)):
                for jj in range(len(all_info[j])):
                    if 0 < jj < 4:
                        if all_info[j][jj] != '-':
                            all_info[j][jj] = links.pop(0)

            scientists_site += [j for j in all_info]
            print(i, 'Page')
        except IndexError:
            return [i, end]
    return 'success'


start, end = int(input('Enter number of start page: ')), int(input('Enter number of end page: '))
while True:
    res = parse_db(start, end)
    if res == 'success':
        print('Parse success')
        break
    else:
        start, end = res[0], res[1]
        print('Page is empty, retrying...')

if input('Commit changes? [y/n]: ').lower() == 'y':
    for i in scientists_site:
        if not db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i[5]).first():
            univer = Ukraine_Universities(univername=i[5])
            db_sess.add(univer)
            db_sess.commit()

        univer = db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i[5]).first()
        scientist = Ukraine_Scientists(name=i[0], google_scholar=i[1], scopus=i[2], publon=i[3],
                                       science=i[4], univer=univer)
        db_sess.add(scientist)
        db_sess.commit()
    print('commit success')

input('\nPress Enter to continue ')
