from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual('/', home_url)

    def test_recipe_detail_url_is_correct(self):
        detail_url = reverse('recipes:detail', args=[1])
        self.assertEqual('/recipe/1/', detail_url)

    def test_recipe_filter_by_category_url_is_correct(self):
        filter_by_category_url = reverse(
            'recipes:filter_by_category', kwargs={'category_id': 1})

        self.assertEqual('/recipe/category/1/', filter_by_category_url)
