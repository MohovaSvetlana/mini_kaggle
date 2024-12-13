import sqlalchemy

from data.db import Base


class User(Base):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    is_organizer = sqlalchemy.Column(sqlalchemy.Boolean)
