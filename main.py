from flask import Flask, render_template, request, session, redirect
import requests
import json
from bs4 import BeautifulSoup as BS
from sqlalchemy import or_
from dotenv import load_dotenv
import threading
from rating import calculate_university_rating, get_articles, get_projects, get_students, get_scientists, \
    calculate_department_rating, calculate_faculty_rating, calculate_employee_rating, calculate_international_rating, calculate_national_rating,\
        calculate_national_rating, calculate_project_rating, calculate_students_rating, calculate_publication_rating, calculate_scientist_rating
from data_load import scientists, universities, map_uk, articles_main_page, students_main_page
from kw_cloud import get_keyword_frequency_for_department, get_keyword_frequency_for_faculty, \
    get_keyword_frequency_for_scientist, get_keyword_frequency_for_university, get_word_cloud_picture

from data.Standart import db_session
from mail_sender import send_mail
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.Forms.Login import LoginForm
from data.Forms.Registration import RegisterForm
from data.database.user import User
from data.database.kaz_universities import Kaz_Universities
from data.database.univer_projects import UniverProjects
from data.database.items_and_criteria import ItemsAndCriteria
from data.database.ukraine_universities import Ukraine_Universities
from data.database.ukraine_faculties import UkraineFaculties
from data.database.ukraine_departments import UkraineDepartments
from data.database.ukraine_scientists import Ukraine_Scientists
from data.database.criteria import Criterias
from data.database.keywords import Keywords

