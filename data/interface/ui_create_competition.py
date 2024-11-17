import os
from PySide6.QtWidgets import QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, \
    QComboBox, QLineEdit, QFileDialog, QLabel, QSpinBox, QDateEdit

from data.interface.ui_pages_bar import PagesBar
from data.time import Time
from database import DataBase


class UICreateCompetition(PagesBar):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller
        self.competition_type = None
        self.metric = None
        self.train_file_name = None
        self.test_file_name = None
        self.solution_file_name = None

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.create_competition_layout = QVBoxLayout()
        self.competition_title_le = QLineEdit("Название соревнования")
        self.describe_comptition_te = QTextEdit("Описание соревнования")

        self.period_layout = QHBoxLayout()
        self.period_lb = QLabel("Период в днях")
        self.period_lb.setMaximumWidth(100)
        self.choose_period = QSpinBox()
        self.choose_period.valueChanged.connect(self.update_period_date)
        self.choose_period.setMaximum(1000000)
        self.period_de = QDateEdit(Time.to_pyside_date(Time.get_current_date()))
        self.period_de.setMinimumDate(Time.to_pyside_date(Time.get_current_date()))
        self.period_de.setEnabled(False)

        self.attempts_layout = QHBoxLayout()
        self.attempts_lb = QLabel("Попыток в день")
        self.attempts_lb.setMaximumWidth(100)
        self.choose_attempts = QSpinBox()
        self.choose_attempts.setMinimum(1)
        self.choose_attempts.setMaximum(1000000)

        self.choose_type_cb = QComboBox()
        self.add_competition_types()
        self.choose_type_cb.currentTextChanged.connect(self.change_metrics)

        self.choose_metrics_cb = QComboBox()
        self.choose_metrics_cb.currentTextChanged.connect(self.change_metric)
        self.change_metrics()

        self.train_data_layout = QHBoxLayout()
        self.add_train_data_btn = QPushButton("Добавить тренировочные данные")
        self.add_train_data_btn.clicked.connect(self.load_train_file)
        self.train_file_lb = QLabel()
        self.test_data_layout = QHBoxLayout()
        self.add_test_data_btn = QPushButton("Добавить данные для тестированипя")
        self.add_test_data_btn.clicked.connect(self.load_test_file)
        self.test_file_lb = QLabel()
        self.solution_data_layout = QHBoxLayout()
        self.add_solution_btn = QPushButton("Добавить решение")
        self.add_solution_btn.clicked.connect(self.load_solution_file)
        self.solution_file_lb = QLabel()

        self.create_competition_btn = QPushButton("Создать соревнование")
        self.create_competition_btn.clicked.connect(self.create_competition)

        self.period_layout.addWidget(self.period_lb)
        self.period_layout.addWidget(self.choose_period)
        self.period_layout.addWidget(self.period_de)

        self.attempts_layout.addWidget(self.attempts_lb)
        self.attempts_layout.addWidget(self.choose_attempts)

        self.train_data_layout.addWidget(self.add_train_data_btn)
        self.train_data_layout.addWidget(self.train_file_lb)
        self.test_data_layout.addWidget(self.add_test_data_btn)
        self.test_data_layout.addWidget(self.test_file_lb)
        self.solution_data_layout.addWidget(self.add_solution_btn)
        self.solution_data_layout.addWidget(self.solution_file_lb)

        self.create_competition_layout.addWidget(self.competition_title_le)
        self.create_competition_layout.addWidget(self.describe_comptition_te)
        self.create_competition_layout.addLayout(self.period_layout)
        self.create_competition_layout.addLayout(self.attempts_layout)
        self.create_competition_layout.addWidget(self.choose_type_cb)
        self.create_competition_layout.addWidget(self.choose_metrics_cb)
        self.create_competition_layout.addLayout(self.train_data_layout)
        self.create_competition_layout.addLayout(self.test_data_layout)
        self.create_competition_layout.addLayout(self.solution_data_layout)
        self.create_competition_layout.addWidget(self.create_competition_btn)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addLayout(self.create_competition_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()

    def load_train_file(self):
        file_name = self.load_file("Выберете файл для тренировки моделей")
        self.train_file_name = file_name if file_name != "" else None
        if self.train_file_name:
            self.train_file_lb.setText(os.path.split(self.train_file_name)[-1])

    def load_test_file(self):
        file_name = self.load_file("Выберете файл для тестирования")
        self.test_file_name = file_name if file_name else None
        if self.test_file_name:
            self.test_file_lb.setText(os.path.split(self.test_file_name)[-1])

    def load_solution_file(self):
        file_name = self.load_file("Выберете файл с решением")
        self.solution_file_name = file_name if file_name else None
        if self.solution_file_name:
            self.solution_file_lb.setText(os.path.split(self.solution_file_name)[-1])

    def load_file(self, massage="выберете файл"):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        name_file = QFileDialog. \
            getOpenFileName(self.window, massage, desktop, "*.csv")[0]
        return name_file

    def update_period_date(self):
        date = Time.to_pyside_date(Time.get_date_after_days(int(self.choose_period.text())))
        self.period_de.setDate(date)

    def add_competition_types(self):
        for type in DataBase.get_competition_types():
            self.choose_type_cb.addItem(type.name)

    def change_metrics(self):
        self.choose_metrics_cb.clear()
        self.competition_type = DataBase.get_competition_type_by_title(self.choose_type_cb.currentText())

        for metric in DataBase.get_metrics(self.competition_type):
            self.choose_metrics_cb.addItem(metric.name)

    def change_metric(self):
        self.metric = DataBase.get_metric_by_title(self.choose_metrics_cb.currentText())

    def create_competition(self):
        if self.train_file_name and self.test_file_name and self.solution_file_name:
            print("Создать соревнование")
            print(f"Hазвание: {self.competition_title_le.text()}")
            print("Условие:")
            print(self.describe_comptition_te.toPlainText())
            print(f"Тип соревнования: {self.competition_type.name}")
            print(f"Метрика: {self.metric.name}")
            print(f"Длительность: {self.choose_period.text()}")
            print(f"Количество попыток: {self.choose_attempts.text()}")
            print(f"Файлы для соревнования: {self.train_file_name}, {self.test_file_name}, {self.solution_file_name}")
        else:
            print("Файлы не выбраны")
