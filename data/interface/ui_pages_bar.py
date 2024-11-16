from PySide6.QtWidgets import QVBoxLayout, QPushButton
from data.settings import Pages


class PagesBar:
    def __init__(self):
        self.pages_bar_layout = QVBoxLayout()
        self.add_competition_btn = QPushButton("+")
        self.add_competition_btn.clicked.connect(lambda: self.controller.change_page(Pages.create_competition_page))
        self.competitions_btn = QPushButton("Соревнования")
        self.competitions_btn.clicked.connect(lambda: self.controller.change_page(Pages.competitions_list_page))
        self.add_user_btn = QPushButton("Добавить пользователя")
        self.add_user_btn.clicked.connect(lambda: self.controller.change_page(Pages.registration_page))
        self.sign_out = QPushButton("Выйти")
        self.sign_out.clicked.connect(lambda: self.controller.sign_out())
        self.pages_bar_layout.addWidget(self.add_competition_btn)
        self.pages_bar_layout.addWidget(self.competitions_btn)
        self.pages_bar_layout.addWidget(self.add_user_btn)
        self.pages_bar_layout.addWidget(self.sign_out)
        self.hide_buttons_for_organizer()

    def hide_buttons_for_organizer(self):
        self.add_competition_btn.hide()
        self.add_user_btn.hide()

    def show_buttons_for_organizer(self):
        self.add_competition_btn.show()
        self.add_user_btn.show()
