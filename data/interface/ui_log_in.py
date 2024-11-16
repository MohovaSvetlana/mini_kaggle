from PySide6.QtWidgets import QWidget, QLineEdit, \
                               QVBoxLayout, QPushButton, QLabel


class UILogIn:
    def __init__(self, window, controller):

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.controller = controller

        self.login_le = QLineEdit("Введите имя")
        self.password_le = QLineEdit("Введите пароль")
        self.log_in_btn = QPushButton("Войти")
        self.log_in_btn.setMinimumHeight(50)
        self.log_in_btn.clicked.connect(lambda: self.controller.log_in(self.login_le.text(), self.password_le.text()))
        self.error_lb = QLabel("Неправильный логин или пароль")
        self.error_lb.setMaximumHeight(20)
        self.error_lb.hide()

        self.main_layout.addWidget(self.login_le)
        self.main_layout.addWidget(self.password_le)
        self.main_layout.addWidget(self.error_lb)
        self.main_layout.addWidget(self.log_in_btn)

    def show_error(self):
        self.error_lb.show()
