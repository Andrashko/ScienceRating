import sqlalchemy
from data.Standart.db_session import SqlAlchemyBase


class ItemsAndCriteria(SqlAlchemyBase):
    __tablename__ = 'ItemsAndCriteria'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    criteria_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('Criterias.id'))
    item_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    univer_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.String, nullable=False)
