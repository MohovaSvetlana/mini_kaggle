from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel
from data.interface.ui_competition_bars import CompetitionBars


class UIOverviewCompetition(CompetitionBars):
    def __init__(self, window, controller):
        super().__init__()
        self.window = window
        self.controller = controller

        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.overview_competition_layout = QVBoxLayout()
        self.describe_comptition_te = QTextEdit("Описание соревнования")
        self.describe_comptition_te.setEnabled(False)
        self.period_lb = QLabel("Осталось 5 дней до окончания")
        self.type_lb = QLabel("Тип соревнования")
        self.metrix_lb = QLabel("Метрика")
        self.add_train_data_btn = QPushButton("Скачать тренировочные данные")
        self.add_test_data_btn = QPushButton("Скачать данные для тестирования")
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
