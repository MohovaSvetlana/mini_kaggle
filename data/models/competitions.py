import sqlalchemy

from data.db import Base


class Competition(Base):

    __tablename__ = 'competitions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=False)
    description = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('competition types.id'))
    metric = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('metrics.id'))
    period = sqlalchemy.Column(sqlalchemy.DATE)
    attempts = sqlalchemy.Column(sqlalchemy.Integer)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
