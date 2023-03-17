from time import sleep

from django.urls import reverse
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.browser.get(self.live_server_url + reverse("authors:register"))
        self.select_form()

    def select_form(self):
        self.form = self.browser.find_element(
            By.XPATH,
            "/html/body/div[2]/form"
        )
        return self.form

    def select_fields(self):
        self.first_name = self.get_element_by_id(self.form, "id_first_name")
        self.last_name = self.get_element_by_id(self.form, 'id_last_name')
        self.username = self.get_element_by_id(self.form, 'id_username')
        self.email = self.get_element_by_id(self.form, 'id_email')
        self.password = self.get_element_by_id(self.form, 'id_password')
        self.password2 = self.get_element_by_id(self.form, 'id_password2')

    @parameterized.expand([
        ("id_first_name", "Nome não pode estar em branco"),
        ("id_last_name", "Sobrenome não pode estar em branco"),
        ("id_username", "Nome de usuário não pode estar em branco"),
        ("id_password", "Senha não pode estar em branco"),
    ])
    def test_first_name_field_does_not_accept_empty_values(self, field_id, msg):
        self.fill_form_dummy_data(self.form)
        self.get_element_by_id(self.form, "id_email").send_keys("email@invalid")
        field = self.get_element_by_id(self.form, field_id)
        field.send_keys(Keys.ENTER)
        self.select_form()
        self.assertIn(msg, self.form.text)

    def test_incorrect_email_field_message(self):
        self.fill_form_dummy_data(self.form)
        self.select_fields()
        self.email.send_keys(
            "email@invalid",
            Keys.ENTER
        )
        self.select_form()
        self.assertIn("Formato de email inválido", self.form.text)

    def test_passwords_do_not_match(self):
        self.fill_form_dummy_data(self.form)
        self.select_fields()
        self.password.send_keys("P@ssw0rd")
        self.password2.send_keys("An0th3rP@ssw0rd")
        self.email.send_keys("email@invalid", Keys.ENTER)
        self.select_form()
        self.assertIn("As senhas não conferem", self.form.text)

    def test_user_valid_data_register_successfully(self):
        form = self.select_form()
        self.select_fields()

        self.first_name.send_keys("Alek")
        self.last_name.send_keys("Intelcore")
        self.username.send_keys("Alek_Intelcore")
        self.email.send_keys("alek@intelcore.com")
        self.password.send_keys("Al3k1nt3lc0r3")
        self.password2.send_keys("Al3k1nt3lc0r3")
        
        form.submit()

        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Sua conta foi criada com sucesso", body)

    def fill_form_dummy_data(self, form: WebElement) -> None:
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)
