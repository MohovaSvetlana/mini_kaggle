from data.users import User
from data.competition_types import CompetitionTypes
from data.metrics import Metric
from data.competitions import Competition

from data.db import db_session as db
from werkzeug.security import generate_password_hash, check_password_hash


class DataBase:
    @staticmethod
    def add_new_user(login, password, is_organizer):
        if DataBase.get_user_by_login(login) is None:
            user = User()
            user.login = login
            user.password = generate_password_hash(password)
            user.is_organizer = is_organizer
            db.add(user)
            db.commit()
            return True
        else:
            return False

    @staticmethod
    def add_new_competition(title, description, competition_type, metric, period, attempts):
        competition = Competition()
        competition.title = title
        competition.description = description
        competition.type = competition_type
        competition.metric = metric
        competition.period = period
        competition.attempts = attempts
        competition.is_finished = False
        db.add(competition)
        db.commit()
        return competition.id

    def check_log_in(self, login, password):
        user = self.get_user_by_login(login)
        if user and check_password_hash(user.password, password):
            return True
        return False

    @staticmethod
    def get_user_by_login(login):
        return User.query.filter(User.login == login).first()

    @staticmethod
    def get_competition_type_by_title(title):
        return CompetitionTypes.query.filter(CompetitionTypes.name == title).first()

    @staticmethod
    def get_competition_type_by_id(competition_type_id):
        return CompetitionTypes.query.filter(CompetitionTypes.id == competition_type_id).first()

    @staticmethod
    def get_metric_by_title(title):
        return Metric.query.filter(Metric.name == title).first()

    @staticmethod
    def get_metric_by_id(metric_id):
        return Metric.query.filter(Metric.id == metric_id).first()

    @staticmethod
    def get_metrics(competition_type):
        return Metric.query.filter(Metric.competition_type == competition_type.id)

    @staticmethod
    def get_competition_types():
        return CompetitionTypes.query

    @staticmethod
    def get_competitions():
        return Competition.query

    @staticmethod
    def get_competition_by_id(competition_id):
        return Competition.query.filter(Competition.id == competition_id).first()

    @staticmethod
    def finish_competition(competition):
        competition.is_finished = True
        db.commit()
