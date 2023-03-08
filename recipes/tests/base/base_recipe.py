from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from recipes.models import Category, Recipe
from django.template.defaultfilters import slugify


class RecipeMixin:
    fake = Faker('pt_BR')

    def _make_fake_recipe(self, **recipe_fields: dict[str, str]) -> dict:
        title = self.fake.sentence(nb_words=6)

        recipe = {
            'title': recipe_fields.get(
                'title',
                title
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
            'slug': slugify(title),
        }

        is_published = recipe_fields.get('is_published')
        are_the_preparation_steps_html = recipe_fields.get('are_the_preparation_steps_html')

        if is_published:
            recipe.update({'is_published': is_published})

        if are_the_preparation_steps_html:
            recipe.update({'are_the_preparation_steps_html': are_the_preparation_steps_html})

        return recipe

    def make_recipes(self, num_of_recipes: int = 10) -> list[Recipe]:
        recipes = []

        for n in range(num_of_recipes):
            user = self.create_test_user(
                username=f"TestUser{n * 17}",
                email=f"user{n * 17}@email.com"
            )

            recipe = self.make_random_recipe(
                author_data=user,
                title=f"recipe {n}",
                is_published=True,
            )
            recipes.append(recipe)
        
        return recipes

    def create_test_user(self, **fields: dict[str, str]) -> User:
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
            cover='https://loremflickr.com/300/300/',
            author=author,
            category=category,
        )

    def make_random_recipe(
            self,
            author_data: dict[str, str] | User = {},
            category_name: str | Category = "Test category",
            **recipe_fields: dict[str, str]
        ) -> Recipe:

        author = author_data
        category = category_name

        if isinstance(author_data, dict):
            author = self.create_test_user(**author_data)

        if isinstance(category_name, str):
            category = self.create_category_for_tests(name=category_name)

        return self.create_random_recipe(category, author, **recipe_fields)


class RecipeTestBase(TestCase, RecipeMixin):
    ...
