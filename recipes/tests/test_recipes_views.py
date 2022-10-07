from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_class_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.Home)

    def test_recipe_detail_view_class_is_correct(self):
        view = resolve(reverse('recipes:detail', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.DetailRecipe)

    def test_recipe_filter_by_category_view_class_is_correct(self):
        view = resolve(
            reverse('recipes:filter_by_category', kwargs={'category_id': 1}))

        self.assertIs(view.func.view_class, views.FilterRecipesByCategory)
