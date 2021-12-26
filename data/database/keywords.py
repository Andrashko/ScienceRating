import sqlalchemy
from data.Standart.db_session import SqlAlchemyBase


class Keywords(SqlAlchemyBase):
    __tablename__ = 'Keywords'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    priority = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    scientist_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('Ukraine_Scientists.id'))
    