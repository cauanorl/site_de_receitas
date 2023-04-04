from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from parameterized import parameterized

from ..models import Category
from .base.base_recipe import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_random_recipe()
        return super().setUp()

    @parameterized.expand([
        ("title", 65),
        ("description", 165),
        ("servings_unit", 65),
    ])
    def test_recipe_fields_max_length(self, field_name, max_length):

        setattr(self.recipe, field_name, ("a" * (max_length + 1)))
        with self.assertRaises(
                ValidationError,
                msg=f"{field_name} didn't raise a ValidationError"):

            self.recipe.full_clean()

    def test_recipe_are_the_preparation_steps_html_is_false_by_default(self):
        self.assertFalse(self.recipe.are_the_preparation_steps_html)

    def test_recipe_is_published_is_false_by_default(self):
        self.assertFalse(self.recipe.is_published)

    def test_recipe_slug_field_is_unique(self):
        other_recipe = self.make_random_recipe(
            author_data={
                'username': 'Alek',
                'password': 'teste123'
            })

        with self.assertRaises(
            IntegrityError,
            msg="The slug field in Recipes don't raise an IntegrityError. "
                "The slug fields aren't the same."
        ):
            self.recipe.title = other_recipe.title
            self.recipe.save()


class CategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = Category.objects.create(name="test category")
        return super().setUp()

    def test_category_name_field_raises_an_error_if_max_length_is_greater_than_30_chars(self): # noqa
        self.category.name = "a" * 31
        self.assertRaises(
            ValidationError,
            self.category.full_clean,
        )

    def test_category_string_representation_is_name_field(self):
        self.assertEqual(str(self.category), self.category.name)
