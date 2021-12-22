from data.database.ukraine_universities import Ukraine_Universities
from data.Standart import db_session
db_session.global_init("db/database.db")
db_sess = db_session.create_session()
for u in db_sess.query(Ukraine_Universities).filter(Ukraine_Universities.region == "ua-ks").all():
    u.region = "ua-kc"
db_sess.commit()