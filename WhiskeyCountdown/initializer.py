import argparse

# FIXME: make WhiskeyLogger a part of WhiskeyCountdown - leave Werkzug logger in WhiskeyFlask
#from WhiskeyFlask.whiskey_logger import WhiskeyLogger


class _WhiskeyCli:
    DEFAULT_ARG_PARSE_DESCRIPTION = 'Run Whiskey Countdown'

    def __init__(self, **kwargs):
        # self.logger = WhiskeyLogger(**kwargs)()
        # kwargs.setdefault('logger', self.logger)
        # self.logger.name = self.__class__.__name__
        # self.logger.info(f'Initializing {self.__class__.__name__} instance')
        self.early_arrival = kwargs.get('early_arrival', False)

    @classmethod
    def _init_parser(cls, **kwargs):
        arg_parse_description = kwargs.get('arg_parse_description', cls.DEFAULT_ARG_PARSE_DESCRIPTION)
        parser = argparse.ArgumentParser(description=arg_parse_description)
        parser.add_argument(
            "-e",
            "--early_arrival",
            action="store_true",
            help="Use Early Arrival Countdown",
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Enable debug mode",
        )
        return parser

    @classmethod
    def _parse_args(cls, **kwargs):
        parser = cls._init_parser(**kwargs)
        return parser.parse_args()
