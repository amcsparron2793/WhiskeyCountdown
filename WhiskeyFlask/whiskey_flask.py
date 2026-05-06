"""
whiskey_flask.py

"""

from WhiskeyFlask import _WhiskeyCli, WhiskeyInitializer, WhiskeyCountdownInitializer


class WhiskeyFlask(WhiskeyInitializer, _WhiskeyCli):
    TEST_DEFAULT_HOST = '127.0.0.1'
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 5000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.name = self.__class__.__name__

        self.debug_mode = kwargs.get('debug', False)
        self.host = kwargs.get('host', self._get_default_host(self.debug_mode))
        self.port = kwargs.get('port', self.__class__.DEFAULT_PORT)
        self.logger.info(f'host set to {self.host} on port {self.port} '
                         f'with debug mode set to {self.debug_mode}')
        if self.debug_mode:
            self.logger.warning('DEBUG MODE ENABLED')
        self.logger.info('WhiskeyFlask initialized')

    @classmethod
    def from_cli(cls):
        args = cls._parse_args()

        if cls._cli_is_debug_with_default_production_host(args.debug, args.host):
            args.host = cls._get_default_host(args.debug)
            print(f"DEBUG MODE: Using {args.host} as the host")

        return cls(host=args.host, port=args.port, debug=args.debug)

    def run(self, *args, **kwargs):
        kwargs.setdefault('host', self.host)
        kwargs.setdefault('port', self.port)
        kwargs.setdefault('debug', self.debug_mode)
        self.logger.info(f'Running {self.app.name} on {self.host}:{self.port}')
        self.app.run(*args, **kwargs)


class WhiskeyFlaskCountdown(WhiskeyCountdownInitializer, WhiskeyFlask):
    ...


if __name__ == '__main__':
    qr_app = WhiskeyFlask(debug=True)
    qr_app.run()
