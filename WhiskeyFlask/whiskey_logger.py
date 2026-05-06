import string
from re import sub

from logging import Logger, getLogger, INFO, Formatter, LogRecord
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

from EasyLoggerAJM.easy_logger import EasyLogger
from EasyLoggerAJM.logger_parts import ColorizedFormatter

from WhiskeyFlask import DEFAULT_FLASK_APP_NAME, DEFAULT_PROJECT_ROOT


class WerkzeugFileFormatter(Formatter):
    """
    Custom formatter to handle log record messages.

    This class provides custom handling of log messages, particularly ensuring
    that the messages are cleaned to contain only printable characters, and
    any issues with interpolation of modified log messages are avoided. Inherits
    from `Formatter`.
    """

    def format(self, record: LogRecord) -> str:
        record.msg = self.clean_log_message(record.msg)
        record.args = None  # Clear args to avoid interpolation
        # issues after modification

        return super().format(record)

    @staticmethod
    def _remove_ansi_escape_sequences(msg: str) -> str:
        """Remove ANSI escape sequences from a string."""
        pattern = r"\[\w.*?m"
        return sub(pattern, "", msg)

    def clean_log_message(self, msg: str) -> str:
        if not isinstance(msg, str):
            return msg

        # ensures only characters that are printable per Unicode
        # and part of `string.printable` are retained. This covers
        # both common printable characters and certain Unicode
        # characters that might also be "printable" but aren't
        # in the ASCII set.
        # The self._remove_ansi_escape_sequences() method covers any leftovers from Colorizer
        return ''.join(filter(lambda x: x in string.printable and x.isprintable(),
                              self._remove_ansi_escape_sequences(msg)))


class WhiskeyLogger(EasyLogger):
    DEFAULT_LOG_SPEC = 'hourly'
    _PROJECT_NAME = ''.join([x.capitalize() for x in DEFAULT_FLASK_APP_NAME.split('_')])
    ROOT_LOG_LOCATION_DEFAULT = Path(DEFAULT_PROJECT_ROOT.parent, 'logs')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log_spec', self.__class__.DEFAULT_LOG_SPEC)
        kwargs.setdefault('show_warning_logs_in_console', True)
        super().__init__(*args, **kwargs)

    def __call__(self) -> Logger:
        return self.logger


class WerkzeugLogger(EasyLogger):
    LOG_LEVEL_TO_STREAM = INFO
    DEFAULT_LOG_SPEC = WhiskeyLogger.DEFAULT_LOG_SPEC

    ROOT_LOG_LOCATION_DEFAULT = WhiskeyLogger.ROOT_LOG_LOCATION_DEFAULT
    _PROJECT_NAME = 'Werkzeug'

    DEFAULT_ROTATING_MAX_BYTES = 10_000_000
    DEFAULT_ROTATING_BACKUP_COUNT = 5

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log_spec', self.__class__.DEFAULT_LOG_SPEC)
        super().__init__(*args, **kwargs)
        self.initialize_logger(logger=getLogger('werkzeug'))
        self.create_stream_handler(log_level_to_stream=self.__class__.LOG_LEVEL_TO_STREAM)

        self.rotating_max_bytes = kwargs.get('rotating_max_bytes',
                                             self.__class__.DEFAULT_ROTATING_MAX_BYTES)
        self.rotating_backup_count = kwargs.get('rotating_backup_count',
                                                self.__class__.DEFAULT_ROTATING_BACKUP_COUNT)

        self.make_rotating_file_handler()

    def __call__(self) -> Logger:
        return self.logger

    def make_file_handlers(self, *args, **kwargs):
        ...

    def _setup_formatters(self, **kwargs) -> (Formatter, Union[ColorizedFormatter, Formatter]):
        kwargs.setdefault('formatter', WerkzeugFileFormatter())
        return super()._setup_formatters(**kwargs)

    def make_rotating_file_handler(self, *args, **kwargs):
        mb = kwargs.get('rotating_max_bytes', self.rotating_max_bytes)
        bc = kwargs.get('rotating_backup_count', self.rotating_backup_count)
        fname = f'werkzeug-{self.log_spec["format"][0]}_{self.timestamp}.log'

        rfh_args = {'filename': Path(self.log_location, fname),
                    'maxBytes': mb,
                    'backupCount': bc}

        self._internal_logger.debug(f'rotating file handler args set to {rfh_args}')
        self._internal_logger.info('creating rotating file handler')
        self.create_other_handlers(RotatingFileHandler, handler_args=rfh_args, **kwargs)
