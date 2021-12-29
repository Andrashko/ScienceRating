from data.Standart import db_session
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.criteria import Criterias
from data.database.keywords import Keywords
from data.database.univer_projects import UniverProjects
from rating import calculate_scientist_rating, calculate_university_rating

db_session.global_init("db/database.db")
db_sess = db_session.create_session()

# for sci in db_sess.query(Ukraine_Scientists).all()[9700:]:
#     val = calculate_scientist_rating(sci)
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "scientist").filter(ItemsAndCriteria.criteria_id == 300).filter(ItemsAndCriteria.item_id == sci.id):
#         if is_first:
#             criteria.value = val
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 300
#         criteria.item_type = "scientist"
#         criteria.country = "ukraine"
#         criteria.item_id = sci.id     
#         criteria.univer_id = sci.univer_id
#         criteria.value = val   
#         db_sess.add(criteria)
#     db_sess.commit()
#     print(sci.id)

# for univer in db_sess.query(Ukraine_Universities).all():
#     val = calculate_university_rating(univer)


#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 301).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = val
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 301
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = val
#         db_sess.add(criteria)
#     db_sess.commit()
#     print(univer.id)

for univer in db_sess.query(Ukraine_Universities).all():
    mag = 0
    bak = 0
    if univer.students_bak:
        bak = univer.students_bak
    if univer.students_mag:
        mag = univer.students_mag
    is_first = True
    for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 1).filter(ItemsAndCriteria.item_id == univer.id):
        if is_first:
            criteria.value = bak+mag
            is_first = False
        else:
            db_sess.delete(criteria)
    if is_first:
        criteria = ItemsAndCriteria()
        criteria.criteria_id = 1
        criteria.item_type = "university"
        criteria.country = "ukraine"
        criteria.item_id = univer.id      
        criteria.univer_id = univer.id
        criteria.value = bak+mag
        db_sess.add(criteria)

    is_first = True
    for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 2).filter(ItemsAndCriteria.item_id == univer.id):
        if is_first:
            criteria.value = bak
            is_first = False
        else:
            db_sess.delete(criteria)
    if is_first:
        criteria = ItemsAndCriteria()
        criteria.criteria_id = 2
        criteria.item_type = "university"
        criteria.country = "ukraine"
        criteria.item_id = univer.id      
        criteria.univer_id = univer.id
        criteria.value = bak
        db_sess.add(criteria)
    
    is_first = True
    for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 3).filter(ItemsAndCriteria.item_id == univer.id):
        if is_first:
            criteria.value = mag
            is_first = False
        else:
            db_sess.delete(criteria)
    if is_first:
        criteria = ItemsAndCriteria()
        criteria.criteria_id = 3
        criteria.item_type = "university"
        criteria.country = "ukraine"
        criteria.item_id = univer.id      
        criteria.univer_id = univer.id
        criteria.value = mag
        db_sess.add(criteria)


    pr = db_sess.query(UniverProjects).filter(UniverProjects.univer_id == univer.id).count()
    is_first = True
    for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 44).filter(ItemsAndCriteria.item_id == univer.id):
        if is_first:
            criteria.value = pr
            is_first = False
        else:
            db_sess.delete(criteria)
    if is_first:
        criteria = ItemsAndCriteria()
        criteria.criteria_id = 44
        criteria.item_type = "university"
        criteria.country = "ukraine"
        criteria.item_id = univer.id      
        criteria.univer_id = univer.id
        criteria.value = pr
        db_sess.add(criteria)


    db_sess.commit()
    print(univer.id)

# for dep in db_sess.query(UkraineDepartments).all():
#     sc = db_sess.query(Ukraine_Scientists).filter(Ukraine_Scientists.department_id == dep.id)
#     doctors = sc.filter(Ukraine_Scientists.degree.ilike("%доктор%")).count()
#     candidats = sc.filter(Ukraine_Scientists.degree.ilike("%кандидат%")).count()
#     total = sc.count()
    
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 6).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = total
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 6
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = total
#         db_sess.add(criteria)

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = doctors+candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 7
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = doctors+candidats
#         db_sess.add(criteria)

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 9).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 9
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = candidats
#         db_sess.add(criteria)
    
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 10).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = doctors
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 10
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = doctors
#         db_sess.add(criteria)

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 11).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 11
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 12).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 12
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)
    
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "department").filter(ItemsAndCriteria.criteria_id == 13).filter(ItemsAndCriteria.item_id == dep.id):
#         if is_first:
#             criteria.value = (doctors+candidats)*100/total if total>0 else 0
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#     if is_first:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 13
#         criteria.item_type = "department"
#         criteria.country = "ukraine"
#         criteria.item_id = dep.id      
#         criteria.univer_id = db_sess.query(UkraineFaculties).get(dep.faculty_id).univer_id
#         criteria.value = (doctors+candidats)*100/total if total>0 else 0
#         db_sess.add(criteria)
#     db_sess.commit()
#     print(f"dep {dep.id}")


