# BBDC-Booking-Bot

Program help to check the available slots in BBDC (Bukit Batok Driving Centre), and send notification to your phone by Telegram bot.

NOTE: Due to new updates to BBDC site, stricter anti-botting measures have been added so do use at your own risk.

# Prerequisites

- Python3
- [Telegram Bot](https://t.me/botfather)

# Setup

## Clone the repo

```sh
$ git clone https://github.com/kombucha7/bbdc-bot.git
$ cd bbdc-bot
```

## Create virtual environment and source the environment

```sh
# create virtual environment
$ python -m venv .venv
# activate the environment
$ .venv/bin/activate.ps1
```

## Install dependencies

```sh
$ pip install -r requirements.txt
```

## Create your telegram bot

Follow this [post](https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l) to create your telegram bot

## Fill in your information

please fill in the followings in the `config.yaml`

- `Interval` of checking the slots (example: every 5 mins)
- BBDC `username` and `password`
- Telegram Bot `token` and `chat_id`

# Run the program

## Run the program

```sh
python main.py
```

# References

- https://github.com/rohit0718/BBDC-Bot
- https://github.com/weimingwill/bbdc-booking
- https://core.telegram.org/bots
- https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l
- https://github.com/lizzzcai/bbdc-booking-bot
