import functools

from flask import (Blueprint, g, render_template, redirect, request, url_for, send_file)
from io import BytesIO
import json

from database import DataBase
from data.blueprints_user import login_required
from data.time import Time
from data.testing import TestingSubmissions
from data.overview_data import OverviewData
from data.file_handler import FileHandler

bp = Blueprint("competition", __name__)
testing_thread = TestingSubmissions()
testing_thread.run()


@bp.before_app_request
def load_competition():
    g.competition = None


def competition_required(func):

    @functools.wraps(func)
    def wrapped_func(competition_id):
        if g.competition is None or g.competiton.id != competition_id:
            g.competition = DataBase.get_competition_by_id(competition_id)
        _check_competition_finished(g.competition)
        return func()

    return wrapped_func


def _recheck_competition(competition_id):
    DataBase.reset_all_scores_to_submissions(competition_id)
    testing_thread.run()


def _check_competition_finished(competition):
    if not competition.is_finished and competition.period < Time.get_current_date():
        DataBase.finish_competition(competition)
        _recheck_competition(competition.id)


@bp.route("/")
def index():
    return render_template("main.html", title="Главная")


@bp.route("/competitions_list")
@login_required
def competitions_list():
    competitions = list(DataBase.get_competitions())
    return render_template("competitions_list.html", competitions=competitions,  title="Соревнования")


@bp.route("/create_competition", methods=['GET', 'POST'])
@login_required
def create_competition():
    if request.method == "POST":
        competition_id = DataBase.add_new_competition(request.form['title'],
                                                      request.form['description'].replace("\r\n", "<br>"),
                                                      DataBase.get_competition_type_by_title(request.form['type']).id,
                                                      DataBase.get_metric_by_title(request.form['metric']).id,
                                                      Time.get_date_after_days(int(request.form['period'])),
                                                      int(request.form['attempts']))

        FileHandler.create_competition_files_folder(competition_id, request.files['train_file'],
                                                    request.files['test_file'], request.files['solution_file'])

        return redirect(url_for("competition.competitions_list"))

    metrics = dict()
    for competition_type in DataBase.get_competition_types():
        metrics[competition_type.name] = [m.name for m in DataBase.get_metrics(competition_type)]
    return render_template("create_competition.html", metrics=json.dumps(metrics), title="Создание соревнования")\
        if g.user.is_organizer else redirect(url_for("competition.competitions_list"))


@bp.route("/delete_competition/<competition_id>")
@login_required
@competition_required
def delete_competition():
    if g.user.is_organizer:
        DataBase.delete_competition(g.competition.id)
        return redirect(url_for("competition.competitions_list"))
    return 0


@bp.route("/overview_competition/<competition_id>")
@login_required
@competition_required
def overview_competition():
    return render_template("overview_competition.html", competition=g.competition, db=DataBase, title="О соревновании")


@bp.route("/send_submission/<competition_id>", methods=['GET', 'POST'])
@login_required
@competition_required
def send_submission():
    attempts = g.competition.attempts - DataBase.get_number_of_today_submissions(g.user.id, g.competition.id)
    if request.method == "POST" and attempts > 0:
        submission_id = DataBase.add_new_submission(g.user.id, g.competition.id, request.form['description'])
        FileHandler.create_submission_file(submission_id, request.files['submission_file'])
        testing_thread.run()
        return redirect(url_for("competition.all_submissions", attempts=attempts, competition_id=g.competition.id))

    return render_template("send_submission.html", competition=g.competition,
                           attempts=attempts, title="Отправить решение")


@bp.route("/all_submissions/<competition_id>")
@login_required
@competition_required
def all_submissions():
    solutions = DataBase.get_all_submissions(g.competition, g.user)
    return render_template("all_submissions.html", competition=g.competition, solutions=solutions, title="Все решения")


@bp.route("/leaderboard/<competition_id>")
@login_required
@competition_required
def leaderboard():
    if not g.competition.is_finished:
        table = DataBase.get_leaderboard_by_submissions(g.competition.id, False)
        return render_template("leaderboard.html", leaderboard=table, competition=g.competition, title="Таблица лидеров")
    return redirect(url_for("competition.results", competition_id=g.competition.id))


@bp.route("/results/<competition_id>")
@login_required
@competition_required
def results():
    if g.user.is_organizer or g.competition.is_finished:
        table = DataBase.get_leaderboard_by_submissions(g.competition.id, True)
        return render_template("leaderboard.html", leaderboard=table, competition=g.competition, title="Результаты")
    return redirect(url_for("competition.leaderboard", competition_id=g.competition.id))


@bp.route("/describe_data/<competition_id>")
@competition_required
def describe_data():
    return render_template("describe_data.html", competition=g.competition, title="Описание данных",
                           data_head=OverviewData.get_head_data(g.competition.id),
                           described_data=OverviewData.get_described_data(g.competition.id))


@bp.route("/recheck/<competition_id>")
@competition_required
def recheck():
    _recheck_competition(g.competition.id)
    return redirect(url_for("competition.all_submissions", competition_id=g.competition.id))


@bp.route('/download/<competition_id>/<file_name>')
def download_competition_file(competition_id, file_name):
    if g.user.is_organizer or file_name in ("train", "test"):
        if file_name == "train":  file_path = FileHandler.get_competition_train_file_path(competition_id)
        elif file_name == "test": file_path = FileHandler.get_competition_test_file_path(competition_id)
        else:                     file_path = FileHandler.get_competition_submission_file_path(competition_id)

        return download(file_path, file_name + "_" + str(competition_id) + ".csv")
    return 0


@bp.route('/download/submission/<submission_id>')
def download_submission_file(submission_id):
    if g.user.id == DataBase.get_submission_by_id(submission_id).author or g.user.is_organizer:
        file_path = FileHandler.get_competition_submission_file_path(submission_id)
        return download(file_path, "submission_" + str(submission_id) + ".csv")
    return 0


def download(file_path, file_name):
    with open(file_path, 'rb') as f:
        file_data = BytesIO(f.read())
    return send_file(file_data, download_name=file_name, as_attachment=True)
