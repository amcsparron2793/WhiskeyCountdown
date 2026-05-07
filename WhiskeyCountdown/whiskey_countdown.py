import datetime
from os import system
from time import sleep

from WhiskeyCountdown import TTStrings, _WhiskeyCli, WhiskeyInitializer


class WhiskeyCountdown(WhiskeyInitializer, _WhiskeyCli, TTStrings):

    @classmethod
    def from_cli(cls):
        args = cls._parse_args()
        return cls._initialize_countdown_class(early_arrival=args.early_arrival, debug=args.debug)

    @classmethod
    def _initialize_countdown_class(cls, **kwargs):
        early_arrival = kwargs.get('early_arrival', False)
        if early_arrival:
            return EarlyWhiskeyCountdown(**kwargs)
        else:
            return cls(**kwargs)

    @property
    def countdown_title_string(self):
        tt_string = (self.__class__.TIME_TO_STRING[:-2]
                     if self.__class__.TIME_TO_STRING.strip().endswith(':')
                     else self.__class__.TIME_TO_STRING)
        return (f"Counting down to {self.__class__.APPROX_DATETIME.ctime()} "
                f"({tt_string})")

    @property
    def final_countdown_string(self):
        return '\n'.join([self.countdown_title_string,
                          self.countdown_string])

    @property
    def countdown_string(self):
        if self.time_to_days == 0:
            return self._no_days_left_string()
        elif self.time_to_hours == 0:
            return self._no_hours_left_string()
        else:
            return self._days_left_string()

    def run_countdown_timer(self) -> str:
        while True:
            print(self.final_countdown_string)
            sleep(1)
            system('cls')

    def __str__(self):
        return self.countdown_string


class EarlyWhiskeyCountdown(WhiskeyCountdown):
    APPROX_DATETIME = datetime.datetime(2026, 5, 14, 17)
    TIME_TO_STRING = "Time to EARLY arrival: "


if __name__ == "__main__":
    whiskey_countdown = WhiskeyCountdown()
    whiskey_countdown.run_countdown_timer()
