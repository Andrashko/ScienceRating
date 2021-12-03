import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class Kaz_Universities(SqlAlchemyBase):
    __tablename__ = 'Kaz_Universities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    univername = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=False)
