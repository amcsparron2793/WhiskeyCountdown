from logging import getLogger
from typing import Callable

from flask import render_template


class HomePage:
    DEFAULT_HOME_PAGE_FILENAME = "index.html"

    def __init__(self, **kwargs):
        self.debug_mode = kwargs.get('debug', False)
        self.logger = kwargs.get('logger', getLogger(__name__))
        self.logger.name = self.__class__.__name__
        # filename only since flask will look for templates
        # in the templates folder (normally the package root/templates).
        self.home_page_filename = kwargs.get('home_page_filename', self.__class__.DEFAULT_HOME_PAGE_FILENAME)

        self.logger.info(f'home page filename set to {self.home_page_filename}')

    def get(self):
        self.logger.debug(f'rendering template {self.home_page_filename}')
        return render_template(self.home_page_filename)


class WhiskeyHomePage(HomePage):
    def __init__(self, countdown_class: Callable, **kwargs):
        super().__init__(**kwargs)
        self.countdown_class = countdown_class()
        if self.countdown_class is None:
            raise ValueError('countdown_class must be provided')

    def get(self):
        self.logger.debug(f'rendering template {self.home_page_filename}')
        return render_template(self.home_page_filename, countdown=self.countdown_class)