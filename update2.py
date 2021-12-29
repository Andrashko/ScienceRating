from data.Standart import db_session
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.criteria import Criterias
from data.database.keywords import Keywords 

db_session.global_init("db/database.db")
db_sess = db_session.create_session()

# crit_list = [23,33]
# for dep in db_sess.query(UkraineDepartments).all():
#     for cr in crit_list:
#         value = 0
#         for sc in db_sess.query(Ukraine_Scientists).filter(Ukraine_Scientists.department_id == dep.id).all():
#             for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "scientist").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == sc.id):
#                 value += int(criteria.value)
            
#         is_first = True
#         for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == dep.id):
#             if is_first and value != 0:
#                 criteria.value = value
#                 is_first = False
#             else:
#                 db_sess.delete(criteria)
#         if is_first and value != 0:
#             criteria = ItemsAndCriteria()
#             criteria.criteria_id = cr
#             criteria.item_type = "department"
#             criteria.country = "ukraine"
#             criteria.item_id = dep.id      
#             criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#             criteria.value = value
#             db_sess.add(criteria)

#     db_sess.commit()  
#     print(f"departmrnt {dep.id}")


crit_list = [23,33,6,7,9,10,11,12]
for fac in db_sess.query(UkraineFaculties).all():
    for cr in crit_list:
        value = 0
        for dep in db_sess.query(UkraineDepartments).filter(UkraineDepartments.faculty_id == fac.id).all():
            for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == dep.id):
                value += int(criteria.value)
            
        is_first = True
        for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == fac.id):
            if is_first and value != 0:
                criteria.value = value
                is_first = False
            else:
                db_sess.delete(criteria)
        if is_first and value != 0:
            criteria = ItemsAndCriteria()
            criteria.criteria_id = cr
            criteria.item_type = "faculty"
            criteria.country = "ukraine"
            criteria.item_id = fac.id      
            criteria.univer_id = fac.univer_id
            criteria.value = value
            db_sess.add(criteria)

    db_sess.commit()  
    print(f"faculty {fac.id}")

for univer in db_sess.query(Ukraine_Universities).all():
    for cr in crit_list:
        value = 0
        for fac in db_sess.query(UkraineFaculties).filter(UkraineFaculties.univer_id == univer.id).all():
            for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == fac.id):
                value += int(criteria.value)
            
        is_first = True
        for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == cr).filter(ItemsAndCriteria.item_id == univer.id):
            if is_first and value != 0:
                criteria.value = value
                is_first = False
            else:
                db_sess.delete(criteria)
        if is_first and value != 0:
            criteria = ItemsAndCriteria()
            criteria.criteria_id = cr
            criteria.item_type = "university"
            criteria.country = "ukraine"
            criteria.item_id = univer.id     
            criteria.univer_id = univer.id  
            criteria.value = value
            db_sess.add(criteria)

    db_sess.commit()  
    print(f"univer {univer.id}")