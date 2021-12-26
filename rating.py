from data.Standart import db_session
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.criteria import Criterias

"""
Функция находит рейтинг университета 
"""


def calculate_university_rating(univer):
    db_sess = db_session.create_session()
    rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == univer.id)
    try:
        rating_value = 0
        for j in rating:
            if j.criteria_id == 7 and univer.scientists:
                rating_value += int(int(j.value) * 100 /
                                    len(univer.scientists))
            elif db_sess.query(Criterias).get(j.criteria_id).number in [str(_) for _ in range(1, 16)]:
                rating_value += int(j.value)
            # QS
            if j.criteria_id == 199:
                rating_value += 1000 * int(j.value)
            if j.criteria_id == 200:
                rating_value += 2000 * int(j.value)

        rating_value += len(univer.projects) * 100

        return rating_value
    except ZeroDivisionError:
        return 0
    except AttributeError:
        return 0
