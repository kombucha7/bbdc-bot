from app import app
import schedule
import time
from config import load_config

# load config
config = load_config("config.yaml")
interval = config["interval"]


def job():
    try:
        app(config)
    except Exception as e:
        print(e)

def checkTime():
    current_hour = time.localtime().tm_hour
    return current_hour < 23 and current_hour > 14

if __name__ == "__main__":
    job()  # test
    schedule.every(interval).minutes.do(job)
    while True:
        if checkTime():
            schedule.run_pending()
            time.sleep(1)
        else:
            print("night sleep")
            time.sleep(3600)
