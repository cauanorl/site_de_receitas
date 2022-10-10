from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from recipes.models import Category, Recipe


class RecipeTestBase(TestCase):
    fake = Faker('pt_BR')

    def _make_recipe(self) -> dict:
        return {
            'title': self.fake.sentence(nb_words=6),
            'description': self.fake.sentence(nb_words=6),
            'preparation_time': self.fake.random_number(digits=2, fix_len=True),
            'preparation_time_unit': 'Minutos',
            'servings': self.fake.random_number(digits=2, fix_len=True),
            'servings_unit': "Porção",
            'preparation_steps': self.fake.text(3000),
            'is_published': True,
        }

    def create_test_user(self, *args, **fields) -> User:
        return User.objects.create_user(
            first_name=fields.get('first_name', "First"),
            last_name=fields.get("last_name", "Last"),
            username=fields.get("username", "test_username"),
            email=fields.get('email', 'email@email.com'),
            password=fields.get('password', '123test321')
        )

    def create_category_for_tests(self, name="Category") -> Category:
        return Category.objects.create(name=name)

    def create_random_recipe(self, category: Category, author: User):
        return Recipe.objects.create(
            **self._make_recipe(),
            slug="slug-test",
            cover='https://loremflickr.com/300/300/',
            author=author,
            category=category,
        )

    def create_complete_recipe(self) -> Recipe:
        author = self.create_test_user()
        category = self.create_category_for_tests()

        return self.create_random_recipe(category, author)
