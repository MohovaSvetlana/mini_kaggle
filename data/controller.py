from PySide6.QtWidgets import QMainWindow

from data.interface.ui_log_in import UILogIn
from data.interface.ui_registration import UIRegistration
from data.interface.ui_competitions_list import UICompetitionsList
from data.interface.ui_create_competition import UICreateCompetition
from data.interface.ui_overview_competition import UIOverviewCompetition
from data.interface.ui_send_solution import UISendSolution
from data.interface.ui_leaderboard import UILeaderboard
from data.interface.ui_all_solutions import UIAllSolutions

from data.settings import Pages, W, H
from database import DataBase


class Controller:
    def __init__(self):
        self.database = DataBase()
        self.user = self.database.get_user_by_login("Организатор")

        self.window = QMainWindow()
        self.window.setWindowTitle("Mini-kaggle")
        self.window.setMinimumSize(W, H)
        self.interface = UICompetitionsList(self.window, self)
        self.window.show()

    def change_page(self, page):
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
