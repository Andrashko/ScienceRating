from data.Standart import db_session
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.items_and_criteria import ItemsAndCriteria
from json import dump, load 

db_session.global_init('db/database.db')

db_sess = db_session.create_session()

for d in db_sess.query(UkraineDepartments):
    for d2 in db_sess.query(UkraineDepartments).filter(UkraineDepartments.department_name == d.department_name).filter(UkraineDepartments.id != d.id):
        if db_sess.query(UkraineFaculties).get(d.faculty_id).univer_id != db_sess.query(UkraineFaculties).get(d2.faculty_id).univer_id:
            continue
        for s in d2.scientists:
            s.department_id = d.id
        db_sess.delete(d2)
    db_sess.commit()