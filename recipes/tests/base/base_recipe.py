from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from recipes.models import Category, Recipe


class RecipeTestBase(TestCase):
    fake = Faker('pt_BR')

    def _make_fake_recipe(self, **recipe_fields: dict[str, str]) -> dict:
        recipe = {
            'title': recipe_fields.get(
                'title',
                self.fake.sentence(nb_words=6)
            ),
            'description': recipe_fields.get(
                'description',
                self.fake.sentence(nb_words=6)
            ),
            'preparation_time': recipe_fields.get(
                'preparation_time', 
                self.fake.random_number(digits=2, fix_len=True)
            ),
            'preparation_time_unit': recipe_fields.get(
                'preparation_time_unit',
                'M'
            ),
            'servings': recipe_fields.get(
                'servings',
                self.fake.random_number(digits=2, fix_len=True)
            ),
            'servings_unit': recipe_fields.get(
                'servings_unit',
                "Porção"
            ),
            'preparation_steps': recipe_fields.get(
                'preparation_steps',
                self.fake.text(3000)
            ),
        }

        is_published = recipe_fields.get('is_published')
        are_the_preparation_steps_html = recipe_fields.get('are_the_preparation_steps_html')

        if is_published:
            recipe.update({'is_published': is_published})

        if are_the_preparation_steps_html:
            recipe.update({'are_the_preparation_steps_html': are_the_preparation_steps_html})

        return recipe

    def create_test_user(self, *args, **fields: dict[str, str]) -> User:
        return User.objects.create_user(
            first_name=fields.get('first_name', "First"),
            last_name=fields.get("last_name", "Last"),
            username=fields.get("username", "test_username"),
            email=fields.get('email', 'email@email.com'),
            password=fields.get('password', '123test321')
        )

    def create_category_for_tests(self, name="Category") -> Category:
        return Category.objects.create(name=name)

    def create_random_recipe(
        self,
        category: Category,
        author: User,
        **recipe_fields: dict[str, str]
    ):
        return Recipe.objects.create(
            **self._make_fake_recipe(**recipe_fields),
            slug="slug-test",
            cover='https://loremflickr.com/300/300/',
            author=author,
            category=category,
        )

    def make_random_recipe(
            self,
            author_data: dict[str, str] = {},
            category_name: str = "Test category",
            **recipe_fields: dict[str, str]
        ) -> Recipe:
        author = self.create_test_user(**author_data)
        category = self.create_category_for_tests(name=category_name)

        return self.create_random_recipe(category, author, **recipe_fields)
