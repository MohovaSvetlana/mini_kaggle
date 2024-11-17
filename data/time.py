from datetime import datetime as dt
from datetime import timedelta
from PySide6.QtCore import QDate


class Time:
    @staticmethod
    def get_current_date():
        return dt.today().date()

    @staticmethod
    def get_date_after_days(days: int, date=get_current_date()):
        return date + timedelta(days=days)

    @staticmethod
    def to_pyside_date(date):
        return QDate(date.year, date.month, date.day)

