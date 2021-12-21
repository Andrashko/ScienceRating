import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class Ukraine_Universities(SqlAlchemyBase):
    __tablename__ = 'Ukraine_Universities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    univername = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    students_bak = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    students_mag = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    faculties = orm.relationship('UkraineFaculties', backref='univer')
    scientists = orm.relationship('Ukraine_Scientists', backref='univer')
    projects = orm.relationship('UniverProjects', backref='univer')
