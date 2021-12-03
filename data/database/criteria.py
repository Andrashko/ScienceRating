import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class Criterias(SqlAlchemyBase):
    __tablename__ = 'Criterias'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    measurement = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    purpose = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    operatorr = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    items_and_criteria = orm.relationship('ItemsAndCriteria', backref="criteria")
