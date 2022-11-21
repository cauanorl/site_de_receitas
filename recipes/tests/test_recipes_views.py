from django.db.models import QuerySet
from django.http import HttpResponseRedirect
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
    def test_recipe_class_views_are_correct(self, namespace, view_class, params: dict = {}):
        view = resolve(reverse(namespace, kwargs={**params}))
        self.assertIs(view.func.view_class, view_class)

    @parameterized.expand([
        ('recipes:home',),
        ('recipes:search', {'q': 'Valor'}),
    ])
    def test_views_return_status_code_200_no_made_recipes(self, namespace, query={}):
        response = self.client.get(reverse(namespace), data={**query})
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ['recipes:detail', {'id': 1}],
        ['recipes:filter_by_category', {'category_id': 1}],
    ])
    def test_views_return_status_code_404_no_made_recipes(self, namespace, params={}):
        response = self.client.get(reverse(namespace, kwargs={**params}))
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        ('recipes:home', 'recipes/pages/home.html'),
        ('recipes:search', 'recipes/pages/home.html', {'q': 'q'}),
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

    def test_recipe_home_is_paginated(self):
        url = reverse('recipes:home')
        user = self.create_test_user()

        for n in range(10):
            self.make_random_recipe(
                author_data=user,
                title=f"recipe {n}",
                is_published=True,
            )

        response = self.client.get(url)
        page_obj = response.context.get('page_obj')

        self.assertEqual(page_obj.paginator.num_pages, 2)

    def test_recipe_home_is_paginated_by_nine_recipes(self):
        url = reverse('recipes:home')
        user = self.create_test_user()

        for n in range(10):
            self.make_random_recipe(
                author_data=user,
                title=f"recipe {n}",
                is_published=True,
            )

        response = self.client.get(url)
        page_obj = response.context.get('page_obj')

        self.assertEqual(len(page_obj), 9)


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_variable_is_named_correctly(self):
        query = "Teste"
        user = self.create_test_user()

        self.make_random_recipe(
            is_published=True, title=query, author_data=user)
        self.make_random_recipe(
            is_published=True, title=f'Etset', author_data=user)

        response = self.client.get(reverse('recipes:search'), data={
            'q': f'{query}'
        })

        self.assertEqual(
            len(response.context.get('recipes')),
            1,
            msg=f"Search variable is incorrect."
                f"query string for search must be named as 'q'."
        )

    def test_recipe_search_can_find_recipes_by_title_and_description(self):
        user = self.create_test_user()
        expected_recipes_number = 3
        search_query = "Teste"
        test_fields = [
            ('Teste de search', 'Description'),
            ("  TeStE  ", 'Teste'),
            ("Fácil search", 'Forbidden'),
            ('Título', "teste de description")
        ]

        for title, description in test_fields:
            self.make_random_recipe(
                is_published=True,
                title=title,
                author_data=user,
                description=description
            )

        response = self.client.get(
            reverse('recipes:search'), data={'q': search_query})

        query_set = response.context.get('recipes')

        self.assertEqual(
            len(query_set),
            expected_recipes_number,
            msg=f"The view doesn't load {expected_recipes_number} recipes "
                f"for search '{search_query}'"
                f"\nExpected: {expected_recipes_number}"
                f"\nGot: {len(query_set)}"
        )

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        query = "Teste"
        url = reverse('recipes:search')
        response = self.client.get(url, data={'q': query})

        self.assertIn(
            f'Searching for &quot;{query}&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_is_paginated(self):
        url = reverse('recipes:search')
        user = self.create_test_user()

        for n in range(10):
            self.make_random_recipe(
                author_data=user,
                title=f"recipe {n}",
                is_published=True,
            )

        response = self.client.get(url, data={'q': 'recipe'})
        page_obj = response.context.get('page_obj')

        self.assertEqual(page_obj.paginator.num_pages, 2)

    def test_recipe_search_context_object_name_is_correct(self):
        response = self.client.get(reverse('recipes:search'), data={'q': 'r'})

        self.assertIsInstance(response.context.get('recipes'), QuerySet)

    def test_recipe_search_redirects_to_home_page_if_no_query(self):
        res = self.client.get(reverse('recipes:search'), data={'q': ''})

        self.assertEqual(res.status_code, 302)
        self.assertIsInstance(res, HttpResponseRedirect)


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

    def test_recipe_detail_raises_a_http_404_if_recipe_is_not_published(self):
        recipe = self.make_random_recipe()

        response = self.client.get(
            reverse('recipes:detail', kwargs={'id': recipe.id})
        )

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
