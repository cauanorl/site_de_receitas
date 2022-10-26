from django.core.exceptions import ValidationError

from parameterized import parameterized

from .base.base_recipe import RecipeTestBase


class RecipeModelsTest(RecipeTestBase):
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
                msg=f"{field_name} didn't raise a ValidationError"
            ):

            self.recipe.full_clean()

    def test_recipe_are_the_preparation_steps_html_is_false_by_default(self):
        self.assertFalse(self.recipe.are_the_preparation_steps_html)

    def test_recipe_is_published_is_false_by_default(self):
        self.assertFalse(self.recipe.is_published)
