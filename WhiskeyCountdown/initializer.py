import argparse
from os import chdir
from pathlib import Path
from typing import Union

from WhiskeyCountdown import WhiskeyLogger, DEFAULT_PROJECT_ROOT, InvalidProjectRootError


class _WhiskeyCli:
    DEFAULT_ARG_PARSE_DESCRIPTION = 'Run Whiskey Countdown'

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', WhiskeyLogger(**kwargs)())
        kwargs.setdefault('logger', self.logger)
        self.logger.name = self.__class__.__name__
        self.logger.info(f'Initializing {self.__class__.__name__} instance')
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


class WhiskeyInitializer:
    def __init__(self, **kwargs):
        self._project_root = None

        self.logger = kwargs.get('logger', WhiskeyLogger(**kwargs)())
        kwargs.setdefault('logger', self.logger)
        self.logger.name = self.__class__.__name__
        self.logger.debug(f'logger name set to {self.logger.name}')
        self.debug_mode = kwargs.get('debug', False)
        self.project_root = kwargs.get('project_root', DEFAULT_PROJECT_ROOT)

        self.logger.info(f'project root set to {self.project_root} with debug mode set to {self.debug_mode}')

    def _validate_project_root(self, value: Union[str, Path]) -> Path:
        if Path(value).is_dir():
            return Path(value)
        else:
            try:
                raise InvalidProjectRootError(
                    f"Invalid project root: {value}. "
                    f"Must be a valid directory path.")
            except InvalidProjectRootError as e:
                self.logger.error(e)
                raise e

    @property
    def project_root(self):
        return self._project_root

    @project_root.setter
    def project_root(self, value):
        self._project_root = self._validate_project_root(value)
        if Path('./') != self._project_root:
            self.logger.warning(f'changing working directory to {self._project_root}')
            chdir(self._project_root)
