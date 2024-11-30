from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
from data.interface.ui_pages_bar import PagesBar
from data.settings import Pages
from database import DataBase


class UICompetitionsList(QWidget, PagesBar):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        scroll = QScrollArea()
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        content_layout = QHBoxLayout(content_widget)

        self.competitions_layout = QVBoxLayout()
        self.competitions_buttons = []
        for competition in DataBase.get_competitions():
            btn = QPushButton(str(competition.id) + ". " + competition.title)
            btn.competition_id = competition.id
            self.competitions_buttons.append(btn)
            self.competitions_layout.addWidget(btn)
            btn.setMinimumSize(400, 40)
            btn.clicked.connect(self.choose_competition)
        self.main_layout.addLayout(self.pages_bar_layout)
        content_layout.addLayout(self.competitions_layout)
        self.main_layout.addLayout(content_layout)
        self.main_layout.addWidget(scroll)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()

    def choose_competition(self):
        self.controller.change_page(Pages.overview_competition_page, self.sender().competition_id)
