import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class UkraineDepartments(SqlAlchemyBase):
    __tablename__ = 'UkraineDepartments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    department_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    faculty_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('UkraineFaculties.id'))
    scientists = orm.relationship('Ukraine_Scientists', backref='department')
