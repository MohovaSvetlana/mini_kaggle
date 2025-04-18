from datetime import datetime as dt
from datetime import timedelta


class Time:
    @staticmethod
    def get_current_date():
        return dt.today().date()

    @staticmethod
    def get_date_after_days(days, date=None):
        if date is None:
            date = Time.get_current_date()
        return date + timedelta(days=days)
