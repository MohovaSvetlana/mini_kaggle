from datetime import datetime as dt
from datetime import timedelta
from PySide6.QtCore import QDate


class Time:
    @staticmethod
    def get_current_date():
        return dt.today().date()

    def get_date_after_days(self, days, date=None):
        if date is None:
            date = self.get_current_date()
        return date + timedelta(days=days)

    @staticmethod
    def to_pyside_date(date):
        return QDate(date.year, date.month, date.day)

    def compare_dates(self, date1, date2=None):
        if date2 is None:
            date2 = self.get_current_date()
        if date1.year == date2.year and date1.month == date2.month and date1.day == date2.day:
            return 0
        elif (date1.year > date2.year or date1.year == date2.year and
              (date1.month > date2.month or date1.month == date2.month and date1.day > date2.day)):
            return 1
        else:
            return -1
