from django.urls import resolve, reverse

from .. import views
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
        recipe = self.make_random_recipe(is_published=True)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertTrue(response.context.get('recipes'))
        self.assertContains(response, recipe)
        self.assertIn(recipe.title, content)

    def test_recipe_home_template_loads_only_published_recipes(self):
        published_recipe = self.make_random_recipe(
            author_data={'username': 'user1'},
            is_published=True,
            slug="teste-1"
        )
        not_published_recipe = self.make_random_recipe(
            author_data={'username': 'user2'},
            slug='teste-2'
        )

        response = self.client.get(reverse('recipes:home'))

        self.assertNotContains(response, not_published_recipe)
        self.assertContains(response, published_recipe)


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_class_is_correct(self):
        view = resolve(reverse('recipes:detail', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.DetailRecipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It loads one recipe"

        recipe = self.make_random_recipe(title=needed_title, is_published=True)
        response = self.client.get(reverse('recipes:detail', args=[recipe.id]))

        self.assertContains(response, recipe)

    def test_recipe_detail_template_does_not_load_unpublished_recipes(self):
        not_published_recipe = self.make_random_recipe(
            author_data={'username': 'user2'}, is_published=False)

        response = self.client.get(
            reverse('recipes:detail', args=[not_published_recipe.id]))

        self.assertEqual(response.status_code, 404)


class RecipeFilterByCategoryViewTest(RecipeTestBase):

    def test_recipe_filter_by_category_view_class_is_correct(self):
        view = resolve(
            reverse('recipes:filter_by_category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.FilterRecipesByCategory)

    def test_recipe_filter_by_category_view_returns_404_not_found(self):
        response = self.client.get(
            reverse('recipes:filter_by_category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_filter_by_category_template_loads_filtered_recipes(self):
        breakfast_recipe = self.make_random_recipe(
            category_name="Breakfast",
            author_data={'username': 'user1'},
            is_published=True,
            slug="teste-1"
        )
        dinner_recipe = self.make_random_recipe(
            category_name="Dinner",
            author_data={'username': 'user2'},
            is_published=True,
            slug="teste-2"
        )

        response = self.client.get(
            reverse(
                'recipes:filter_by_category',
                kwargs={'category_id': breakfast_recipe.category.id}))

        self.assertContains(response, breakfast_recipe)
        self.assertNotContains(response, dinner_recipe)
        self.assertEqual(response.status_code, 200)

    def test_recipe_filter_by_category_template_does_not_load_unpublished_recipes(self):
        breakfast_recipe = self.make_random_recipe(
            category_name="Breakfast",
            is_published=False,
        )

        response = self.client.get(
            reverse(
                'recipes:filter_by_category',
                kwargs={'category_id': breakfast_recipe.category.id}))

        self.assertNotContains(response, breakfast_recipe)
