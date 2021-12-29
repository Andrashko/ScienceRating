from data.Standart import db_session
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.criteria import Criterias
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments


universities_rating_cache = {}
faculties_rating_cache = {}
departments_rating_cache = {}
scientists_rating_cache = {}

"""
Функция находит рейтинг университета 
"""




def get_students(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in range(2, 4):
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value), False])
    return criters_values


def get_scientists(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in [ 9, 10, 11]:
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value), False])
    return criters_values


def get_articles(univer_id):
    db_sess = db_session.create_session()

    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer_id)

    criters_values = []
    for i in [23, 33]:
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
            criters_values.append([criteria.name, int(value.value), False])
    return criters_values


def get_projects(univer_id):
    db_sess = db_session.create_session()

    return db_sess.query(Ukraine_Universities).get(univer_id).projects


def calculate_students_rating(univer):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(ItemsAndCriteria.item_id == univer.id)
        value = int(ic.filter(ItemsAndCriteria.criteria_id == 1).first().value)*0.1
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
        value = 0
        mag = ic.filter(ItemsAndCriteria.criteria_id == 11).first()
        if mag:
            value +=  int(mag.value)
        phd = ic.filter(ItemsAndCriteria.criteria_id == 9).first()
        if phd:
            value += 2*int( phd.value)
        doctor =   ic.filter(ItemsAndCriteria.criteria_id == 10).first()   
        if doctor:
            value += 4*int( doctor.value) # докторов
        return value
    except:
        return 0

def calculate_publication_rating(item, type):
    db_sess = db_session.create_session()
    try:
        ic = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == type).filter(ItemsAndCriteria.item_id == item.id)
        value = 0
        scopus = ic.filter(ItemsAndCriteria.criteria_id == 23).first()
        if scopus:
            value += int (scopus.value)
        scopus_cit = ic.filter(ItemsAndCriteria.criteria_id == 33).first()
        if scopus_cit:
            value += 0.1* int (scopus_cit.value)
        
        return value
    except:
        return 0

def calculate_university_rating(univer):
    if not universities_rating_cache.get (univer.id):
        universities_rating_cache[univer.id] = calculate_students_rating(univer) + calculate_project_rating(univer) + calculate_international_rating(univer) + calculate_national_rating (
        univer) + calculate_employee_rating(univer, "university") + calculate_publication_rating(univer, "university")
    return universities_rating_cache[univer.id]

def calculate_faculty_rating(faculty):
    if not faculties_rating_cache.get(faculty.id):
        faculties_rating_cache[faculty.id] = calculate_employee_rating(faculty, "faculty") + calculate_publication_rating(faculty, "faculty")
    return faculties_rating_cache[faculty.id]

def calculate_department_rating(department):
    if not departments_rating_cache.get(department.id):
        departments_rating_cache[department.id] = calculate_employee_rating(department, "department") + calculate_publication_rating(department, "department")
    return departments_rating_cache[department.id]

def calculate_scientist_rating(scientist):
    if not scientists_rating_cache.get(scientist.id):
        scientists_rating_cache[scientist.id] = calculate_publication_rating(scientist, "scientist")
    return scientists_rating_cache[scientist.id] 

# faculties = []
# departments = []
# db_session.global_init("db/database.db")
# db_sess = db_session.create_session()
# for fac in db_sess.query(UkraineFaculties).filter(UkraineFaculties.univer_id == 36).all():
#     if ' - без факультету' not in fac.faculty_name:
#         faculties.append([fac.faculty_name, fac.id, calculate_faculty_rating(fac)])
#         for dep in db_sess.query(UkraineDepartments).filter(UkraineDepartments.faculty_id == fac.id).all():
#             departments.append([dep.department_name, dep.id, calculate_department_rating(dep)])