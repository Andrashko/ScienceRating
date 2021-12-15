import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class UniverProjects(SqlAlchemyBase):
    __tablename__ = 'UniverProjects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    project_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    univer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('Ukraine_Universities.id'))
