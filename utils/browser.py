from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import os


ROOT_PATH = Path(__file__).resolve().parent.parent
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / 'chromedriver.exe'


def make_chrome_browser(*options: list[str]):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS", False) == "1":
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser


if __name__ == "__main__":
    now = datetime.now()
    browser = make_chrome_browser()
    print((datetime.now() - now).seconds)
    browser.get('https://www.facebook.com/')
    browser.quit()
    finish = datetime.now() - now
    print(
        str(finish.seconds)
    )
