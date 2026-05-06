from WhiskeyFlask import WhiskeyFlaskCountdown


def main():
    srv = WhiskeyFlaskCountdown.from_cli()
    srv.logger.debug('running from __main__.py')
    srv.run()


if __name__ == "__main__":
    main()
