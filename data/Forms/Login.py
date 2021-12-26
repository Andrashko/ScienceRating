from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')
