from WhiskeyCountdown import WhiskeyCountdown


def main():
    countdown = WhiskeyCountdown().from_cli()
    countdown.run_countdown_timer()


if __name__ == "__main__":
    main()
