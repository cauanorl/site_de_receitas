import pytest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def select_form(self) -> WebElement:
        form = self.browser.find_element(
            By.XPATH,
            "/html/body/div[2]/form"
        )

        return form

    def test_user_cannot_log_in_if_user_is_already_logged_in(self):
        string_password = "P@ssw0rd"
        self.browser.get(self.live_server_url + reverse("authors:login"))

        user = User.objects.create_user(username="MyTestUser", password=string_password)

        self.fill_out_and_submit_login_form(user.username, string_password)

        self.browser.get(self.live_server_url + reverse("authors:login"))
        self.assertIn(
            "Nenhuma receita publicada no momento",
            self.browser.find_element(By.TAG_NAME, "body").text
        )

    def fill_out_and_submit_login_form(self, username, password):
        form = self.select_form()
        form.find_element(By.XPATH, '//*[@id="id_username"]').send_keys(username)
        form.find_element(By.XPATH, '//*[@id="id_password"]').send_keys(password, Keys.ENTER)

    def test_user_valid_data_can_login_successfully(self):
        string_password = "P@ssw0rd"

        user = User.objects.create_user(
            username="my_user",
            password=string_password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))
        self.fill_out_and_submit_login_form(user.username, string_password)

        self.assertIn(
            "Nenhuma receita publicada no momento",
            self.browser.find_element(By.TAG_NAME, "body").text
        )

    def test_password_is_incorrect(self):
        string_password = "P@ssw0rd"
        wrong_password = "Wr0ngP@ss0rd"

        user = User.objects.create_user(
            username="my_user",
            password=string_password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))
        self.fill_out_and_submit_login_form(user.username, wrong_password)

        self.assertIn(
            "Sua senha está incorreta",
            self.browser.find_element(By.TAG_NAME, "body").text
        )

    def test_user_does_not_exist(self):
        username = "UserDoesNotExistUsername"
        string_password = "P@ssw0rd"

        self.browser.get(self.live_server_url + reverse("authors:login"))
        self.fill_out_and_submit_login_form(username, string_password)
        self.assertIn(
            "Esse nome de usuário não existe",
            self.browser.find_element(By.TAG_NAME, "body").text
        )

    def test_login_fields_do_not_accept_empty_values(self):
        username = " "
        string_password = " "

        self.browser.get(self.live_server_url + reverse("authors:login"))
        self.fill_out_and_submit_login_form(username, string_password)
        self.assertIn(
            "Este campo é obrigatório",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
