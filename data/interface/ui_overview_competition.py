from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
from data.interface.ui_competition_bars import CompetitionBars
from database import DataBase


class UIOverviewCompetition(CompetitionBars):
    def __init__(self, window, controller):
        super().__init__()
        self.window = window
        self.controller = controller

        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.overview_competition_layout = QVBoxLayout()
        self.title_le = QLineEdit(self.controller.competition.title)
        self.title_le.setEnabled(False)
        self.describe_comptition_te = QTextEdit(self.controller.competition.description)
        self.describe_comptition_te.setEnabled(False)
        self.period_lb = QLabel(f"Дата окончания: {self.controller.competition.period}")
        self.type_lb = QLabel(DataBase.get_competition_type_by_id(self.controller.competition.type).name)
        self.metrix_lb = QLabel(DataBase.get_metric_by_id(self.controller.competition.metric).name)
        self.add_train_data_btn = QPushButton("Скачать тренировочные данные")
        self.add_train_data_btn.clicked.connect(lambda: self.controller.download_competition_file("train"))
        self.add_test_data_btn = QPushButton("Скачать данные для тестирования")
        self.add_test_data_btn.clicked.connect(lambda: self.controller.download_competition_file("test"))
        self.overview_competition_layout.addWidget(self.title_le)
        self.overview_competition_layout.addWidget(self.describe_comptition_te)
        self.overview_competition_layout.addWidget(self.period_lb)
        self.overview_competition_layout.addWidget(self.type_lb)
        self.overview_competition_layout.addWidget(self.metrix_lb)
        self.overview_competition_layout.addWidget(self.add_train_data_btn)
        self.overview_competition_layout.addWidget(self.add_test_data_btn)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addLayout(self.overview_competition_layout)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
        if self.controller.competition.is_finished:
            self.change_buttons_for_finished_competition()
