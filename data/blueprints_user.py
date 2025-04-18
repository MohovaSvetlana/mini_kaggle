import functools
from flask import (Blueprint, session, g,
                   render_template, redirect, request, url_for)

from database import DataBase
from .forms import LoginForm, RegisterForm


bp = Blueprint("user", __name__)


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('competition.index', title='Главная'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = DataBase.get_user_by_id(user_id)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if not g.user.is_organizer:
        return redirect(url_for("competition.competitions_list"))

    form = RegisterForm()
    message = ''
    if request.method == "POST":
        if DataBase.get_user_by_login(form.login.data):
            return render_template('registration.html', title="Регистрация", form=form,
                                   message="Этот логин уже используется")
        DataBase.add_new_user(form.login.data, form.password.data, form.is_organizer.data)
        message = f"Пользователь {form.login.data} успешно зарегистрирован"

    return render_template('registration.html', title="Регистрация", form=form, message=message)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = DataBase().get_user_by_login(form.login.data)

        if DataBase.check_log_in(user, form.password.data):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for('competition.competitions_list'))

        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('competition.index'))