db_session.global_init("db/database.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rating_sk'
BASE_URL = "http://science-rating.co.ua"  # необходимо для роботы редиректа на хостинге
BASE_URL = ""  # Для роботы на локахосте

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(BASE_URL + '/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(BASE_URL + '/')
        return render_template('login.html', msg='Неправильний логін або пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, msg='Паролі не співпадають')
        if form.login.data.isdigit():
            return render_template('register.html', form=form, msg='Логін не може складатися лише з цифр')
        for i in form.login.data:
            if (not i.isdigit()) and (not i.isalpha()):
                return render_template('register.html', form=form, msg='У логіні можуть бути лише цифри та літери')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.user_email == form.email.data).first():
            return render_template('register.html', form=form, msg='Користувач із цією поштою вже існує')
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', form=form, msg='Такий користувач уже є')
        user = User(
            login=form.login.data,
            user_email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        threading.Thread(target=send_mail, args=[form.email.data, 'Реєстрація пройшла успішно',
                                                 f'Ваш логін: {form.login.data}']).start()
        return redirect(BASE_URL + '/login')
    return render_template('register.html', form=form)


@app.route('/')
def universities_rating():
    db_sess = db_session.create_session()
    univers = []
    for i in universities[:10]:
        if len(i[0]) > 65:
            univers.append([i[0][:65].strip() + '...', i[1], i[2]])
        else:
            univers.append([i[0], i[1], i[2]])

    return render_template('universities_rating.html', color_page_one='#F63E3E', univers_rating=univers,
                           map_uk=map_uk, univers=len(universities), students=students_main_page,
                           articles=articles_main_page, scientists=len(db_sess.query(Ukraine_Scientists).all()),
                           users=len(db_sess.query(User).all()))


@app.route('/scientists')
def all_scientists():
    db_sess = db_session.create_session()
    return render_template('scientists.html', scientists=scientists[:500], color_page_three='#F63E3E')


@app.route('/add_compare/<int:univer_id>')
def add_compare(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    if 'univers' not in session:
        session['univers'] = [univer_id]
    else:
        if len(session['univers']) < 5 and univer_id not in session['univers']:
            univers = session['univers']
            univers.append(univer_id)
            session['univers'] = univers

    return redirect(BASE_URL + '/universities')


@app.route('/delete_compare/<int:univer_id>')
def delete_compare(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    if 'univers' in session:
        if session['univers']:
            univers = session['univers']
            univers.pop(univers.index(univer_id))
            session['univers'] = univers

    return redirect(BASE_URL + '/universities')


@app.route('/universities')
def all_universities():
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()

    univers_compare = []
    univers_js = {'students': [], 'scientists': [],
                  'faculties': [], 'rating': [], 'departments': [],
                  'univers': []}
    if 'univers' in session:
        univers_compare = [[db_sess.query(Ukraine_Universities).get(i).univername, i] for i in session['univers']]
    else:
        session['univers'] = []

    for i in univers_compare:
        univer = db_sess.query(Ukraine_Universities).get(i[1])

        if len(univer.univername) > 30:
            univers_js['univers'].append(univer.univername.replace('"', "«")[:30].strip() + '...')
        else:
            univers_js['univers'].append(univer.univername.replace('"', "«"))
        if univer.students_bak and univer.students_mag:
            univers_js['students'].append(f'{univer.students_bak + univer.students_mag}')
        else:
            univers_js['students'].append('0')

        faculty_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'faculty').filter(
            ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == univer.id)

        department_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'department').filter(
            ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == univer.id)

        faculties = []
        if faculty_rating:
            for j in faculty_rating:
                if (' - без факультету' not in db_sess.query(UkraineFaculties).get(j.item_id).faculty_name) and \
                        (not db_sess.query(UkraineFaculties).get(j.item_id).faculty_name.isdigit()):
                    faculties.append(db_sess.query(UkraineFaculties).get(j.item_id).faculty_name)

        departments = []
        if department_rating:
            for j in department_rating:
                departments.append(db_sess.query(UkraineDepartments).get(j.item_id).department_name)

        univers_js['faculties'].append(f'{len(faculties)}')
        univers_js['departments'].append(f'{len(departments)}')
        univers_js['scientists'].append(f'{len(univer.scientists)}')

        rating = universities[[j[0] for j in universities].index(i[0])][1]
        try:
            univers_js['rating'].append(f'{rating}')
        except ZeroDivisionError:
            univers_js['rating'].append('0')
        except AttributeError:
            univers_js['rating'].append('0')

    for i in range(len(univers_compare)):
        if len(univers_compare[i][0]) > 50:
            univers_compare[i][0] = univers_compare[i][0][:50].strip() + '...'

    universities_rev = list(reversed(universities))
    universities_name = sorted([[i.univername, i.id] for i in db_sess.query(Ukraine_Universities)], key=lambda x: x[0])

    universities_region = {'ua-ch': list(filter(lambda x: x[3] == 'ua-ch', universities)),
                           'ua-ck': list(filter(lambda x: x[3] == 'ua-ck', universities)),
                           'ua-cv': list(filter(lambda x: x[3] == 'ua-cv', universities)),
                           'ua-dp': list(filter(lambda x: x[3] == 'ua-dp', universities)),
                           'ua-dt': list(filter(lambda x: x[3] == 'ua-dt', universities)),
                           'ua-if': list(filter(lambda x: x[3] == 'ua-if', universities)),
                           'ua-kc': list(filter(lambda x: x[3] == 'ua-kc', universities)),
                           'ua-kh': list(filter(lambda x: x[3] == 'ua-kh', universities)),
                           'ua-kk': list(filter(lambda x: x[3] == 'ua-kk', universities)),
                           'ua-km': list(filter(lambda x: x[3] == 'ua-km', universities)),
                           'ua-kr': list(filter(lambda x: x[3] == 'ua-kr', universities)),
                           'ua-ks': list(filter(lambda x: x[3] == 'ua-ks', universities)),
                           'ua-kv': list(filter(lambda x: x[3] == 'ua-kv', universities)),
                           'ua-lh': list(filter(lambda x: x[3] == 'ua-lh', universities)),
                           'ua-lv': list(filter(lambda x: x[3] == 'ua-lv', universities)),
                           'ua-mk': list(filter(lambda x: x[3] == 'ua-mk', universities)),
                           'ua-my': list(filter(lambda x: x[3] == 'ua-my', universities)),
                           'ua-pl': list(filter(lambda x: x[3] == 'ua-pl', universities)),
                           'ua-rv': list(filter(lambda x: x[3] == 'ua-rv', universities)),
                           'ua-sc': list(filter(lambda x: x[3] == 'ua-sc', universities)),
                           'ua-sm': list(filter(lambda x: x[3] == 'ua-sm', universities)),
                           'ua-tp': list(filter(lambda x: x[3] == 'ua-tp', universities)),
                           'ua-vi': list(filter(lambda x: x[3] == 'ua-vi', universities)),
                           'ua-vo': list(filter(lambda x: x[3] == 'ua-vo', universities)),
                           'ua-zk': list(filter(lambda x: x[3] == 'ua-zk', universities)),
                           'ua-zp': list(filter(lambda x: x[3] == 'ua-zp', universities)),
                           'ua-zt': list(filter(lambda x: x[3] == 'ua-zt', universities))
                           }

    return render_template('universities.html', color_page_one='#F63E3E',
                           univers=universities, univers_rev=universities_rev, univers_name=universities_name,
                           univers_compare=univers_compare, univers_js=univers_js,
                           univers_region=universities_region)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()
    inp = ''
    univers = []
    scientists = []
    univers_kw = []
    scientists_kw = []

    if request.method == 'POST':
        if 'inp_val' in request.form.keys():
            inp = request.form['inp_val'].strip()

        if inp:
            univers = sorted(
                [[i.univername, i.id] for i in db_sess.query(Ukraine_Universities).all() if inp.lower() in
                 i.univername.lower()], key=lambda x: x[0])[:500]

            scientists = sorted([[i.name, i.id] for i in db_sess.query(Ukraine_Scientists).all()
                                 if inp.lower() in i.name.lower()],
                                key=lambda x: x[0])[:500]

            for kw in db_sess.query(Keywords).filter(Keywords.word.ilike(f"%{inp}%")).all():
                try:
                    scientist = db_sess.query(Ukraine_Scientists).get(kw.scientist_id)
                    univer = db_sess.query(Ukraine_Universities).get(scientist.univer_id)
                    if all(map(lambda x: x[1] != scientist.id, scientists_kw)):
                        scientists_kw.append([scientist.name, scientist.id])
                    if all(map(lambda x: x[1] != univer.id, univers_kw)):
                        univers_kw.append([univer.univername, univer.id])
                except Exception:
                    continue
            scientists_kw = sorted(scientists_kw, key=lambda x: x[0])[:500]
            univers_kw = sorted(univers_kw, key=lambda x: x[0])[:500]

    return render_template('search.html', value=inp, univers=univers, scientists=scientists,
                           univers_kw=univers_kw, scientists_kw=scientists_kw)


@app.route('/university_info/<int:university_id>')
def university_info(university_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()
    university = db_sess.query(Ukraine_Universities).get(university_id)

    faculties = []
    faculties_rev = []
    faculties_name = []
    departments = []
    departments_rev = []
    departments_name = []
    for fac in db_sess.query(UkraineFaculties).filter(UkraineFaculties.univer_id == university_id).all():
        if ' - без факультету' not in fac.faculty_name:
            faculties.append([fac.faculty_name, fac.id, calculate_faculty_rating(fac)])
        for dep in db_sess.query(UkraineDepartments).filter(UkraineDepartments.faculty_id == fac.id).all():
            departments.append([dep.department_name, dep.id, calculate_department_rating(dep)])
    faculties = sorted(faculties, key=lambda x: x[2], reverse=True)
    faculties_rev = faculties[::-1]
    faculties_name = sorted(faculties, key=lambda x: x[0])

    departments = sorted(departments, key=lambda x: x[2], reverse=True)
    departments_rev = departments[::-1]
    departments_name = sorted(departments, key=lambda x: x[0])

    facult_depart = []
    facult_empty = True
    depart_empty = True
    for i in range(len(departments)):
        if not departments and not faculties:
            facult_depart = []
            break

        try:
            facult_depart.append([faculties[i][0], faculties[i][1], faculties[i][2]])
            facult_empty = False
        except IndexError:
            facult_depart.append(['', -1, 0])

        try:
            facult_depart[i].append([departments[i][0], departments[i][1], departments[i][2]])
            depart_empty = False
        except IndexError:
            facult_depart[i].append([' ', -1, 0])

    facult_depart_rev = []
    for i in range(len(departments)):
        if not departments and not faculties:
            facult_depart_rev = []
            break

        try:
            facult_depart_rev.append([faculties_rev[i][0], faculties_rev[i][1], faculties_rev[i][2]])
            facult_empty = False
        except IndexError:
            facult_depart_rev.append(['', -1, 0])

        try:
            facult_depart_rev[i].append([departments_rev[i][0], departments_rev[i][1], departments_rev[i][2]])
            depart_empty = False
        except IndexError:
            facult_depart_rev[i].append([' ', -1, 0])

    facult_depart_name = []
    for i in range(len(departments)):
        if not departments and not faculties:
            facult_depart_name = []
            break

        try:
            facult_depart_name.append([faculties_name[i][0], faculties_name[i][1]])
            facult_empty = False
        except IndexError:
            facult_depart_name.append(['', -1])

        try:
            facult_depart_name[i].append([departments_name[i][0], departments_name[i][1]])
            depart_empty = False
        except IndexError:
            facult_depart_name[i].append(' ')

    return render_template('university_info.html',
                           facult_depart=facult_depart, facult_depart_rev=facult_depart_rev,
                           facult_depart_name=facult_depart_name, univer=university, facult_empty=facult_empty,
                           depart_empty=depart_empty,
                           keywords_cloud=get_word_cloud_picture(get_keyword_frequency_for_university((university_id))))


@app.route('/university_projects/<int:univer_id>')
def university_projects(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()
    univer = db_sess.query(Ukraine_Universities).get(univer_id)
    return render_template('university_projects.html', univer=univer)


@app.route('/faculty_info/<int:faculty_id>')
def faculty_info(faculty_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()
    faculty = db_sess.query(UkraineFaculties).get(faculty_id)
    departments = []
    departments_rev = []
    departments_name = []
    for dep in db_sess.query(UkraineDepartments).filter(UkraineDepartments.faculty_id == faculty_id).all():
        departments.append([dep.department_name, dep.id, calculate_department_rating(dep)])
    departments = sorted(departments, key=lambda x: x[2], reverse=True)
    departments_rev = list(reversed(departments))
    departments_name = sorted(departments, key=lambda x: x[0])

    return render_template('faculty_info.html', departments=departments, departments_rev=departments_rev,
                           departments_name=departments_name, faculty=faculty,
                           keywords_cloud=get_word_cloud_picture(get_keyword_frequency_for_faculty((faculty_id))))


@app.route('/department_info/<int:depart_id>')
def department_info(depart_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()
    depart = db_sess.query(UkraineDepartments).get(depart_id)
    univer_id = db_sess.query(UkraineFaculties).get(depart.faculty_id).univer_id
    return render_template('department_info.html',
                           depart=depart, univer_id=univer_id,
                           keywords_cloud=get_word_cloud_picture(get_keyword_frequency_for_department((depart_id))))


@app.route('/university_info_rating/<int:university_id>')
def university_info_rating(university_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()

    university = db_sess.query(Ukraine_Universities).get(university_id)

    criters_values = []
    students = get_students(university_id)
    scientists = get_scientists(university_id)
    articles = get_articles(university_id)

    criters_values.append(['Освітня діяльність', calculate_students_rating(university), True])
    criters_values += students

    criters_values.append(['Кадровый потенціал', calculate_employee_rating (university, "university"), True])
    criters_values += scientists

    criters_values.append(['Публікаційна діяльність', calculate_publication_rating (university, "university"), True])
    criters_values += articles

    criters_values.append(['Проєктна діяльність', calculate_project_rating(university), True])


    return render_template('university_info_rating.html', univer=university, criters_values=criters_values,
                           rating_value=calculate_university_rating(university))


@app.route('/scientist_info/<int:scientist_id>')
def scientist_info(scientist_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL + '/login')

    db_sess = db_session.create_session()

    scientist = db_sess.query(Ukraine_Scientists).get(scientist_id)
    info = [scientist.name.split()]

    if scientist.google_scholar and (scientist.google_scholar != '-'):
        info.append(scientist.google_scholar)
    else:
        info.append(False)

    if scientist.scopus and (scientist.scopus != '-'):
        info.append(scientist.scopus)
    else:
        info.append(False)

    if scientist.publon and (scientist.publon != '-'):
        info.append(scientist.publon)
    else:
        info.append(False)

    try:
        univer_name = db_sess.query(Ukraine_Universities).get(scientist.univer_id).univername
        if len(univer_name) > 57:
            info.append(univer_name[:57].strip() + '...')
        else:
            info.append(univer_name)
    except AttributeError:
        info.append('')
    if scientist.degree and ('немає' not in scientist.degree):
        info.append(scientist.degree)
    else:
        info.append(False)
    if scientist.science:
        info.append(scientist.science)
    else:
        info.append(False)

    SIZE = 60
    google_scholar = []
    graph = False
    stat_info = []
    if scientist.google_scholar and (scientist.google_scholar != '-'):
        res = requests.get(scientist.google_scholar)
        html = BS(res.content, 'html.parser')

        graph = {'years': [i.text for i in html.find_all('span', class_='gsc_g_t')],
                 'gr': [i.text for i in html.find_all('span', class_='gsc_g_al')],
                 'colors': ['#F63E3E' for i in range(len(html.find_all('span', class_='gsc_g_t')))]}
        try:
            stat_info = [f"Статистика цитування: {html.find_all('td', class_='gsc_rsb_std')[0].text}",
                         f"h-індекс: {html.find_all('td', class_='gsc_rsb_std')[2].text}",
                         f"i10-індекс: {html.find_all('td', class_='gsc_rsb_std')[4].text}"]
        except IndexError:
            stat_info = False

        for i in html.find_all('tr', class_='gsc_a_tr'):
            try:
                a_one = i.find_all('a', class_='gsc_a_at')[0].text[:SIZE].strip() + '...'
            except IndexError:
                a_one = ''

            try:
                a_one_href = 'https://scholar.google.com.ua' + i.find_all('a', class_='gsc_a_at')[0].get('href')
            except IndexError:
                a_one_href = ''

            try:
                div_one = i.find_all('div')[0].text
            except IndexError:
                div_one = ''

            try:
                div_two = i.find_all('div')[1].text[:SIZE].strip() + '...'
            except IndexError:
                div_two = ''

            try:
                a_two = i.find_all('a', class_='gsc_a_ac gs_ibl')[0].text
            except IndexError:
                a_two = ''

            try:
                a_two_href = i.find_all('a', class_='gsc_a_ac gs_ibl')[0].get('href')
            except IndexError:
                a_two_href = ''

            try:
                span = i.find_all('span', class_='gsc_a_h gsc_a_hc gs_ibl')[0].text
            except IndexError:
                span = ''
            google_scholar.append([[a_one, a_one_href], div_one, div_two, [a_two, a_two_href], span])

        photo = True
        if 'https' in html.find_all('img', id='gsc_prf_pup-img')[0].get('src'):
            info.append(html.find_all('img', id='gsc_prf_pup-img')[0].get('src'))
        else:
            photo = False
    else:
        google_scholar = False
        photo = False

    if scientist.publon:
        url = f'https://publons.com/api/v2/academic/publication/' \
              f'?academic={scientist.publon.split("/")[len(scientist.publon.split("/")) - 1]}'
        headers = {"Authorization": "Token 01aa647bdc5658a42d90d629265b6d6443891e44",
                   "Content-Type": "application/json"}
        res = requests.get(url, headers=headers)
        articles = json.loads(res.content)
    SIZE_title = 60
    SIZE_journal = 40

    try:
        publon = []
        if scientist.publon and (scientist.publon != '-'):
            for i in articles['results']:
                title = i['publication']['title'][:SIZE_title].strip() + '...'
                journal_name = i['journal']['name'][:SIZE_journal].strip() + '...'

                publon.append([i['publication']['ids']['url'], title,
                               i['publication']['date_published'].replace('-', '.'),
                               i['journal']['ids']['url'], journal_name])
    except KeyError:
        publon = 'no access'

    scopus = []
    SIZE = 60
    with open('db/scopus.json', encoding='utf-8') as file:
        scop = json.load(file)
    for i in scop:
        if i['name'] == scientist.name:
            for j in i['publications']:
                artic_name = j['title']
                if len(artic_name) > SIZE:
                    artic_name = artic_name[:SIZE].strip() + '...'

                scopus.append([artic_name, j['journal'], j['meta'], j['citations'],
                               [[l['name'], l['url']] for l in j['coauthors']]])

    return render_template('scientist_info.html', scientist=info, google_articles=google_scholar,
                           publon_articles=publon, photo=photo, univer_id=scientist.univer_id,
                           depart_id=scientist.department_id, scopus_articles=scopus, graph=graph, stat_info=stat_info,
                           keywords_cloud=get_word_cloud_picture(get_keyword_frequency_for_scientist(scientist_id)))


if __name__ == '__main__':
    app.run()
