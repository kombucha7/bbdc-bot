import logging
import datetime
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from bot import send_message

# setup logging
logging.basicConfig(filename="log.txt",
                    format='%(asctime)s %(message)s', level=logging.INFO)

chrome_options = Options()
chrome_options.add_argument("--headless")

def app(config):  # sourcery skip: extract-duplicate-method
    # username password
    username = config["bbdc"]["username"]
    password = config["bbdc"]["password"]

    # bot
    bot_token = config["telegram"]["token"]
    chat_id = config["telegram"]["chat_id"]
    enable_bot = config["telegram"]["enabled"]


    # connect to Chrome
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://booking.bbdc.sg/#/login?redirect=%2Fhome%2Findex')

    # login BBDC
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-8"]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-15"]')))
    id_login = browser.find_element(By.XPATH, '//*[@id="input-8"]')
    id_login.send_keys(username)
    password_login = browser.find_element(By.XPATH, '//*[@id="input-15"]')
    password_login.send_keys(password)
    login_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/form/div/div[5]/button/span')
    login_button.click()

    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/nav/div[1]/div[3]/div[2]/a')))
    except TimeoutException:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div[2]/div[1]/div/button[2]')))
        expand_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div[2]/div[1]/div/button[2]')
        expand_button.click()
    finally:  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/nav/div[1]/div[3]/div[2]/a')))
        booking_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/nav/div[1]/div[3]/div[2]/a')
        booking_button.click()  

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]')))
    practical_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]')
    practical_button.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/div/button/span')))
    book_slot_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/div/button/span')
    book_slot_button.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]')))
    no_fixed_instructor_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]')
    no_fixed_instructor_button.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[3]/div/button/span')))
    next_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[3]/div/button/span')
    next_button.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[1]/div[1]')))
    months_array = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[1]/div[1]').find_elements(By.XPATH, ".//button")

    return_months = [month.find_element(By.XPATH, ".//span").text for month in months_array]

    print(return_months)

    logging.info("find available slots")
    wanted = [datetime.date.today().strftime("%b'%y").upper(), (datetime.date.today() + relativedelta(months=+1)).strftime("%b'%y").upper()]
    successful = False
    available_months = []
    for want in wanted:
        if want in return_months:
            successful = True
            available_months.append(want)
    if successful:
        message = f"Found available slots for {available_months} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        message = f"No slots available at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if enable_bot:
        send_message(message, bot_token, chat_id)
    logging.info(message)
    browser.quit()

    
    