import string
from re import sub

from logging import Logger, getLogger, INFO, Formatter, LogRecord
from logging.handlers import RotatingFileHandler
from pathlib import Path

from EasyLoggerAJM.easy_logger import EasyLogger

from WhiskeyCountdown import WhiskeyLogger
from WhiskeyFlask import DEFAULT_FLASK_APP_NAME


class WhiskeyFlaskLogger(WhiskeyLogger):
    _PROJECT_NAME = ''.join([x.capitalize() for x in DEFAULT_FLASK_APP_NAME.split('_')])


class WerkzeugFileFormatter(Formatter):
    """
    Custom formatter to handle log record messages.

    This class provides custom handling of log messages, particularly ensuring
    that the messages are cleaned to contain only printable characters, and
    any issues with interpolation of modified log messages are avoided. Inherits
    from `Formatter`.
    """

    @staticmethod
    def _manual_arg_format(record: LogRecord):
        """ Format the message with its arguments before cleaning"""
        if record.args:
            # Manually format the message
            record.msg = record.msg % record.args
            # Optional: Clear the args to avoid reformatting issues downstream
            record.args = None
        return record

    def format(self, record: LogRecord) -> str:
        record = self._manual_arg_format(record)

        # Clean the fully formatted log message
        record.msg = self.clean_log_message(record.msg)

        # Now use the parent class to complete formatting
        return super().format(record)

    @staticmethod
    def _remove_ansi_escape_sequences(msg: str) -> str:
        """Remove ANSI escape sequences from a string."""
        # sub out any string that starts with [ and ends with m with ''
        pattern = r"\[\w.*?m"
        return sub(pattern, "", msg)

    def clean_log_message(self, msg: str) -> str:
        """ Ensures only characters that are printable per Unicode
        and part of `string.printable` are retained. This covers
        both common printable characters and certain Unicode
        characters that might also be "printable" but aren't
        in the ASCII set. The self._remove_ansi_escape_sequences()
        method covers any leftovers from Colorizer. """

        if not isinstance(msg, str):
            return msg

        # filter out any non-printable chars from the results of self._remove_ansi_escape_sequences
        filtered_msg_list = filter(lambda x: x in string.printable and x.isprintable(),
                                   self._remove_ansi_escape_sequences(msg))
        return ''.join(filtered_msg_list)


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

    def _setup_formatters(self, **kwargs):
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
