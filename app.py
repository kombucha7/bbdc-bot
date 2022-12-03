import logging
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from bot import send_message

# setup logging
logging.basicConfig(filename="log.txt",
                    format='%(asctime)s %(message)s', level=logging.INFO)


def app(config):
    # username password
    username = config["bbdc"]["username"]
    password = config["bbdc"]["password"]
    # want sessions
    want_sessions = config["booking"]["want_sessions"]

    # bot
    bot_token = config["telegram"]["token"]
    chat_id = config["telegram"]["chat_id"]
    enable_bot = config["telegram"]["enabled"]

    # chrome host
    chrome_host = config["chromedriver"]["host"]

    # connect to Chrome
    # browser = webdriver.Remote('{:}/wd/hub'.format(chrome_host), DesiredCapabilities.CHROME)
    browser = webdriver.Chrome()
    browser.get('https://booking.bbdc.sg/#/login?redirect=%2Fhome%2Findex')

    # login BBDC
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholer="example: 567A02071990"')))
    wait.until(EC.presence_of_element_located((By.ID, "txtNRIC")))
    id_login = browser.find_element(By.ID, 'txtNRIC')
    id_login.send_keys(username)
    password_login = browser.find_element(By.ID, 'txtPassword')
    password_login.send_keys(password)
    login_button = browser.find_element(By.ID, 'loginbtn')
    login_button.click()

    # proceed unsure form (Chrome)
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.visibility_of_element_located(
        (By.ID, "proceed-button"))).click()

    # Switching to Left Frame and accessing element by text
    browser.switch_to.default_content()
    frame = browser.find_element(By.NAME, 'leftFrame')
    browser.switch_to.frame(frame)
    # non_fixed_instructor = browser.find_element_by_link_text(
    #     'Booking without Fixed Instructor')
    non_fixed_instructor = browser.find_element(
        By.LINK_TEXT, 'Booking without Fixed Instructor')
    non_fixed_instructor.click()

    # Switching back to Main Frame and pressing 'I Accept'
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        browser.find_element(By.NAME, 'mainFrame')))
    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "btn"))).click()
    accept_btn = browser.find_element(By.CLASS_NAME, 'btn')
    accept_btn.click()

    # Selection menu
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        browser.find_element(By.NAME, 'mainFrame')))
    wait.until(EC.visibility_of_element_located((By.ID, "checkMonth")))

    # 0 refers to first month, 1 refers to second month, and so on...
    months = browser.find_elements(By.ID, 'checkMonth')
    if len(months) == 13:
        months[12].click()  # all months
    else:
        months[0].click()  # first month

    # 0 refers to first session, 1 refers to second session, and so on...
    sessions = browser.find_elements(By.ID, 'checkSes')
    sessions[8].click()  # all sessions

    # 0 refers to first day, 1 refers to second day, and so on...
    days = browser.find_elements(By.ID, 'checkDay')
    days[7].click()  # all days

    # Selecting Search
    browser.find_element(By.NAME, 'btnSearch').click()

    # Dismissing Prompt
    wait = WebDriverWait(browser, 15)
    wait.until(EC.alert_is_present())
    alert_obj = browser.switch_to.alert
    alert_obj.accept()

    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "slot")))
    except TimeoutException:
        logging.info("no slot is available")
        browser.quit()
        return

    logging.info("find available slots")
    wanted = []
    # 0 refers to first slot, 1 refers to second slot, and so on...
    slots = browser.find_elements(By.NAME, 'slot')
    logging.info(f"number of slot: {len(slots)}")
    for slot in slots:     # Selecting all checkboxes
        # parse the data
        parent = slot.find_element(By.XPATH, './..')
        text = parent.get_attribute("onmouseover")
        splits = text.split(",")
        session_date = splits[2].replace('"', '')
        session_id = splits[3].replace('"', '')
        session_start_time = splits[4].replace('"', '')
        session_end_time = splits[5].replace('"', '')
        print(session_id)
        logging.info(
            f"session available:    date:{session_date}, slot:{session_id}, "
            f"time:{session_start_time}-{session_end_time}"
        )
        if session_id in want_sessions:
            wanted.append({"check": slot, "date": session_date, "slot": session_id,
                          "start_time": session_start_time, "end_time": session_end_time})

    logging.info(f"number of wanted slot: {len(wanted)}")

    # send notification by telegram if any available slot
    if wanted and enable_bot:
        print("Here")
        message = "session availabile:"
        for sess in wanted:
            date = sess["date"]
            slot = sess["slot"]
            start, end = sess["start_time"], sess["end_time"]
            message += f"\ndate:{date}, slot:{slot}, time:{start}-{end}"
        send_message(message, bot_token, chat_id)

        # # Uncomment the below code to book the first available slot
        # # select the first one and submit
        # wanted[0]['check'].click()
        # # clicking random element to hide hover effect
        # browser.find_element_by_class_name('pgtitle').click()
        # # Selecting Submit
        # browser.find_element_by_name('btnSubmit').click()
        # # Selecting confirm
        # wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, "//input[@value='Confirm']")))
        # browser.find_element_by_xpath("//input[@value='Confirm']").click()
    elif not wanted and enable_bot:
        message = f"No slots availabe at {time.localtime()}"
        send_message(message, bot_token, chat_id)

    browser.quit()
