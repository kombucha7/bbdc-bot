# BBDC-Booking-Bot

Program help to check the available slots in BBDC (Bukit Batok Driving Centre), and send notification to your phone by Telegram bot.

# Prerequisites

- Python3
- [Docker](https://docs.docker.com/get-docker/) (headless Chrome)
- [Telegram Bot](https://t.me/botfather)

# Setup

## Pull docker image of Chrome

```sh
$ docker pull selenium/standalone-chrome
```

## Clone the repo

```sh
$ git clone https://github.com/kombucha7/bbdc-bot.git
$ cd bbdc-bot
```

## Create virtual environment and source the environment

```sh
# create virtual environment
$ python3 -m venv .venv
# activate the environment
$ source .venv/bin/activate
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
- Your wanted `sessions`
- Telegram Bot `token` and `chat_id`

# Run the program

## Launch Chrome container

```sh
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome
```

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