# оновить показатели scopus для ученого
# from json import load
# with open ("db/scopus.json", encoding="utf-8") as file:
#     sc = load(file)

# for sci in db_sess.query(Ukraine_Scientists).all():
#     for s in sc:
#         if s.get("name") == sci.name:
#             is_first = True
#             for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "scientist").filter(ItemsAndCriteria.criteria_id == 23).filter(ItemsAndCriteria.item_id == sci.id):
#                 if is_first:
#                     criteria.value = s.get("documents")
#                     is_first = False
#                 else:
#                     db_sess.delete(criteria)
#                 db_sess.commit()
#             else:
#                 criteria = ItemsAndCriteria()
#                 criteria.criteria_id = 23
#                 criteria.item_type = "scientist"
#                 criteria.country = "ukraine"
#                 criteria.item_id = sci.id     
#                 criteria.univer_id = sci.univer_id
#                 criteria.value = s.get("documents")    
#                 db_sess.add(criteria)
#                 db_sess.commit()
            
#             for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "scientist").filter(ItemsAndCriteria.criteria_id == 33).filter(ItemsAndCriteria.item_id == sci.id):
#                 if is_first:
#                     criteria.value = s.get("documents")
#                     is_first = False
#                 else:
#                     db_sess.delete(criteria)
#                 db_sess.commit()
#             else:
#                 criteria = ItemsAndCriteria()
#                 criteria.criteria_id = 33
#                 criteria.item_type = "scientist"
#                 criteria.country = "ukraine"
#                 criteria.item_id = sci.id     
#                 criteria.univer_id = sci.univer_id
#                 criteria.value = s.get("citations")    
#                 db_sess.add(criteria)
#                 db_sess.commit()
            
#             break
#     print(sci.id)


# for fac in db_sess.query(UkraineFaculties).all():
#     sc = 0
#     doctors = 0
#     candidats = 0
#     total = 0
#     for dep in db_sess.query(UkraineDepartments).filter(UkraineDepartments.faculty_id == fac.id).all():
#         sc = db_sess.query(Ukraine_Scientists).filter(Ukraine_Scientists.department_id == dep.id)
#         doctors += sc.filter(Ukraine_Scientists.degree.ilike("%доктор%")).count()
#         candidats += sc.filter(Ukraine_Scientists.degree.ilike("%кандидат%")).count()
#         total += sc.count()
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 6).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = total
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 6
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = total
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = doctors+candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 7
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = doctors+candidats
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 9).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 9
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = candidats
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 10).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = doctors
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 10
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = doctors
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 11).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 11
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 12).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 12
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "faculty").filter(ItemsAndCriteria.criteria_id == 13).filter(ItemsAndCriteria.item_id == fac.id):
#         if is_first:
#             criteria.value = (doctors+candidats)*100/total if total>0 else 0  
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 13
#         criteria.item_type = "faculty"
#         criteria.country = "ukraine"
#         criteria.item_id = fac.id      
#         criteria.univer_id = fac.univer_id
#         criteria.value = (doctors+candidats)*100/total   if total>0 else 0  
#         db_sess.add(criteria)
#         db_sess.commit()
#     print(fac.id)




# for univer in db_sess.query(Ukraine_Universities).all():
#     sc = db_sess.query(Ukraine_Scientists).filter(Ukraine_Scientists.univer_id == univer.id)
#     doctors = sc.filter(Ukraine_Scientists.degree.ilike("%доктор%")).count()
#     candidats = sc.filter(Ukraine_Scientists.degree.ilike("%кандидат%")).count()
#     total = sc.count()
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 6).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = total
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 6
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = total 
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = doctors+candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 7
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = doctors+candidats
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 9).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = candidats
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 9
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = candidats
#         db_sess.add(criteria)
#         db_sess.commit()
        
#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 10).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = doctors
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 10
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = doctors
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 11).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 11
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 12).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value = total - (doctors+candidats)
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 12
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = total - (doctors+candidats)
#         db_sess.add(criteria)
#         db_sess.commit()

#     is_first = True
#     for criteria in db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == "university").filter(ItemsAndCriteria.criteria_id == 13).filter(ItemsAndCriteria.item_id == univer.id):
#         if is_first:
#             criteria.value =  (doctors+candidats)*100/total  if total>0 else 0
#             is_first = False
#         else:
#             db_sess.delete(criteria)
#         db_sess.commit()
#     else:
#         criteria = ItemsAndCriteria()
#         criteria.criteria_id = 13
#         criteria.item_type = "university"
#         criteria.country = "ukraine"
#         criteria.item_id = univer.id      
#         criteria.univer_id = univer.id
#         criteria.value = (doctors+candidats)*100/total   if total>0 else 0     
#         db_sess.add(criteria)
#         db_sess.commit()

#     print(univer.id)