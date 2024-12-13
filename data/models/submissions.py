import sqlalchemy

from data.db import Base


class Submission(Base):

    __tablename__ = 'submissions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    competition = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('competitions.id'))
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    date = sqlalchemy.Column(sqlalchemy.Date)
    validation_score = sqlalchemy.Column(sqlalchemy.Float)
    test_score = sqlalchemy.Column(sqlalchemy.Float)
    is_checked = sqlalchemy.Column(sqlalchemy.Boolean)
