from logging import getLogger

from flask import render_template


class ErrorHandlers:
    DEFAULT_ERR_404_PAGE_FILENAME = "404.html"
    DEFAULT_ERR_404_CODE = 404

    def __init__(self, **kwargs):
        self.debug_mode = kwargs.get('debug', False)
        self.logger = kwargs.get('logger', getLogger(__name__))
        self.logger.name = self.__class__.__name__

        self.err_404_page_filename = kwargs.get('err_404_page_filename',
                                                self.__class__.DEFAULT_ERR_404_PAGE_FILENAME)
        self.err_404_code = kwargs.get('err_404_code',
                                       self.__class__.DEFAULT_ERR_404_CODE)

    def handle_page_not_found(self, error):
        # You can render a custom HTML page or return a plain string
        try:
            return (render_template(self.err_404_page_filename),
                    self.err_404_code)
        except IOError:
            if self.debug_mode:
                raise
            return f"Error page not found - {error}", self.err_404_code

    def handle_template_not_found(self, e):
        return self.handle_page_not_found(e)
