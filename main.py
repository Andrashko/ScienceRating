from flask import Flask, render_template
import requests
import json
from bs4 import BeautifulSoup as BS
from sqlalchemy import or_

from data.Standart import db_session
from data.database.kaz_universities import Kaz_Universities
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.criteria import Criterias

db_session.global_init("db/database.db")

app = Flask(__name__)


@app.route('/')
def universities_rating():
    db_sess = db_session.create_session()

    scientists = []
    for i in range(1, 33):
        get = db_sess.query(Ukraine_Scientists).get(i)

        if get.google_scholar != '-' and get.publon != '-' and get.scopus != '-':
            scientists.append([get.name.split(), i])

    rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.criteria_id == 7)
    universities = []
    for i in rating:
        university = db_sess.query(Ukraine_Universities).get(i.item_id)

        try:
            if len(university.univername) > 65:
                universities.append([university.univername[:65].strip() + '...',
                                     int(i.value) * 100 / len(list(university.scientists)), i.item_id])
            else:
                universities.append([university.univername,
                                     int(i.value) * 100 / len(list(university.scientists)), i.item_id])
        except ZeroDivisionError:
            pass
    universities = sorted(universities, key=lambda x: x[1], reverse=True)[:10]

    return render_template('universities_rating.html', color_page_one='#F63E3E', univers_rating=universities,
                           scientists=scientists)


@app.route('/universities')
def all_universities():
    db_sess = db_session.create_session()

    universities = sorted([[i.univername, i.id] for i in db_sess.query(Ukraine_Universities)], key=lambda x: x[0])

    return render_template('universities.html', color_page_one='#F63E3E', univers=universities)


@app.route('/university_info/<int:university_id>')
def university_info(university_id):
    db_sess = db_session.create_session()
    university = db_sess.query(Ukraine_Universities).get(university_id)
    scientists = len(list(university.scientists))

    faculty_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'faculty').filter(
        ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == university_id)

    department_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'department').filter(
        ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == university_id)

    faculties = []
    if faculty_rating:
        for i in faculty_rating:
            if (' - без факультету' not in db_sess.query(UkraineFaculties).get(i.item_id).faculty_name) and \
                    (not db_sess.query(UkraineFaculties).get(i.item_id).faculty_name.isdigit()):
                try:
                    faculties.append([db_sess.query(UkraineFaculties).get(i.item_id).faculty_name, i.item_id,
                                      int(i.value) * 100 / scientists])
                except ZeroDivisionError:
                    faculties.append([' ', -1])
        faculties = sorted(faculties, key=lambda x: x[2], reverse=True)

    departments = []
    if department_rating:
        for i in department_rating:
            try:
                departments.append([db_sess.query(UkraineDepartments).get(i.item_id).department_name, i.item_id,
                                    int(i.value) * 100 / scientists])
            except ZeroDivisionError:
                departments.append([' ', -1])
        departments = sorted(departments, key=lambda x: x[2], reverse=True)

    facult_depart = []
    facult_empty = True
    depart_empty = True
    for i in range(len(departments)):
        if not departments and not faculties:
            facult_depart = []
            break

        try:
            facult_depart.append([faculties[i][0], faculties[i][1]])
            facult_empty = False
        except IndexError:
            facult_depart.append(['', -1])

        try:
            facult_depart[i].append([departments[i][0], departments[i][1]])
            depart_empty = False
        except IndexError:
            facult_depart[i].append(' ')

    return render_template('university_info.html', facult_depart=facult_depart, univer=university,
                           facult_empty=facult_empty, depart_empty=depart_empty)


@app.route('/faculty_info/<int:faculty_id>')
def faculty_info(faculty_id):
    db_sess = db_session.create_session()
    faculty = db_sess.query(UkraineFaculties).get(faculty_id)
    return render_template('faculty_info.html', faculty=faculty)


@app.route('/department_info/<int:depart_id>')
def department_info(depart_id):
    db_sess = db_session.create_session()
    depart = db_sess.query(UkraineDepartments).get(depart_id)
    univer_id = db_sess.query(UkraineFaculties).get(depart.faculty_id).univer_id
    return render_template('department_info.html', depart=depart, univer_id=univer_id)


