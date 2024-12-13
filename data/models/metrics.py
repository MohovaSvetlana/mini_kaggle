import sqlalchemy
from data.db import Base


class Metric(Base):

    __tablename__ = 'metrics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    competition_type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('competition types.id'))
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
