import json
from data.Standart import db_session

from data.database.ukraine_universities import Ukraine_Universities
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists

db_session.global_init("db/database.db")
db_sess = db_session.create_session()

with open('data.json', encoding='utf-8') as file:
    res = json.load(file)

# университеты
for i in res:
    if not db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i['name']).first():
        univer = Ukraine_Universities(univername=i['name'])
        db_sess.add(univer)
        db_sess.commit()

    univer = db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i['name']).first()

    # факультативы
    for j in i['faculties']:
        facult = UkraineFaculties(faculty_name=j['name'], univer=univer)
        db_sess.add(facult)
        db_sess.commit()

        facult = db_sess.query(UkraineFaculties).filter(UkraineFaculties.faculty_name == j['name']).filter(
            UkraineFaculties.univer_id == univer.id).first()

        # департаменты
        for l in j['departmets']:
            depart = UkraineDepartments(department_name=l['name'], faculty=facult)
            db_sess.add(depart)
            db_sess.commit()

            depart = db_sess.query(UkraineDepartments).filter(UkraineDepartments.department_name == l['name']).filter(
                UkraineDepartments.faculty_id == facult.id).first()

            for f in l['scientiests']:
                scientist_name = ' '.join(f['name'].split())
                scientist_db = db_sess.query(Ukraine_Scientists).filter(
                    Ukraine_Scientists.name == scientist_name).first()

                if scientist_db:
                    scientist_db.degree = f['degree']
                    scientist_db.title = f['title']
                    scientist_db.univer_id = univer.id
                    scientist_db.department = depart

                    db_sess.merge(scientist_db)
                    db_sess.commit()
                else:
                    scientist = Ukraine_Scientists(name=scientist_name, degree=f['degree'], title=f['title'],
                                                   department=depart, univer=univer)

                    db_sess.add(scientist)
                    db_sess.commit()
print('success')
