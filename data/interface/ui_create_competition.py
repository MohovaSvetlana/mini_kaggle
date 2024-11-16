from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, \
    QComboBox, QLineEdit
from data.interface.ui_pages_bar import PagesBar


class UICreateCompetition(PagesBar):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.create_competition_layout = QVBoxLayout()
        self.competition_title_le = QLineEdit("Название соревнования")
        self.describe_comptition_te = QTextEdit("Описание соревнования")
        self.choose_period = QLineEdit("Период в днях")
        self.choose_attempts = QLineEdit("Попыток в день")
        self.choose_type_cb = QComboBox()
        self.choose_type_cb.addItem("Регрессия")
        self.choose_type_cb.addItem("Классификация")
        self.choose_metrix_cb = QComboBox()
        self.choose_metrix_cb.addItem("Метрика 1")
        self.choose_metrix_cb.addItem("Метрика 2")
        self.add_train_data_btn = QPushButton("Добавить тренировочные данные")
        self.add_test_data_btn = QPushButton("Добавить данные для тестированипя")
        self.add_solution_btn = QPushButton("Добавить решение")
        self.create_competition_layout.addWidget(self.competition_title_le)
        self.create_competition_layout.addWidget(self.describe_comptition_te)
        self.create_competition_layout.addWidget(self.choose_period)
        self.create_competition_layout.addWidget(self.choose_attempts)
        self.create_competition_layout.addWidget(self.choose_type_cb)
        self.create_competition_layout.addWidget(self.choose_metrix_cb)
        self.create_competition_layout.addWidget(self.add_train_data_btn)
        self.create_competition_layout.addWidget(self.add_test_data_btn)
        self.create_competition_layout.addWidget(self.add_solution_btn)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addLayout(self.create_competition_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
