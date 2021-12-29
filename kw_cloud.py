from wordcloud import WordCloud
import io
import base64
from data.database.ukraine_departments  import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_faculties import UkraineFaculties
from data.Standart import db_session

cache = {}

NO_KEYWORDS = {"Наука": 1}

def get_word_cloud_picture(freq):
    pil_img = WordCloud(width=300, height=200, background_color="white", max_words=10, prefer_horizontal=1, min_font_size=10).generate_from_frequencies(freq).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64

def get_keyword_frequency_for_scientist(id):
    db_sess = db_session.create_session()
    scientist = db_sess.query(Ukraine_Scientists).get(id) 
    keywords_frequency = {}
    for kw in scientist.keywords:
        keywords_frequency [kw.word] = kw.priority
    if len(keywords_frequency)>0:
        return keywords_frequency
    return NO_KEYWORDS
    
def get_keyword_frequency_for_department(id):
    db_sess = db_session.create_session()
    department = db_sess.query(UkraineDepartments).get(id)
    keywords_frequency = {}
    for scientist in department.scientists:
        for kw in scientist.keywords:
            if (keywords_frequency.get(kw.word)):
                keywords_frequency [kw.word] += kw.priority
            else:
                keywords_frequency [kw.word] = kw.priority
    if len(keywords_frequency)>0:
        return keywords_frequency
    return NO_KEYWORDS

def get_keyword_frequency_for_university(id):
    if cache.get(id):
        return cache[id]
    db_sess = db_session.create_session()
    univer = db_sess.query(Ukraine_Universities).get(id)
    keywords_frequency = {}
    for scientist in univer.scientists:
        for kw in scientist.keywords:
            if (keywords_frequency.get(kw.word)):
                keywords_frequency [kw.word] += kw.priority
            else:
                keywords_frequency [kw.word] = kw.priority
    if len(keywords_frequency)>0:
        cache[id] = keywords_frequency
        return keywords_frequency
    return NO_KEYWORDS

def get_keyword_frequency_for_faculty(id):
    db_sess = db_session.create_session()
    faculty = db_sess.query(UkraineFaculties).get(id)
    keywords_frequency = {}
    for department in faculty.departments:
        for scientist in department.scientists:
            for kw in scientist.keywords:
                if (keywords_frequency.get(kw.word)):
                    keywords_frequency [kw.word] += kw.priority
                else:
                    keywords_frequency [kw.word] = kw.priority
    if len(keywords_frequency)>0:
        return keywords_frequency
    return NO_KEYWORDS