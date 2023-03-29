from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By



class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_element_by_id(self, web_element: WebElement, element_id: str) -> WebElement:
        element = web_element.find_element(
            By.XPATH,
            f'//*[@id="{element_id}"]'
        )

        return element
