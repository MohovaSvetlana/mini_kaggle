import functools

from flask import (Blueprint, session, g, render_template, redirect, request, url_for, send_file)
from io import BytesIO
import json
import os

from database import DataBase
from data.blueprints_user import login_required
from data.time import Time
from data.testing import TestingSubmissions


bp = Blueprint("competition", __name__)
testing_thread = TestingSubmissions()
testing_thread.run()


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
        id_competition = DataBase.add_new_competition(request.form['title'],
                                                      request.form['description'].replace("\r\n", "<br>"),
                                                      DataBase.get_competition_type_by_title(request.form['type']).id,
                                                      DataBase.get_metric_by_title(request.form['metric']).id,
                                                      Time.get_date_after_days(int(request.form['period'])),
                                                      int(request.form['attempts']))

        dst = os.path.join(os.getcwd(), "db", "competitions", str(id_competition))
        os.mkdir(dst)
        request.files['train_file'].save(os.path.join(dst, "train.csv"))
        request.files['test_file'].save(os.path.join(dst, "test.csv"))
        request.files['solution_file'].save(os.path.join(dst, "solution.csv"))
        return redirect(url_for("competition.competitions_list"))

    metrics = dict()
    for competition_type in DataBase.get_competition_types():
        metrics[competition_type.name] = [m.name for m in DataBase.get_metrics(competition_type)]
    return render_template("create_competition.html", metrics=json.dumps(metrics), title="Создание соревнования")\
        if g.user.is_organizer else redirect(url_for("competition.competitions_list"))


@bp.before_app_request
def load_competition():
    g.competition = None


def competition_required(func):

    @functools.wraps(func)
    def wrapped_func(competition_id):
        if g.competition is None or g.competiton.id != competition_id:
            g.competition = DataBase.get_competition_by_id(competition_id)
        check_competition_finished(g.competition)
        return func()

    return wrapped_func


def check_competition_finished(competition):
    if not competition.is_finished and competition.period < Time.get_current_date():
        DataBase.finish_competition(competition)
        DataBase.reset_all_scores_to_submissions(competition.id)
        testing_thread.run()


@bp.route("/overview_competition/<competition_id>")
@login_required
@competition_required
def overview_competition():
    return render_template("overview_competition.html", competition=g.competition, db=DataBase, title="О соревновании")


@bp.route("/send_submission/<competition_id>", methods=['GET', 'POST'])
@login_required
@competition_required
def send_submission():

    if request.method == "POST":
        id_submission = DataBase.add_new_submission(g.user.id, g.competition.id, request.form['description'])
        dst = os.path.join(os.getcwd(), "db", "submissions", f"submission{id_submission}.csv")
        request.files['submission_file'].save(dst)
        testing_thread.run()
        return redirect(url_for("competition.all_submissions", competition_id=g.competition.id))

    return render_template("send_submission.html", competition=g.competition, title="Отправить решение")


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


@bp.route('/download/<competition_id>/<file_name>')
def download_competition_file(competition_id, file_name):
    if g.user.is_organizer or file_name in ("train", "test"):
        file_path = os.path.join(os.getcwd(), "db", "competitions", str(competition_id), f"{file_name}.csv")
        file_name += "_" + str(competition_id) + ".csv"
        return download(file_path, file_name)
    return 0


@bp.route('/download/submission/<submission_id>')
def download_submission_file(submission_id):
    if g.user.id == DataBase.get_submission_by_id(submission_id).author or g.user.is_organizer:
        file_path = os.path.join(os.getcwd(), "db", "submissions", f"submission{submission_id}.csv")
        return download(file_path, "submission_" + str(submission_id) + ".csv")
    return 0


def download(file_path, file_name):
    with open(file_path, 'rb') as f:
        file_data = BytesIO(f.read())
    return send_file(file_data, download_name=file_name, as_attachment=True)
