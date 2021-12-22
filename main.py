from flask import Flask, render_template, request, session, redirect
import requests
import json
from bs4 import BeautifulSoup as BS
from sqlalchemy import or_
from dotenv import load_dotenv
import threading

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
from rating import calculate_university_rating

db_session.global_init("db/database.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rating_sk'
BASE_URL="http://science-rating.co.ua" # необходимо для роботы редиректа на хостинге
# BASE_URL="" # Для роботы на локахосте

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
    return redirect(BASE_URL+'/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(BASE_URL+'/')
        return render_template('login.html', msg='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, msg='Пароли не совпадают')
        if form.login.data.isdigit():
            return render_template('register.html', form=form, msg='Логин не может состоять только из цифр')
        for i in form.login.data:
            if (not i.isdigit()) and (not i.isalpha()):
                return render_template('register.html', form=form, msg='В логине могут быть только цифры и буквы')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.user_email == form.email.data).first():
            return render_template('register.html', form=form, msg='Пользователь с этой почтой уже существует')
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', form=form, msg='Такой пользователь уже есть')
        user = User(
            login=form.login.data,
            user_email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        threading.Thread(target=send_mail, args=[form.email.data, 'Регистрация прошла успешно',
                                                 f'Ваш логин: {form.login.data}']).start()
        return redirect(BASE_URL+'/login')
    return render_template('register.html', form=form)


@app.route('/')
def universities_rating():
    db_sess = db_session.create_session()

    # scientists = []
    # for i in range(1, 33):
    #     get = db_sess.query(Ukraine_Scientists).get(i)

    #     if get.google_scholar != '-' and get.publon != '-' and get.scopus != '-':
    #         scientists.append([get.name.split(), i])

    # rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
    #     ItemsAndCriteria.criteria_id == 7)
    universities = []
    mid = []
    map_uk = {
        "ua-kc":-2000000
    }
    for university in db_sess.query(Ukraine_Universities).all():
        rating = calculate_university_rating(university) 
        if university.region in map_uk.keys():
            map_uk[university.region] += rating
        else:
            map_uk[university.region] = rating
        if len(university.univername) > 65:
            universities.append([university.univername[:65].strip() + '...', rating])
        else:
            universities.append([university.univername,rating])
        mid.append(rating)
    # for i in rating:
    #     university = db_sess.query(Ukraine_Universities).get(i.item_id)
    #     if university.region in map_uk.keys():
    #         map_uk[university.region] += int(int(i.value) * 100 / len(list(university.scientists)))
    #     else:
    #         map_uk[university.region] = int(int(i.value) * 100 / len(list(university.scientists)))

    #     try:
    #         if len(university.univername) > 65:
    #             universities.append([university.univername[:65].strip() + '...',
    #                                  int(i.value) * 100 / len(list(university.scientists)), i.item_id])
    #         else:
    #             universities.append([university.univername,
    #                                  int(i.value) * 100 / len(list(university.scientists)), i.item_id])

    #         mid.append(int(i.value) * 100 / len(list(university.scientists)))
    #     except ZeroDivisionError:
    #         pass
    universities = sorted(universities, key=lambda x: x[1], reverse=True)[:10]
    mid = '%.2f' % (sum(mid) / len(mid))

    return render_template('universities_rating.html', color_page_one='#F63E3E', univers_rating=universities,
                          map_uk=map_uk, mid=mid)


@app.route('/add_compare/<int:univer_id>')
def add_compare(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    if 'univers' not in session:
        session['univers'] = [univer_id]
    else:
        if len(session['univers']) < 5 and univer_id not in session['univers']:
            univers = session['univers']
            univers.append(univer_id)
            session['univers'] = univers

    return redirect(BASE_URL+'/universities')


@app.route('/delete_compare/<int:univer_id>')
def delete_compare(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    if 'univers' in session:
        if session['univers']:
            univers = session['univers']
            univers.pop(univers.index(univer_id))
            session['univers'] = univers

    return redirect(BASE_URL+'/universities')


@app.route('/universities')
def all_universities():
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

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

        if len(univer.univername) > 35:
            univers_js['univers'].append(univer.univername[:35].strip() + '...')
        else:
            univers_js['univers'].append(univer.univername)
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

        # rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        #     ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.item_id == i[1]).first()
        rating = calculate_university_rating(univer)
        try:
            univers_js['rating'].append(f'{rating}')
        except ZeroDivisionError:
            univers_js['rating'].append('0')
        except AttributeError:
            univers_js['rating'].append('0')

    for i in range(len(univers_compare)):
        if len(univers_compare[i][0]) > 50:
            univers_compare[i][0] = univers_compare[i][0][:50].strip() + '...'

    universities = sorted([[i.univername, i.id] for i in db_sess.query(Ukraine_Universities)], key=lambda x: x[0])

    return render_template('universities.html', color_page_one='#F63E3E', univers=universities,
                           univers_compare=univers_compare, univers_js=univers_js)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()
    inp = ''
    univers = []
    scientists = []

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

    return render_template('search.html', value=inp, univers=univers, scientists=scientists)


@app.route('/university_info/<int:university_id>')
def university_info(university_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()
    university = db_sess.query(Ukraine_Universities).get(university_id)
    scientists = len(list(university.scientists))

    faculty_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'faculty').filter(
        ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == university_id)

    department_rating = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'department').filter(
        ItemsAndCriteria.criteria_id == 7).filter(ItemsAndCriteria.univer_id == university_id)

    faculties = []
    if faculty_rating:
        for i in faculty_rating:
            if (' - без факультету' not in db_sess.query(UkraineFaculties).get(i.item_id).faculty_name) and \
                    (not db_sess.query(UkraineFaculties).get(i.item_id).faculty_name.isdigit()):
                try:
                    faculties.append([db_sess.query(UkraineFaculties).get(i.item_id).faculty_name, i.item_id,
                                      int(i.value) * 100 / scientists])
                except ZeroDivisionError:
                    faculties.append([' ', -1])
        faculties = sorted(faculties, key=lambda x: x[2], reverse=True)

    departments = []
    if department_rating:
        for i in department_rating:
            try:
                departments.append([db_sess.query(UkraineDepartments).get(i.item_id).department_name, i.item_id,
                                    int(i.value) * 100 / scientists])
            except ZeroDivisionError:
                departments.append([' ', -1])
        departments = sorted(departments, key=lambda x: x[2], reverse=True)

    facult_depart = []
    facult_empty = True
    depart_empty = True
    for i in range(len(departments)):
        if not departments and not faculties:
            facult_depart = []
            break

        try:
            facult_depart.append([faculties[i][0], faculties[i][1]])
            facult_empty = False
        except IndexError:
            facult_depart.append(['', -1])

        try:
            facult_depart[i].append([departments[i][0], departments[i][1]])
            depart_empty = False
        except IndexError:
            facult_depart[i].append(' ')

    return render_template('university_info.html', facult_depart=facult_depart, univer=university,
                           facult_empty=facult_empty, depart_empty=depart_empty)


@app.route('/university_projects/<int:univer_id>')
def university_projects(univer_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()
    univer = db_sess.query(Ukraine_Universities).get(univer_id)
    return render_template('university_projects.html', univer=univer)


@app.route('/faculty_info/<int:faculty_id>')
def faculty_info(faculty_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()
    faculty = db_sess.query(UkraineFaculties).get(faculty_id)
    return render_template('faculty_info.html', faculty=faculty)


@app.route('/department_info/<int:depart_id>')
def department_info(depart_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()
    depart = db_sess.query(UkraineDepartments).get(depart_id)
    univer_id = db_sess.query(UkraineFaculties).get(depart.faculty_id).univer_id
    return render_template('department_info.html', depart=depart, univer_id=univer_id)


@app.route('/university_info_rating/<int:university_id>')
def university_info_rating(university_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

    db_sess = db_session.create_session()

    university = db_sess.query(Ukraine_Universities).get(university_id)
    scientists = len(list(university.scientists))
    # criterias = db_sess.query(Criterias).filter(or_(Criterias.number == '2.1.1.', Criterias.number == '2.1.2.',
    #                                                 Criterias.number == '2.1.3.', Criterias.number == '2.2.',
    #                                                 Criterias.number == '2.3.'))
    # criterias = db_sess.query(Criterias).all()
    values = db_sess.query(ItemsAndCriteria).filter(ItemsAndCriteria.item_type == 'university').filter(
        ItemsAndCriteria.item_id == university.id)

    criters_values = []
    for i in range(1, 200):
        criteria = db_sess.query(Criterias).get(i)
        value = values.filter(ItemsAndCriteria.criteria_id == i).first()
        if criteria and value:
           criters_values.append([criteria.name, value]) 
    # index = 0
    # for i in range(8, 13):
    #     criters_values.append([criterias[index].name, values.filter(ItemsAndCriteria.criteria_id == i).first()])
    #     index += 1

    # for i in range(1, 8):
    #     criters_values.append([db_sess.query(Criterias).get(i).name, values.filter(ItemsAndCriteria.criteria_id == i).first()])
    # for i in range(14, 54):
    #     criters_values.append([db_sess.query(Criterias).get(i).name, values.filter(ItemsAndCriteria.criteria_id == i).first()])

    return render_template('university_info_rating.html', univer=university, criters_values=criters_values,
                           rating_value=calculate_university_rating(university))


@app.route('/scientist_info/<int:scientist_id>')
def scientist_info(scientist_id):
    if not current_user.is_authenticated:
        return redirect(BASE_URL+'/login')

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
        info.append(db_sess.query(Ukraine_Universities).get(scientist.univer_id).univername)
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
    h_index = {}
    if scientist.google_scholar and (scientist.google_scholar != '-'):
        res = requests.get(scientist.google_scholar)
        html = BS(res.content, 'html.parser')

        h_index = {'years': [i.text for i in html.find_all('span', class_='gsc_g_t')],
                   'h': [i.text for i in html.find_all('span', class_='gsc_g_al')],
                   'colors': ['#F63E3E' for i in range(len(html.find_all('span', class_='gsc_g_t')))]}

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
                           depart_id=scientist.department_id, scopus_articles=scopus, h_index=h_index)


if __name__ == '__main__':
    app.run()
