from flask import Blueprint, g, render_template, request
from io import BytesIO
import base64
from data.overview_data import OverviewData
from data.blueprints_competiton import competition_required

bp = Blueprint("plots", __name__)


@bp.route("/generate_line_chart/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_line_chart():
    data = None
    if request.method == "POST":
        columns = [*request.form.keys()][1:]
        if request.form['index'] in request.form:
            columns.remove(request.form['index'])
        data = OverviewData.line_chart(g.competition.id, request.form['index'], columns)

    return render_plots(data, page="plots/generate_line_chart.html")


@bp.route("/generate_scatterplot/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_scatterplot():
    data = None
    if request.method == "POST":
        if "regline" in request.form:
            data = OverviewData.reg_plot(g.competition.id, request.form['x'], request.form['y'],
                                         request.form['hue'] if 'hue' in request.form else None)
        else:
            data = OverviewData.scatterplot(g.competition.id, request.form['x'], request.form['y'],
                                            request.form['hue'] if 'hue' in request.form else None)

    return render_plots(data, page="plots/generate_scatterplot.html")


@bp.route("/generate_bar_chart/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_bar_chart():
    data = None
    if request.method == "POST":
        data = OverviewData.bar_chart(g.competition.id, request.form['x'], request.form['y'])

    return render_plots(data, page="plots/generate_bar_chart.html")


@bp.route("/generate_heatmaps/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_heatmaps():
    data = None
    if request.method == "POST":
        val = [*request.form.keys()]
        index = OverviewData.get_columns_data(g.competition.id)[0]
        if len(val) > 2 or len(val) == 1 and val[0] != 'annot':
            if val[-1] == 'annot':
                data = OverviewData.heatmaps(g.competition.id, val[:-1], index, True)
            else:
                data = OverviewData.heatmaps(g.competition.id, val, index, False)

    return render_plots(data, page="plots/generate_heatmaps.html")


@bp.route("/generate_histogram/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_histogram():
    data = None
    if request.method == "POST":
        data = OverviewData.histogram(g.competition.id, request.form['val'],
                                      request.form['hue'] if 'hue' in request.form else None)

    return render_plots(data, page="plots/generate_histogram.html")


@bp.route("/generate_density_plot/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_density_plot():
    data = None
    if request.method == "POST":
        data = OverviewData.density_plot(g.competition.id, request.form['val'],
                                         request.form['hue'] if 'hue' in request.form else None)

    return render_plots(data, page="plots/generate_density_plot.html")


@bp.route("/generate_categorical_scatterplot/<competition_id>", methods=['GET', 'POST'])
@competition_required
def generate_categorical_scatterplot():
    data = None
    if request.method == "POST":
        data = OverviewData.categorical_scatterplot(g.competition.id, request.form['x'], request.form['y'])

    return render_plots(data, page="plots/generate_categorical_scatterplot.html")


def render_plots(data: BytesIO, page):
    if data:
        data = data.read()
        data = base64.b64encode(data).decode()
        return render_template(page, competition=g.competition, title="Построение графиков",
                               plot=f'<img src="data:image/png;base64,{data}">',
                               rows=OverviewData.get_columns_data(g.competition.id))
    else:
        return render_template(page, competition=g.competition, title="Построение графиков",
                               rows=OverviewData.get_columns_data(g.competition.id))
