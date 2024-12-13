from PySide6.QtWidgets import QVBoxLayout, QPushButton

from data.settings import Pages
from data.interface.ui_pages_bar import PagesBar


class CompetitionBars(PagesBar):
    def __init__(self):
        self.toolbar_layout = QVBoxLayout()
        self.overview_competition_btn = QPushButton("О соревновании")
        self.overview_competition_btn.clicked.connect(lambda:
                                                      self.controller.change_page(Pages.overview_competition_page))
        self.send_solution_btn = QPushButton("Отправить решение")
        self.send_solution_btn.clicked.connect(lambda: self.controller.change_page(Pages.send_submission_page))
        self.all_solutions_btn = QPushButton("Все решения")
        self.all_solutions_btn.clicked.connect(lambda: self.controller.change_page(Pages.all_submissions_page))
        self.validation_leaderboard_btn = QPushButton("Таблица лидеров")
        self.validation_leaderboard_btn.clicked.connect(lambda: self.controller.change_page(Pages.leaderboard_page))
        self.test_leaderboard_btn = QPushButton("Результаты")
        self.test_leaderboard_btn.clicked.connect(lambda: self.controller.change_page(Pages.results_page))

        self.toolbar_layout.addWidget(self.overview_competition_btn)
        self.toolbar_layout.addWidget(self.send_solution_btn)
        self.toolbar_layout.addWidget(self.all_solutions_btn)
        self.toolbar_layout.addWidget(self.validation_leaderboard_btn)
        self.toolbar_layout.addWidget(self.test_leaderboard_btn)
        super().__init__()
        self.hide_buttons_for_organizer()

    def hide_buttons_for_organizer(self):
        PagesBar.hide_buttons_for_organizer(self)
        self.test_leaderboard_btn.hide()

    def show_buttons_for_organizer(self):
        PagesBar.show_buttons_for_organizer(self)
        self.test_leaderboard_btn.show()

    def change_buttons_for_finished_competition(self):
        self.validation_leaderboard_btn.hide()
        self.test_leaderboard_btn.show()
