from data.database.keywords import Keywords
from data.Standart import db_session

db_session.global_init("db/database.db")
db_sess = db_session.create_session()
# text = []
# for kw in db_sess.query(Keywords).filter(Keywords.id>10000).all():
#     text.append(f"{kw.id} : {kw.word}\n")
#     if kw.id>=11068:
#         break
# with open ("kw.txt", "w", encoding="utf-8") as file:
#          file.writelines(text)

# for i in range (11):
#     with open (f"kw{i}.txt", "w", encoding="utf-8") as file:
#         file.writelines(text[1000*i:1000*(i+1)])

with open("kw.txt", encoding="utf-8") as file:
    for line in file:
        id, word = line.split(":")
        id = int (id.strip())
        word=word.strip()
        kw = db_sess.query(Keywords).get(id)
        kw.word = word
        db_sess.commit()
        print (id, word)