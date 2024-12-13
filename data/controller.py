from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from data.interface.ui_log_in import UILogIn
from data.interface.ui_registration import UIRegistration
from data.interface.ui_competitions_list import UICompetitionsList
from data.interface.ui_create_competition import UICreateCompetition
from data.interface.ui_overview_competition import UIOverviewCompetition
from data.interface.ui_send_submission import UISendSubmission
from data.interface.ui_leaderboard import UILeaderboard
from data.interface.ui_all_submissions import UIAllSubmissions

from data.settings import Pages, W, H
from data.file_handler import FileHandler
from data.testing import TestingSolutions
from database import DataBase
from data.time import Time


class Controller:
    def __init__(self):
        self.database = DataBase()
        self.testing_thread = TestingSolutions()
        self.testing_thread.start()
        self.user = None
        self.competition = None

        self.window = QMainWindow()
        self.window.setWindowTitle("Mini-kaggle")
        self.window.setWindowIcon(QIcon("static/images/icon.png"))
        self.window.setMinimumSize(W, H)
        self.interface = UILogIn(self.window, self)
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
        elif page == Pages.send_submission_page:
            self.interface = UISendSubmission(self.window, self)
        elif page == Pages.all_submissions_page:
            self.interface = UIAllSubmissions(self.window, self)
        elif page == Pages.leaderboard_page:
            self.interface = UILeaderboard(self.window, self)
        elif page == Pages.results_page:
            self.interface = UILeaderboard(self.window, self, is_results=True)

    def log_in(self, login, password):
        if self.database.check_log_in(login, password):
            self.user = self.database.get_user_by_login(login)
            self.change_page(Pages.competitions_list_page)
        else:
            self.interface.show_error()

    def sign_out(self):
        self.user = None
        self.change_page(Pages.log_in_page)

    @staticmethod
    def download_submission(submission_id):
        FileHandler().download_submission_file(submission_id)

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
        if not self.competition.is_finished and competition.period < Time.get_current_date():
            DataBase.finish_competition(competition)
            DataBase.reset_all_scores_to_submissions(competition.id)
            self.testing_thread.run()

    def send_submission(self, submission_file_name, description):
        if FileHandler.check_file(submission_file_name) and self.get_today_attempts() > 0:
            id_submission = DataBase.add_new_submission(self.user.id, self.competition.id, description)
            FileHandler.create_submission_file(id_submission, submission_file_name)
            self.testing_thread.run()
            return True
        else:
            return False

    def get_today_attempts(self):
        return self.competition.attempts - DataBase.get_number_of_today_submissions(self.user.id, self.competition.id)
