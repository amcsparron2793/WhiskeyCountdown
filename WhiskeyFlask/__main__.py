from FlaskRedirectPage.flask_redirect_page import QuickRedirect


def main():
    srv = QuickRedirect.from_cli()
    srv.logger.debug('running from __main__.py')
    srv.run()


if __name__ == "__main__":
    main()
