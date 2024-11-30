from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from data.interface.ui_log_in import UILogIn
from data.interface.ui_registration import UIRegistration
from data.interface.ui_competitions_list import UICompetitionsList
from data.interface.ui_create_competition import UICreateCompetition
from data.interface.ui_overview_competition import UIOverviewCompetition
from data.interface.ui_send_solution import UISendSolution
from data.interface.ui_leaderboard import UILeaderboard
from data.interface.ui_all_solutions import UIAllSolutions

from data.settings import Pages, W, H
from data.file_handler import FileHandler
from database import DataBase
from data.time import Time


class Controller:
    def __init__(self):
        self.database = DataBase()
        self.user = self.database.get_user_by_login("Организатор")
        self.competition = None

        self.window = QMainWindow()
        self.window.setWindowTitle("Mini-kaggle")
        self.window.setWindowIcon(QIcon("static/images/icon.png"))
        self.window.setMinimumSize(W, H)
        self.interface = UICompetitionsList(self.window, self)
        self.window.show()

    def change_page(self, page, *args):
        self.interface.controller = None
        if page == Pages.log_in_page:
            self.interface = UILogIn(self.window, self)
        elif page == Pages.registration_page:
            self.interface = UIRegistration(self.window, self)
        elif page == Pages.competitions_list_page:
            self.interface = UICompetitionsList(self.window, self)
        elif page == Pages.create_competition_page:
            self.interface = UICreateCompetition(self.window, self)
        elif page == Pages.overview_competition_page:
            if len(args) > 0:
                self.process_competition(args[0])
            self.interface = UIOverviewCompetition(self.window, self)
        elif page == Pages.send_solution_page:
            self.interface = UISendSolution(self.window, self)
        elif page == Pages.all_solutions_page:
            self.interface = UIAllSolutions(self.window, self)
        elif page == Pages.leaderboard_page:
            self.interface = UILeaderboard(self.window, self)

    def log_in(self, login, password):
        if self.database.check_log_in(login, password):
            self.user = self.database.get_user_by_login(login)
            self.change_page(Pages.competitions_list_page)
        else:
            self.interface.show_error()

    def sign_out(self):
        self.user = None
        self.change_page(Pages.log_in_page)

    def download_competition_file(self, file_name):
        FileHandler().download_competition_file(file_name, self.competition.id)

    @staticmethod
    def create_competition(train_file_name, test_file_name, solution_file_name,
                           title, description, competition_type, metric, period, attempts):
        if (FileHandler.check_file(train_file_name) and FileHandler.check_file(test_file_name)
                and FileHandler.check_file(solution_file_name)):

            competition_id = DataBase.add_new_competition(title, description, competition_type.id,
                                                          metric.id, period, attempts)
            FileHandler.create_competition_files_folder(competition_id,
                                                        train_file_name, test_file_name, solution_file_name)
            return True
        else:
            return False

    def process_competition(self, competition_id):
        self.competition = DataBase.get_competition_by_id(competition_id)
        self.check_competition_finished(self.competition)

    def check_competition_finished(self, competition):
        if not self.competition.is_finished and Time().compare_dates(competition.period) < 0:
            # retest solutions
            DataBase.finish_competition(competition)
