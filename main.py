import sys
from PySide6.QtWidgets import QApplication
from data.db import init_db
from data.controller import Controller


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    cont = Controller()
    sys.exit(app.exec())

