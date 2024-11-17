import sqlalchemy
from data.db import Base


class CompetitionTypes(Base):

    __tablename__ = 'competition types'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
