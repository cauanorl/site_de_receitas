from unittest import TestCase

from django.forms.utils import ErrorList
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from ..forms import RegisterForm


class AuthorRegisterFormTests(TestCase):
    @parameterized.expand([
        ('first_name',),
        ('last_name',),
        ('username',),
        ('email',),
        ('password',),
        ('password2',),
    ])
    def test_fields_have_a_placeholder(self, field):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs.get('placeholder')

        self.assertTrue(
            placeholder,
            f"Field {field} doesn't have a placeholder"
        )

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Nome de usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Repetir senha'),
    ])
    def test_fields_labels(self, field, label):
        form = RegisterForm()
        field_label = form[field].label
        self.assertEqual(
            label, field_label,
            msg=f"{field_label} != {label} on {field}"
        )


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'first_name': 'Cauan',
            'last_name': 'Rodrigues',
            'username': 'userOrl',
            'password': 'user12435687',
            'password2': 'user12435687',
            'email': 'email@anyemail.com',
        }
        self.register_url = reverse('authors:register')

        return super().setUp()

    @parameterized.expand([
        ("username", 'Este campo é obrigatório'),
        ("password", 'Senha não pode estar em branco'),
        ("email", 'Email não pode estar em branco'),
        ("first_name", 'Este campo é obrigatório'),
        ("last_name", 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        response = self.client.post(self.register_url, data=self.form_data)
        form: RegisterForm = response.context.get('form')
        self.assertIn(msg, form.errors.get(field)[0])

    @parameterized.expand([
        ('username', 'Nome de usuário deve conter no máximo 150 caracteres'),
        ('first_name', 'Nome deve conter no máximo 150 caracteres'),
        ('last_name', 'Sobrenome deve conter no máximo 150 caracteres'),
        ('email', 'Email não deve conter mais de 150 caracteres', True),
    ])
    def test_fields_max_length(self, field, msg, email=False):
        MAX_LENGTH = 150
        data = 'a' * (MAX_LENGTH + 1) if not email else ('a' *
                                                         150) + ('@email.com')

        self.field_has_the_expected_error(
            field,
            {field:  data},
            msg,
            f'"{msg}" not found in error list'
        )

    @parameterized.expand([
        ('username', 6, 'Nome de usuário deve conter mais de 6 caracteres'),
        ('password', 8, 'A senha deve conter no minímo 8 caracteres'),
        ('first_name', 2, 'Primeiro nome deve conter mais que 2 caracteres'),
        ('last_name', 2, 'Sobrenome deve conter mais que 2 caracteres'),
    ])
    def test_fields_min_length(self, field, min_length, msg):
        self.field_has_the_expected_error(
            field,
            {field: 'a' * (min_length - 1)},
            msg,
            f'"{msg}" not found in error list'
        )

    def test_password_has_at_least_one_number(self):
        field = 'password'
        password_without_numbers = 'testepassword'
        expected_error = 'A senha deve conter letras e números'
        failed_test_msg = (
            f"Password '{password_without_numbers}' "
            f"shouldn't have been passed, but it was")

        fields_to_update = {
            'password': password_without_numbers,
            'password2': password_without_numbers
        }

        self.field_has_the_expected_error(
            field,
            fields_to_update,
            expected_error,
            failed_test_msg
        )

    def test_password_has_at_least_one_letter(self):
        field = 'password'
        password_only_numbers = '1234987601'
        expected_error = 'A senha deve conter letras e números'
        failed_test_msg = (
            f"Password '{password_only_numbers}' shouldn't "
            f"have been passed, but it was"
        )

        fields_to_update = {
            'password': password_only_numbers,
            'password2': password_only_numbers
        }

        self.field_has_the_expected_error(
            field,
            fields_to_update,
            expected_error,
            failed_test_msg
        )

    def test_password_has_at_least_8_characters(self):
        field = 'password'
        password = 'abc1234'
        expected_error = 'A senha deve conter no minímo 8 caracteres'
        failed_test_msg = (
            f"Password '{password}' shouldn't have been passed, but it was"
        )
        fields_to_update = {
            'password': password,
            'password2': password
        }

        self.field_has_the_expected_error(
            field,
            fields_to_update,
            expected_error,
            failed_test_msg
        )

    def test_correct_password(self):
        password = 'user12345678'
        self.form_data['password'] = password
        self.form_data['password2'] = password
        response = self.client.post(
            self.register_url,
            data=self.form_data,
        )

        self.assertEqual(
            response.status_code,
            302,
            msg=f"Password '{password}' didn't pass, "
                f"but should have been passed"
        )

    def test_password_is_equal_to_password2(self):
        field = 'password2'
        password1 = 'user12345678'
        password2 = '12345678user'
        expected_error = 'As senhas não conferem'
        failed_test_msg = (
            'Password was not equal to Password2, but it did not raise an error'
        )

        fields_to_update = {
            'password': password1,
            'password2': password2
        }

        self.field_has_the_expected_error(
            field,  
            fields_to_update,
            expected_error,
            failed_test_msg
        )

    def test_email_field_must_be_unique(self):
        for _ in range(2):
            response = self.client.post(self.register_url, data=self.form_data)

        errors_list = response.context.get('form').errors.get('email')
        self.assertIn(
            'Este email já foi cadastrado',
            errors_list,
        )
        self.assertEqual(
            response.status_code,
            200,
            "Email shouldn't have been passed, but it was"
        )

    def test_user_created_can_login(self):
        self.client.post(self.register_url, data=self.form_data)
        is_authenticated = self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password'],
        )

        self.assertTrue(
            is_authenticated,
            f"Login failed to user: {self.form_data['username']}"
        )

    def field_has_the_expected_error(
        self,
        field: str,
        fields_to_update: dict,
        expected_error: str,
        failed_test_msg: str,
    ):
        self.form_data.update(fields_to_update)

        response = self.client.post(self.register_url, data=self.form_data)
        form: RegisterForm = response.context.get('form')

        has_error = self.find_error(
            form.errors.get(field),
            expected_error
        )

        self.assertTrue(
            has_error,
            msg=failed_test_msg
        )

    @staticmethod
    def find_error(errors: ErrorList, msg: str):
        try:
            errors = list(errors)
        except TypeError:
            errors = []

        for error in errors:
            if msg == error:
                return True

        return False
