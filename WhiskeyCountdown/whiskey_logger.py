from logging import Logger
from pathlib import Path

from EasyLoggerAJM import EasyLogger
from WhiskeyCountdown import DEFAULT_PROJECT_ROOT


class WhiskeyLogger(EasyLogger):
    DEFAULT_LOG_SPEC = 'hourly'
    _PROJECT_NAME = DEFAULT_PROJECT_ROOT.name
    ROOT_LOG_LOCATION_DEFAULT = Path(DEFAULT_PROJECT_ROOT, 'logs')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log_spec', self.__class__.DEFAULT_LOG_SPEC)
        kwargs.setdefault('show_warning_logs_in_console', True)
        super().__init__(*args, **kwargs)

    def __call__(self) -> Logger:
        return self.logger
