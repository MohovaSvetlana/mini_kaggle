import os
from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog

from data.interface.ui_competition_bars import CompetitionBars
from data.settings import Pages


class UISendSubmission(CompetitionBars):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller
        self.submission_path = None

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.sending_layout = QVBoxLayout()
        self.choose_submission_btn = QPushButton("Выберите файл")
        self.choose_submission_btn.clicked.connect(self.choose_submission)
        self.submission_name_lb = QLabel()
        self.submission_name_lb.setMaximumHeight(25)
        self.description_le = QLineEdit("Описание решения")
        self.sending_btn = QPushButton("Отправить решение")
        self.sending_btn.clicked.connect(self.send_submission)
        self.attempts_lb = QLabel(f"Осталось попыток: {self.controller.get_today_attempts()}")
        self.attempts_lb.setMaximumHeight(25)

        self.sending_layout.addWidget(self.choose_submission_btn)
        self.sending_layout.addWidget(self.description_le)
        self.sending_layout.addWidget(self.submission_name_lb)
        self.sending_layout.addWidget(self.sending_btn)
        self.sending_layout.addWidget(self.attempts_lb)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addLayout(self.sending_layout)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.get_today_attempts() <= 0:
            self.sending_btn.setEnabled(False)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
        if self.controller.competition.is_finished:
            self.change_buttons_for_finished_competition()

    def choose_submission(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.submission_path = QFileDialog. \
            getOpenFileName(self.window, "Выберите решение", desktop, "*.csv")[0]
        if self.submission_path:
            self.submission_name_lb.setText(os.path.split(self.submission_path)[-1])

    def send_submission(self):
        if self.controller.send_submission(self.submission_path, self.description_le.text()):
            self.controller.change_page(Pages.overview_competition_page)
