from data.Standart import db_session
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.criteria import Criterias


"""
Функция находит рейтинг университета 
"""


def calculate_university_rating(univer):
    # db_sess = db_session.create_session()
    # rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
    #     ItemsAndCriteria.item_id == univer.id)
    # try:
    #     rating_value = 0
    #     for j in rating:
    #         if j.criteria_id == 7 and univer.scientists:
    #             rating_value += int(int(j.value) * 100 /
    #                                 len(univer.scientists))
    #         elif db_sess.query(Criterias).get(j.criteria_id).number in [str(_) for _ in range(1, 16)]:
    #             rating_value += int(j.value)
    #         # QS
    #         if j.criteria_id == 199:
    #             rating_value += 1000 * int(j.value)
    #         if j.criteria_id == 200:
    #             rating_value += 2000 * int(j.value)

    #     rating_value += len(univer.projects) * 100

    #     return rating_value
    # except ZeroDivisionError:
    #     return 0
    # except AttributeError:
    #     return 0
    return calculate_students_rating(univer) + calculate_project_rating(univer) + calculate_international_rating(univer) + calculate_national_rating (
        univer) + calculate_employee_rating(univer, "university") + calculate_publication_rating(univer, "university")

def calculate_faculty_rating(faculty):
    return calculate_employee_rating(faculty, "faculty") + calculate_publication_rating(faculty, "faculty")

def calculate_department_rating(department):
    return calculate_employee_rating(department, "department") + calculate_publication_rating(department, "department")


def get_students(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in range(2, 4):
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value)])
    return criters_values


def get_scientists(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in [8, 9, 10, 11, 12]:
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value)])
    return criters_values


def get_articles(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in [23, 34, 31]:
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value)])
    return criters_values


def get_projects(univer_id):
    db_sess = db_session.create_session()

    return db_sess.query(Ukraine_Universities).get(univer_id).projects


def calculate_students_rating(univer):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(ItemsAndCriteria.item_id == univer.id)
        value = int(ic.filter(ItemsAndCriteria.criteria_id == 1).first().value)
        return value
    except:
        return 0

def calculate_project_rating(univer):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(ItemsAndCriteria.item_id == univer.id)
        value = 100*int(ic.filter(ItemsAndCriteria.criteria_id == 44).first().value)
        return value
    except:
        return 0

def calculate_international_rating(univer):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(ItemsAndCriteria.item_id == univer.id)
        value = 2000*float(ic.filter(ItemsAndCriteria.criteria_id == 199).first().value) #QS
        return value
    except:
        return 0

def calculate_national_rating(univer):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(ItemsAndCriteria.item_id == univer.id)
        value = 1000*float(ic.filter(ItemsAndCriteria.criteria_id == 200).first().value) #top200
        return value
    except:
        return 0


def calculate_employee_rating(item, type):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == type).filter(ItemsAndCriteria.item_id == item.id)
        value = int(ic.filter(ItemsAndCriteria.criteria_id == 11).first().value)+2*int( #без званий
        ic.filter(ItemsAndCriteria.criteria_id == 9).first().value)+4*int( # кандидатов
        ic.filter(ItemsAndCriteria.criteria_id == 10).first().value) # докторов
        return value
    except:
        return 0

def calculate_publication_rating(item, type):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == type).filter(ItemsAndCriteria.item_id == item.id)
        value = int(ic.filter(ItemsAndCriteria.criteria_id == 35).first().value)+5*int( #фаховых
        ic.filter(ItemsAndCriteria.criteria_id == 23).first().value)+5*int( #scopus
        ic.filter(ItemsAndCriteria.criteria_id == 17).first().value) + 0.1 * int(#wos
        ic.filter(ItemsAndCriteria.criteria_id == 33).first().value)+ 0.1 * int(#scopus цитирование
        ic.filter(ItemsAndCriteria.criteria_id == 32).first().value)#wos цитирование
        return value
    except:
        return 0

