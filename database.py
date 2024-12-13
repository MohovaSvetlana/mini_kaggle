from data.models.users import User
from data.models.competition_types import CompetitionTypes
from data.models.metrics import Metric
from data.models.competitions import Competition
from data.models.submissions import Submission

from data.time import Time

from data.db import db_session as db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, func, desc


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

    @staticmethod
    def add_new_submission(user, competition, description):
        submission = Submission()
        submission.author = user
        submission.competition = competition
        submission.description = description
        submission.date = Time.get_current_date()
        submission.score = 1000000
        submission.is_checked = False
        db.add(submission)
        db.commit()
        return submission.id

    @staticmethod
    def add_new_metric(competition_type, title):
        metric = Metric()
        metric.name = title
        metric.competition_type = competition_type
        db.add(metric)
        db.commit()

    def check_log_in(self, login, password):
        user = self.get_user_by_login(login)
        if user and check_password_hash(user.password, password):
            return True
        return False

    @staticmethod
    def get_user_by_login(login):
        return User.query.filter(User.login == login).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter(User.id == user_id).first()

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
    def get_unchecked_submissions():
        return Submission.query.filter(Submission.is_checked == 0)

    @staticmethod
    def get_all_submissions(competition, user):
        data = [["Id", "Дата отправки", "Имя отправителя", "Описание решения", "Оценка"]]
        if user.is_organizer:
            data[0].append("Результат")

        for submission in Submission.query.filter(and_(Submission.competition == competition.id,
                                                  (Submission.author == user.id if not user.is_organizer else True))):
            data.append([submission.id, submission.date, DataBase.get_user_by_id(submission.author).login,
                         submission.description, submission.validation_score])
            if user.is_organizer:
                data[-1].append(submission.test_score)
        return data

    @staticmethod
    def get_number_of_today_submissions(user_id, competition_id):
        return db.query(func.count(Submission.id)).filter(
            and_(Submission.author == user_id,
                 Submission.competition == competition_id,
                 Submission.date == Time.get_current_date())).scalar()

    def get_leaderboard_by_submissions(self, competition_id, is_result):
        competition = DataBase.get_competition_by_id(competition_id)
        competition_finished_date, competition_type = competition.period, competition.type
        score = Submission.test_score if is_result else Submission.validation_score
        if competition_type == 1:
            rate_function = func.min
            order = score
        else:
            rate_function = func.max
            order = desc(score)

        submissions = Submission.query.filter(and_(Submission.competition == competition_id,
                                                   Submission.date <= competition_finished_date if is_result else True)
                                              ).subquery()
        best_score = (db.query(submissions.c.author, rate_function(
            submissions.c.test_score if is_result else submissions.c.validation_score).label('best_score')
                               ).group_by(submissions.c.author).subquery())
        best_submissions = (Submission.query.join(best_score, and_(Submission.author == best_score.c.author,
                                                                   score == best_score.c.best_score)
                                                  ).order_by(order))

        return self._get_leaderboard_data(best_submissions, is_result)

    @staticmethod
    def _get_leaderboard_data(best_submissions, is_result):
        data = [["№", "Имя отправителя", "Описание решения", "Оценка"]]
        repeats = 0
        for num, submission in enumerate(best_submissions, start=1):
            user_login = DataBase.get_user_by_id(submission.author).login
            if data[-1][1] == user_login:
                repeats += 1
            else:
                data.append([num - repeats, user_login, submission.description,
                             submission.test_score if is_result else submission.validation_score])
        return data

    @staticmethod
    def set_score_to_submission(submission, score):
        submission.validation_score = score[0]
        submission.test_score = score[1]
        submission.is_checked = True
        db.commit()

    @staticmethod
    def finish_competition(competition):
        competition.is_finished = True
        db.commit()

    @staticmethod
    def reset_all_scores_to_submissions(competition_id):
        for submission in Submission.query.filter(Submission.competition == competition_id):
            submission.validation_score = None
            submission.test_score = None
            submission.is_checked = False
        db.commit()
