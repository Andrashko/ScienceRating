from data.database.keywords import Keywords
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.keywords import Keywords
from data.Standart import db_session
import json

db_session.global_init("db/database.db")
db_sess = db_session.create_session()
from data.database.keywords import Keywords
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.keywords import Keywords
from data.Standart import db_session
import json

db_session.global_init("db/database.db")
db_sess = db_session.create_session()
with open('db/scopus.json', encoding='utf-8') as file:
    scop = json.load(file)
    for scientist in db_sess.query(Ukraine_Scientists).all():
        if scientist.science:
            dbkw = Keywords(word=scientist.science, priority=30, scientist_id=scientist.id)
            db_sess.add(dbkw)
            db_sess.commit()  
        if scientist.id % 100 == 0:
            print (scientist.id) 
