from WhiskeyCountdown import WhiskeyCountdown


def main():
    # FIXME: for some reason this creates an extra logger with EasyLoggerAJM as the title?
    countdown = WhiskeyCountdown().from_cli()
    countdown.run_countdown_timer()


if __name__ == "__main__":
    main()
