from PySide6.QtWidgets import QWidget, \
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView


from data.interface.ui_competition_bars import CompetitionBars
from database import DataBase


class UILeaderboard(CompetitionBars):
    def __init__(self, window, controller, is_results=False):
        super().__init__()
        self.controller = controller
        self.leaderboard_data = DataBase().get_leaderboard_by_submissions(self.controller.competition.id, is_results)

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.leaderboard_tw = QTableWidget()
        self.leaderboard_tw.setEnabled(False)
        self.leaderboard_tw.setMinimumWidth(300)
        self.leaderboard_tw.setRowCount(len(self.leaderboard_data))
        self.leaderboard_tw.setColumnCount(len(self.leaderboard_data[0]))
        self.leaderboard_tw.horizontalHeader().hide()
        self.leaderboard_tw.verticalHeader().hide()
        header = self.leaderboard_tw.horizontalHeader()

        for col, head_name in enumerate(self.leaderboard_data[0]):
            item = QTableWidgetItem(head_name)
            self.leaderboard_tw.setItem(0, col, item)
            header.setSectionResizeMode(col, QHeaderView.Stretch if 1 <= col <= 2 else QHeaderView.ResizeToContents)

        for row, participant in enumerate(self.leaderboard_data[1:], start=1):
            for col, data in enumerate(participant):
                item = QTableWidgetItem(str(data))
                self.leaderboard_tw.setItem(row, col, item)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addWidget(self.leaderboard_tw)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
        if self.controller.competition.is_finished:
            self.change_buttons_for_finished_competition()
