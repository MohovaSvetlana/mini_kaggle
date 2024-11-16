from PySide6.QtWidgets import QWidget, \
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QPushButton
from random import randint, random
from data.interface.ui_competition_bars import CompetitionBars
from PySide6.QtCore import Qt


class UIAllSolutions(CompetitionBars):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.solutions = []
        for num in range(10):
            solution = list()
            solution.append(randint(1, 1000))
            solution.append(f"Участник {num}")
            solution.append(f"Описание {num}")
            solution.append(random()*10)
            solution.append(random()*10)
            self.solutions.append(solution)

        self.solutions_tw = QTableWidget()
        self.solutions_tw.setRowCount(len(self.solutions) + 1)
        self.solutions_tw.setColumnCount(5)
        self.solutions_tw.verticalHeader().hide()
        self.solutions_tw.horizontalHeader().hide()
        header = self.solutions_tw.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        item = QTableWidgetItem(str("Id"))
        self.solutions_tw.setItem(0, 0, item)
        item = QTableWidgetItem(str("Имя отправителя"))
        self.solutions_tw.setItem(0, 1, item)
        item = QTableWidgetItem(str("Описание решения"))
        self.solutions_tw.setItem(0, 2, item)
        item = QTableWidgetItem(str("Величина ошибки"))
        self.solutions_tw.setItem(0, 3, item)
        item = QTableWidgetItem(str("Результат"))
        self.solutions_tw.setItem(0, 4, item)

        for row, participant in enumerate(self.solutions, start=1):
            btn = QPushButton(str(self.solutions[row-1][0]))
            self.solutions_tw.setCellWidget(row, 0, btn)
            for col, data in enumerate(participant[1:], start=1):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEnabled)
                self.solutions_tw.setItem(row, col, item)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addWidget(self.solutions_tw)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
