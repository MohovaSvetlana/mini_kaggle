from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit

from data.interface.ui_competition_bars import CompetitionBars


class UISendSolution(CompetitionBars):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.sending_layout = QVBoxLayout()
        self.choose_solution_btn = QPushButton("Выберите файл")
        self.description_le = QLineEdit("Описание решения")
        self.sending_btn = QPushButton("Отослать решение")
        self.attempts_lb = QLabel(f"Осталось попыток: {self.controller.competition.attempts}")
        self.attempts_lb.setMaximumHeight(25)
        self.sending_layout.addWidget(self.choose_solution_btn)
        self.sending_layout.addWidget(self.description_le)
        self.sending_layout.addWidget(self.sending_btn)
        self.sending_layout.addWidget(self.attempts_lb)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addLayout(self.sending_layout)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
        if self.controller.competition.is_finished:
            self.change_buttons_for_finished_competition()
