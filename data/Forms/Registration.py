from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import PasswordField, StringField, SubmitField, EmailField


class RegisterForm(FlaskForm):
    email = EmailField('Пошта', validators=[DataRequired()])
    login = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторіть пароль', validators=[DataRequired()])
    submit = SubmitField('Зареєструватись')