@app.route('/university_info_rating/<int:university_id>')
def university_info_rating(university_id):
    db_sess = db_session.create_session()

    university = db_sess.query(Ukraine_Universities).get(university_id)
    scientists = len(list(university.scientists))
    criterias = db_sess.query(Criterias).filter(or_(Criterias.number == '2.1.1.', Criterias.number == '2.1.2.',
                                                    Criterias.number == '2.1.3.', Criterias.number == '2.2.',
                                                    Criterias.number == '2.3.'))
    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == university.id)

    criters_values = []
    index = 0
    for i in range(8, 13):
        criters_values.append([criterias[index].name, values.filter(ItemsAndCriteria.criteria_id == i).first()])
        index += 1

    for i in range(1, 8):
        criters_values.append([db_sess.query(Criterias).get(i).name, 0])
    for i in range(14, 54):
        criters_values.append([db_sess.query(Criterias).get(i).name, 0])

    return render_template('university_info_rating.html', univer=university, criters_values=criters_values,
                           rating_value=int(
                               int(values.filter(ItemsAndCriteria.criteria_id == 7).first().value) * 100 / scientists))


@app.route('/scientist_info/<int:scientist_id>')
def scientist_info(scientist_id):
    db_sess = db_session.create_session()

    scientist = db_sess.query(Ukraine_Scientists).get(scientist_id)
    info = [scientist.name.split()]

    if scientist.google_scholar and (scientist.google_scholar != '-'):
        info.append(scientist.google_scholar)
    else:
        info.append(False)

    if scientist.scopus and (scientist.scopus != '-'):
        info.append(scientist.scopus)
    else:
        info.append(False)

    if scientist.publon and (scientist.publon != '-'):
        info.append(scientist.publon)
    else:
        info.append(False)

    info.append(db_sess.query(Ukraine_Universities).get(scientist.univer_id).univername)
    if scientist.degree and ('немає' not in scientist.degree):
        info.append(scientist.degree)
    else:
        info.append(False)
    if scientist.science:
        info.append(scientist.science)
    else:
        info.append(False)

    if scientist.google_scholar:
        res = requests.get(scientist.google_scholar)
        html = BS(res.content, 'html.parser')
    SIZE = 60

    google_scholar = []
    if scientist.google_scholar and (scientist.google_scholar != '-'):
        for i in html.find_all('tr', class_='gsc_a_tr'):
            try:
                a_one = i.find_all('a', class_='gsc_a_at')[0].text[:SIZE].strip() + '...'
            except IndexError:
                a_one = ''

            try:
                a_one_href = 'https://scholar.google.com.ua' + i.find_all('a', class_='gsc_a_at')[0].get('href')
            except IndexError:
                a_one_href = ''

            try:
                div_one = i.find_all('div')[0].text
            except IndexError:
                div_one = ''

            try:
                div_two = i.find_all('div')[1].text[:SIZE].strip() + '...'
            except IndexError:
                div_two = ''

            try:
                a_two = i.find_all('a', class_='gsc_a_ac gs_ibl')[0].text
            except IndexError:
                a_two = ''

            try:
                a_two_href = i.find_all('a', class_='gsc_a_ac gs_ibl')[0].get('href')
            except IndexError:
                a_two_href = ''

            try:
                span = i.find_all('span', class_='gsc_a_h gsc_a_hc gs_ibl')[0].text
            except IndexError:
                span = ''
            google_scholar.append([[a_one, a_one_href], div_one, div_two, [a_two, a_two_href], span])

        photo = True
        if 'https' in html.find_all('img', id='gsc_prf_pup-img')[0].get('src'):
            info.append(html.find_all('img', id='gsc_prf_pup-img')[0].get('src'))
        else:
            photo = False
    else:
        google_scholar = False
        photo = False

    if scientist.publon:
        url = f'https://publons.com/api/v2/academic/publication/' \
              f'?academic={scientist.publon.split("/")[len(scientist.publon.split("/")) - 1]}'
        headers = {"Authorization": "Token 01aa647bdc5658a42d90d629265b6d6443891e44",
                   "Content-Type": "application/json"}
        res = requests.get(url, headers=headers)
        articles = json.loads(res.content)
    SIZE_title = 60
    SIZE_journal = 40

    try:
        publon = []
        if scientist.publon and (scientist.publon != '-'):
            for i in articles['results']:
                title = i['publication']['title'][:SIZE_title].strip() + '...'
                journal_name = i['journal']['name'][:SIZE_journal].strip() + '...'

                publon.append([i['publication']['ids']['url'], title,
                               i['publication']['date_published'].replace('-', '.'),
                               i['journal']['ids']['url'], journal_name])
    except KeyError:
        publon = 'no access'

    return render_template('scientist_info.html', scientist=info, google_articles=google_scholar,
                           publon_articles=publon, photo=photo, univer_id=scientist.univer_id,
                           depart_id=scientist.department_id)


if __name__ == '__main__':
    app.run()
