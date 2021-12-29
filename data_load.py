from data.Standart import db_session

from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.items_and_criteria import ItemsAndCriteria
from rating import calculate_university_rating

db_session.global_init('db/database.db')

db_sess = db_session.create_session()

scientists = list(sorted([[i.name, i.id, float(db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.criteria_id == 300).filter(ItemsAndCriteria.item_id==i.id).first().value)]\
    for i in db_sess.query(Ukraine_Scientists).all()[:3000]], key=lambda x: x[2], reverse=True))
universities = []
map_uk = {}
for university in db_sess.query(Ukraine_Universities).all():
    rating = float(db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.criteria_id == 301).filter(ItemsAndCriteria.item_id==university.id).first().value)
    map_uk[university.region] = 0
    universities.append([university.univername, rating, university.id, university.region])
universities = sorted(universities, key=lambda x: x[1], reverse=True)


plus = 0
for i in range(200):
    if i <= 10:
        plus = 100
    elif i <= 20:
        plus = 90
    elif i <= 30:
        plus = 80
    elif i <= 40:
        plus = 70
    elif i <= 50:
        plus = 60
    else:
        plus = 10

    map_uk[universities[i][3]] += plus
map_uk['ua-kc'] -= 3000

articles_main_page = 0
for i in db_sess.query(Ukraine_Scientists):
    if i.google_scholar and i.google_scholar != '-':
        articles_main_page += 1
    if i.scopus and i.scopus != '-':
        articles_main_page += 1
    if i.publon and i.publon != '-':
        articles_main_page += 1

students_main_page = 0
for i in db_sess.query(Ukraine_Universities):
    if i.students_bak:
        students_main_page += i.students_bak
    if i.students_mag:
        students_main_page += i.students_mag
