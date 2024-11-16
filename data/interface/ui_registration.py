from PySide6.QtWidgets import QWidget, QLineEdit, \
                               QVBoxLayout, QPushButton, QRadioButton, QLabel
from data.settings import Pages
from database import DataBase


class UIRegistration:
    def __init__(self, window, controller):

        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.login_le = QLineEdit("Введите имя")
        self.password_le = QLineEdit("Введите пароль")
        self.is_organizer_rb = QRadioButton("Сделать организатором")
        self.info_lb = QLabel()
        self.info_lb.setMaximumHeight(25)
        self.registration_btn = QPushButton("Зарегистрировать пользователя")
        self.registration_btn.clicked.connect(self.register)
        self.registration_btn.setMinimumHeight(50)
        self.back_btn = QPushButton("Вернуться")
        self.back_btn.clicked.connect(lambda: self.controller.change_page(Pages.competitions_list_page))

        self.main_layout.addWidget(self.login_le)
        self.main_layout.addWidget(self.password_le)
        self.main_layout.addWidget(self.is_organizer_rb)
        self.main_layout.addWidget(self.info_lb)
        self.main_layout.addWidget(self.registration_btn)
        self.main_layout.addWidget(self.back_btn)

    def register(self):
        name = self.login_le.text()
        password = self.password_le.text()
        is_organizer = self.is_organizer_rb.isChecked()
        if DataBase.add_new_user(name, password, is_organizer):
            self.info_lb.setText(f"Пользователь {name} добавлен")
        else:
            self.info_lb.setText(f"Пользователь с именем {name} уже существует")
