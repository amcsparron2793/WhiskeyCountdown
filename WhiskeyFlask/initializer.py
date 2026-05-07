from pathlib import Path
from os import chdir
from typing import Union

from flask import Flask
from jinja2 import TemplateNotFound

# noinspection PyProtectedMember
from WhiskeyCountdown import DEFAULT_PROJECT_ROOT, _WhiskeyCli
from WhiskeyFlask import (DEFAULT_FLASK_APP_NAME,
                          WhiskeyFlaskLogger,
                          WerkzeugLogger,
                          HomePage, ErrorHandlers,
                          FlaskAppInitializationError, InvalidProjectRootError)


class _WhiskeyFlaskCli(_WhiskeyCli):
    DEFAULT_HOST = None
    DEFAULT_PORT = None
    TEST_DEFAULT_HOST = None
    MANDATORY_ATTRS = ['DEFAULT_HOST', 'DEFAULT_PORT', 'TEST_DEFAULT_HOST']
    DEFAULT_ARG_PARSE_DESCRIPTION = "Run the Whiskey Countdown Page"

    def __init_subclass__(cls, **kwargs):
        missing_attrs = [x for x in cls.MANDATORY_ATTRS if not getattr(cls, x)]
        if missing_attrs:
            raise ValueError(f"Missing mandatory attribute(s): {missing_attrs}")
        super().__init_subclass__()

    @classmethod
    def _get_default_host(cls, is_debug=False):
        return (cls.DEFAULT_HOST
                if not is_debug
                else cls.TEST_DEFAULT_HOST)

    @classmethod
    def _cli_is_debug_with_default_production_host(cls, debug: bool, host: str):
        return debug and (host is None
                          or host == cls.DEFAULT_HOST)

    @classmethod
    def _init_parser(cls, **kwargs):
        parser = super()._init_parser(**kwargs)
        parser.add_argument(
            "-H",
            "--host",
            default=cls.DEFAULT_HOST,
            help=f"Host/IP to bind to (default: {cls.DEFAULT_HOST})",
        )
        parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=cls.DEFAULT_PORT,
            help=f"Port to listen on (default: {cls.DEFAULT_PORT})",
        )
        return parser


class WhiskeyInitializer:
    DEFAULT_APP_NAME = DEFAULT_FLASK_APP_NAME

    def __init__(self, **kwargs):
        self._project_root = None

        self.werkzeug_logger = kwargs.get('werkzeug_logger', WerkzeugLogger()())
        self.logger = kwargs.get('logger', WhiskeyFlaskLogger(**kwargs)())
        kwargs.setdefault('logger', self.logger)
        self.logger.name = self.__class__.__name__
        self.logger.debug(f'logger name set to {self.logger.name}')

        self._app_initialized = False
        self.debug_mode = kwargs.get('debug', False)
        self.app_name = kwargs.get('app_name', self.__class__.DEFAULT_APP_NAME)

        self.project_root = kwargs.get('project_root', DEFAULT_PROJECT_ROOT)
        self.resource_root = kwargs.get('resource_root',
                                        Path(self.project_root / 'WhiskeyFlask'))

        self.logger.info(f'project root set to {self.project_root} with debug mode set to {self.debug_mode}')

        self.home_page, self.error_handlers = self._app_pre_init(**kwargs)

        self.app = self.start_app()

    def _app_pre_init(self, **kwargs):
        home_page = self._initialize_pages(**kwargs)
        error_handlers = self._initialize_error_handlers(**kwargs)
        self.logger.info(f'home page set to {home_page.home_page_filename} '
                         f'Error handlers set to {error_handlers.err_404_page_filename}')
        return home_page, error_handlers

    def _initialize_pages(self, **kwargs):
        kwargs.setdefault('debug', self.debug_mode)
        home_page = HomePage(**kwargs)
        return home_page

    def _initialize_error_handlers(self, **kwargs):
        kwargs.setdefault('debug', self.debug_mode)
        error_handlers = ErrorHandlers(**kwargs)
        return error_handlers

    def _add_url_rules_to_app(self):
        self.app.add_url_rule('/', 'home', self.home_page.get)
        # self.app.add_url_rule('/redirect', 'redirect', self.redirect_page.get)

    def _register_error_handlers_with_app(self):
        self.app.register_error_handler(TemplateNotFound, self.error_handlers.handle_template_not_found)
        self.app.register_error_handler(self.error_handlers.err_404_code, self.error_handlers.handle_page_not_found)

    @property
    def _is_ready_to_initialize(self):
        if not hasattr(self, 'app') or not isinstance(self.app, Flask):
            raise FlaskAppInitializationError("App not initialized. Call start_app(),"
                                              " do not call _initialize_app() directly.")
        if self._app_initialized:
            raise FlaskAppInitializationError("App already initialized. Cannot initialize again.")
        return True

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

    def _initialize_app(self):
        if self._is_ready_to_initialize:
            self._add_url_rules_to_app()
            self._register_error_handlers_with_app()
            self._app_initialized = True

    def start_app(self):
        self.app = Flask(self.app_name,
                         static_folder=Path(self.resource_root, 'static'),
                         template_folder=Path(self.resource_root, 'templates'))
        self._initialize_app()
        return self.app


class WhiskeyCountdownInitializer(WhiskeyInitializer):
    def __init__(self, countdown_class, **kwargs):
        self.countdown_class = countdown_class
        super().__init__(**kwargs)

    def _initialize_pages(self, **kwargs):
        kwargs.setdefault('debug', self.debug_mode)
        kwargs.setdefault('countdown_class', self.countdown_class)
        home_page = HomePage(**kwargs)
        return home_page
