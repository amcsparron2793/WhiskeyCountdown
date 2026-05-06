import datetime
from os import system
from time import sleep

from WhiskeyCountdown import TTAStrings
from WhiskeyFlask import WhiskeyFlask, WhiskeyFlaskCountdown


class WhiskeyCountdown(TTAStrings):

    @property
    def countdown_title_string(self):
        tta_string = (self.__class__.TIME_TO_ARRIVAL_STRING[:-2]
                      if self.__class__.TIME_TO_ARRIVAL_STRING.strip().endswith(':')
                      else self.__class__.TIME_TO_ARRIVAL_STRING)
        return (f"Counting down to {self.__class__.APPROX_ARRIVAL_DATETIME.ctime()} "
                f"({tta_string})")

    @property
    def final_countdown_string(self):
        return '\n'.join([self.countdown_title_string,
                          self.countdown_string])

    @property
    def countdown_string(self):
        if self.time_to_arrival_days == 0:
            return self._no_days_left_string()
        elif self.time_to_arrival_hours == 0:
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
    APPROX_ARRIVAL_DATETIME = datetime.datetime(2026, 5, 14, 17)
    TIME_TO_ARRIVAL_STRING = "Time to EARLY arrival: "


if __name__ == "__main__":
    wf = WhiskeyFlaskCountdown(debug=True, countdown_class=WhiskeyCountdown)
    wf.run()
    #whiskey_countdown = WhiskeyCountdown()
    #whiskey_countdown.run_countdown_timer()
