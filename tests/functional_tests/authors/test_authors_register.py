from time import sleep

from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.browser.get(self.live_server_url + reverse("authors:register"))
        self.form = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/form")
        self.first_name = self.get_element_by_id(self.form, "id_first_name")
        self.last_name = self.get_element_by_id(self.form, 'id_last_name')
        self.username = self.get_element_by_id(self.form, 'id_username')
        self.email = self.get_element_by_id(self.form, 'id_email')
        self.password = self.get_element_by_id(self.form, 'id_password')
        self.password2 = self.get_element_by_id(self.form, 'id_password2')

    def test_t(self):
        self.fill_form_dummy_data(self.form)

        self.first_name.send_keys(Keys.ENTER)
        sleep(4)
        # self.assertIn()
