from data.database.keywords import Keywords
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.keywords import Keywords
from data.Standart import db_session
import json

db_session.global_init("db/database.db")
db_sess = db_session.create_session()
with open('db/scopus.json', encoding='utf-8') as file:
    scop = json.load(file)
    keywords_frequency = {"science":1}
    for scientist in db_sess.query(Ukraine_Scientists).all():
        for i in scop:
            if i['name'] == scientist.name:
                keywords = i.get("keywords")
                if keywords:
                    count = 20
                    skip = False
                    for kw in keywords:
                        for w in scientist.keywords:
                            if w.word == kw:
                                skip = True
                                break
                        if skip:
                            continue
                        dbkw = Keywords(word=kw, priority=count, scientist_id=scientist.id)
                        db_sess.add(dbkw)
                        db_sess.commit()

                        if count <= 10:
                            count -=1
                        else:
                            count -=5
                print(scientist.id)