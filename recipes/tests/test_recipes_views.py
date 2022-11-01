from django.urls import resolve, reverse
from parameterized import parameterized

from .. import views
from .base.base_recipe import RecipeTestBase


class RecipeCommunViewsTests(RecipeTestBase):
    @parameterized.expand([
        ('recipes:home', views.Home),
        ('recipes:search', views.SearchRecipes),
        ('recipes:detail', views.DetailRecipe, {'id': 1}),
        ('recipes:filter_by_category',
         views.FilterRecipesByCategory, {'category_id': 1})
    ])
    def test_recipe_class_views_is_correct(self, namespace, view_class, extra: dict = {}):
        view = resolve(reverse(namespace, kwargs={**extra}))
        self.assertIs(view.func.view_class, view_class)

    @parameterized.expand([
        ('recipes:home',),
        ('recipes:search', {'search': 'Valor'}),
    ])
    def test_views_return_status_code_200_no_made_recipes(self, namespace, query={}):
        response = self.client.get(reverse(namespace), data={**query})
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ['recipes:detail', {'id': 1}],
        ['recipes:filter_by_category', {'category_id': 1}],
    ])
    def test_views_return_status_code_404_no_made_recipes(self, namespace, extra={}):
        response = self.client.get(reverse(namespace, kwargs={**extra}))
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        ('recipes:home', 'recipes/pages/home.html'),
        ('recipes:search', 'recipes/pages/home.html', {'search': 'q'}),
    ])
    def test_views_load_the_correct_templates(self, namespace, template_path, query: dict = {}):
        response = self.client.get(
            reverse(namespace), data={**query})
        self.assertTemplateUsed(
            response,
            template_path,
            msg_prefix=f"The {template_path} isn't used by {namespace}"
        )


class RecipeHomeViewTest(RecipeTestBase):

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


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_is_rendering_the_correct_recipes(self):
        user = self.create_test_user()
        query = "Teste"
        test_titles = ['Teste de search', "  TeStE  ", "Fácil search"]

        for title in test_titles:
            self.make_random_recipe(
                is_published=True,
                title=title,
                author_data=user
            )

        response = self.client.get(
            reverse('recipes:search'), data={'search': query})

        query_sets = response.context.get('recipes')

        self.assertEqual(len(query_sets), 2)


class RecipeDetailViewTest(RecipeTestBase):

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
