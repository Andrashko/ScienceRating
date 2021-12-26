import sqlalchemy
from sqlalchemy import orm
from data.Standart.db_session import SqlAlchemyBase


class Ukraine_Scientists(SqlAlchemyBase):
    __tablename__ = 'Ukraine_Scientists'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    google_scholar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scopus = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    publon = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    science = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    degree = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    department_id = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey('UkraineDepartments.id'))
    univer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('Ukraine_Universities.id'))

    keywords = orm.relationship('Keywords', backref='Ukraine_Scientists')