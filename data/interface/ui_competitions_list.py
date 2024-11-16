from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
from data.interface.ui_pages_bar import PagesBar
from data.settings import Pages


class UICompetitionsList(PagesBar):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.competitions_list = []
        for num in range(100):
            self.competitions_list.append(f"Cоревнование {num}")

        scroll = QScrollArea()
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        content_layout = QHBoxLayout(content_widget)

        self.competitions_layout = QVBoxLayout()
        self.competitions_buttons = []
        for competition in self.competitions_list:
            self.competitions_buttons.append(QPushButton(competition))
            self.competitions_layout.addWidget(self.competitions_buttons[-1])
            self.competitions_buttons[-1].setMinimumSize(400, 40)
            self.competitions_buttons[-1].clicked.connect(lambda:
                                                          self.controller.change_page(Pages.overview_competition_page))
        self.main_layout.addLayout(self.pages_bar_layout)
        content_layout.addLayout(self.competitions_layout)
        self.main_layout.addLayout(content_layout)
        self.main_layout.addWidget(scroll)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
