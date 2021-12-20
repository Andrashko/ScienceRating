import json
from data.Standart import db_session

from data.database.ukraine_universities import Ukraine_Universities
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.criteria import Criterias

db_session.global_init("db/database.db")
db_sess = db_session.create_session()

with open('db/data.json', encoding='utf-8') as file:
    res = json.load(file)

# университеты
for i in res:
    if not db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i['name']).first():
        univer = Ukraine_Universities(univername=i['name'])
        db_sess.add(univer)
        db_sess.commit()

    univer = db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.univername == i['name']).first()

    criteria21 = db_sess.query(Criterias).filter(Criterias.number == '2.1.').first()
    criteria211 = db_sess.query(Criterias).filter(Criterias.number == '2.1.1.').first()
    criteria212 = db_sess.query(Criterias).filter(Criterias.number == '2.1.2.').first()
    criteria213 = db_sess.query(Criterias).filter(Criterias.number == '2.1.3.').first()
    criteria22 = db_sess.query(Criterias).filter(Criterias.number == '2.2.').first()
    criteria23 = db_sess.query(Criterias).filter(Criterias.number == '2.3.').first()

    # критерии для университета
    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria21, item_type='university',
                                   country='ukraine', value=i['u21'])
    db_sess.add(item_criter)
    db_sess.commit()

    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria211, item_type='university',
                                   country='ukraine', value=i['u211'])
    db_sess.add(item_criter)
    db_sess.commit()

    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria212, item_type='university',
                                   country='ukraine', value=i['u212'])
    db_sess.add(item_criter)
    db_sess.commit()

    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria213, item_type='university',
                                   country='ukraine', value=i['u213'])
    db_sess.add(item_criter)
    db_sess.commit()

    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria22, item_type='university',
                                   country='ukraine', value=i['u22'])
    db_sess.add(item_criter)
    db_sess.commit()

    item_criter = ItemsAndCriteria(item_id=univer.id, criteria=criteria23, item_type='university',
                                   country='ukraine', value=i['u23'])
    db_sess.add(item_criter)
    db_sess.commit()

    # факультативы
    for j in i['faculties']:
        facult = UkraineFaculties(faculty_name=j['name'], univer=univer)
        db_sess.add(facult)
        db_sess.commit()

        facult = db_sess.query(UkraineFaculties).filter(UkraineFaculties.faculty_name == j['name']).filter(UkraineFaculties.univer_id == univer.id).first()

        # критерии для факультативов
        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria21, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u21'])
        db_sess.add(item_criter)
        db_sess.commit()

        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria211, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u211'])
        db_sess.add(item_criter)
        db_sess.commit()

        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria212, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u212'])
        db_sess.add(item_criter)
        db_sess.commit()

        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria213, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u213'])
        db_sess.add(item_criter)
        db_sess.commit()

        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria22, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u22'])
        db_sess.add(item_criter)
        db_sess.commit()

        item_criter = ItemsAndCriteria(item_id=facult.id, criteria=criteria23, item_type='faculty',
                                       univer_id=univer.id, country='ukraine', value=j['u23'])
        db_sess.add(item_criter)
        db_sess.commit()

        # департаменты
        for l in j['departmets']:
            depart = UkraineDepartments(department_name=l['name'], faculty=facult)
            db_sess.add(depart)
            db_sess.commit()

            depart = db_sess.query(UkraineDepartments).filter(UkraineDepartments.department_name == l['name']).filter(UkraineDepartments.faculty_id == facult.id).first()

            # критерии для департаментов
            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria21, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u21'])
            db_sess.add(item_criter)
            db_sess.commit()

            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria211, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u211'])
            db_sess.add(item_criter)
            db_sess.commit()

            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria212, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u212'])
            db_sess.add(item_criter)
            db_sess.commit()

            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria213, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u213'])
            db_sess.add(item_criter)
            db_sess.commit()

            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria22, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u22'])
            db_sess.add(item_criter)
            db_sess.commit()

            item_criter = ItemsAndCriteria(item_id=depart.id, criteria=criteria23, item_type='department',
                                           univer_id=univer.id, country='ukraine', value=l['u23'])
            db_sess.add(item_criter)
            db_sess.commit()

            for f in l['scientiests']:
                scientist_name = ' '.join(f['name'].split())
                scientist_db = db_sess.query(Ukraine_Scientists).filter(Ukraine_Scientists.name == scientist_name).first()

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
