import datetime
from WhiskeyCountdown.config import Config


class TTCalculations:
    END_YEAR = Config.END_YEAR
    END_MONTH = Config.END_MONTH
    END_DAY = Config.END_DAY
    END_HOUR = Config.END_HOUR

    @classmethod
    def _get_approx_datetime(cls):
        return datetime.datetime(cls.END_YEAR, cls.END_MONTH, cls.END_DAY, cls.END_HOUR)

    @property
    def time_to_datetime(self) -> datetime.timedelta:
        return self._get_approx_datetime() - datetime.datetime.now()

    @property
    def time_to_days(self) -> int:
        return self.time_to_datetime.days

    @property
    def time_to_hours(self) -> int:
        return round(self.time_to_datetime.seconds // 3600)

    @property
    def time_to_minutes(self) -> int:
        return round(self.time_to_datetime.seconds % 3600 // 60)

    @property
    def time_to_seconds(self):
        return self.time_to_datetime.seconds % 60


class TTStrings(TTCalculations):
    TIME_TO_STRING = Config.TIME_TO_STRING
    DAYS = Config.DAYS_LABEL
    HOURS = Config.HOURS_LABEL
    MINUTES = Config.MINUTES_LABEL
    SECONDS = Config.SECONDS_LABEL

    @property
    def days_string(self):
        return f"{self.time_to_datetime.days} {self.__class__.DAYS}"

    @property
    def hours_string(self):
        return f"{self.time_to_hours} {self.__class__.HOURS}"

    @property
    def minutes_string(self):
        return f"{self.time_to_minutes} {self.__class__.MINUTES}"

    @property
    def seconds_string(self):
        return f"{self.time_to_seconds} {self.__class__.SECONDS}"

    def _days_left_string(self):
        return (f"{self.__class__.TIME_TO_STRING}{self.days_string}, "
                f"{self.hours_string}, {self.minutes_string}, {self.seconds_string}")

    def _no_days_left_string(self):
        return (f"{self.__class__.TIME_TO_STRING}{self.hours_string},"
                f" {self.minutes_string}, {self.seconds_string}")

    def _no_hours_left_string(self):
        return (f"{self.__class__.TIME_TO_STRING}{self.minutes_string},"
                f" {self.seconds_string}")
