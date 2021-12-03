import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class UkraineFaculties(SqlAlchemyBase):
    __tablename__ = 'UkraineFaculties'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    faculty_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    departments = orm.relationship('UkraineDepartments', backref='faculty')
    univer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('Ukraine_Universities.id'))
