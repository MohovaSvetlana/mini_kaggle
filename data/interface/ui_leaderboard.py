from PySide6.QtWidgets import QWidget, \
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QDateEdit


from data.interface.ui_competition_bars import CompetitionBars


class UILeaderboard(CompetitionBars):
    def __init__(self, window, controller):
        super().__init__()
        self.controller = controller
        self.participants = [[1, "Participant 1", 0.6223], [2, "Participant 2", 1.405], [3, "Participant 3", 4.5842]]

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.leaderboard_tw = QTableWidget()
        self.leaderboard_tw.setEnabled(False)
        self.leaderboard_tw.setMinimumWidth(300)
        self.leaderboard_tw.setRowCount(len(self.participants)+1)
        if len(self.participants) != 0:
            self.leaderboard_tw.setColumnCount(len(self.participants[0]))
        self.leaderboard_tw.horizontalHeader().hide()
        self.leaderboard_tw.verticalHeader().hide()
        header = self.leaderboard_tw.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        item = QTableWidgetItem(str("№"))
        self.leaderboard_tw.setItem(0, 0, item)
        item = QTableWidgetItem(str("Имя"))
        self.leaderboard_tw.setItem(0, 1, item)
        item = QTableWidgetItem(str("Оценка"))
        self.leaderboard_tw.setItem(0, 2, item)
        for row, participant in enumerate(self.participants, start=1):
            for col, data in enumerate(participant):
                item = QTableWidgetItem(str(data))
                self.leaderboard_tw.setItem(row, col, item)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addWidget(self.leaderboard_tw)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
