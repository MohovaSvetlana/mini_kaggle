from PySide6.QtWidgets import QWidget, \
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QPushButton
from data.interface.ui_competition_bars import CompetitionBars
from PySide6.QtCore import Qt

from database import DataBase


class UIAllSubmissions(QWidget, CompetitionBars):
    def __init__(self, window, controller):

        super().__init__()
        self.controller = controller
        self.submissions_data = DataBase.get_all_submissions(self.controller.competition, self.controller.user)

        self.window = window
        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.submissions_tw = QTableWidget()
        self.submissions_tw.setRowCount(len(self.submissions_data))
        self.submissions_tw.setColumnCount(len(self.submissions_data[0]))
        self.submissions_tw.verticalHeader().hide()
        self.submissions_tw.horizontalHeader().hide()
        header = self.submissions_tw.horizontalHeader()

        for col, head_name in enumerate(self.submissions_data[0], start=0):
            item = QTableWidgetItem(head_name)
            item.setFlags(Qt.ItemIsEnabled)
            self.submissions_tw.setItem(0, col, item)
            header.setSectionResizeMode(col, QHeaderView.Stretch if 2 <= col <= 3 else QHeaderView.ResizeToContents)

        for row, submission in enumerate(self.submissions_data[1:], start=1):
            btn = QPushButton(str(submission[0]))
            btn.submission_id = submission[0]
            btn.clicked.connect(self.download_submission)
            self.submissions_tw.setCellWidget(row, 0, btn)
            for col, data in enumerate(submission[1:], start=1):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEnabled)
                self.submissions_tw.setItem(row, col, item)

        self.main_layout.addLayout(self.pages_bar_layout)
        self.main_layout.addWidget(self.submissions_tw)
        self.main_layout.addLayout(self.toolbar_layout)

        if self.controller.user.is_organizer:
            self.show_buttons_for_organizer()
        if self.controller.competition.is_finished:
            self.change_buttons_for_finished_competition()

    def download_submission(self):
        self.controller.download_submission(self.sender().submission_id)
