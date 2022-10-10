from django.test import TestCase
from django.urls import resolve, reverse

from .. import views
from ..models import Category
from .base.base_recipe import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_class_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.Home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_loads_recipes(self):
        recipe = self.create_complete_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertTrue(response.context.get('recipes'))
        self.assertContains(response, recipe)
        self.assertIn(recipe.title, content)


class RecipeDetailViewTest(TestCase):
    def test_recipe_detail_view_class_is_correct(self):
        view = resolve(reverse('recipes:detail', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.DetailRecipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.status_code, 404)


class RecipeFilterByCategoryViewTest(TestCase):

    def test_recipe_filter_by_category_view_class_is_correct(self):
        view = resolve(
            reverse('recipes:filter_by_category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.FilterRecipesByCategory)

    def test_recipe_filter_by_category_view_returns_404_not_found(self):
        response = self.client.get(
            reverse('recipes:filter_by_category', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_filter_by_category_template_loads_filtered_recipes(self):
        category = Category.objects.create(name="Category")
        response = self.client.get(
            reverse(
                'recipes:filter_by_category',
                kwargs={'category_id': category.id}))
        self.assertEqual(response.status_code, 200)
