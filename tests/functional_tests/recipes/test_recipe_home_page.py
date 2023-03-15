from unittest.mock import patch

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.models import Recipe

from .base import RecipeBaseFunctionalTest



PATCH_PER_PAGE = 2

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_home_page_no_recipes_found_message(self):
        self.browser.get(self.live_server_url)

        body_text = self.browser.find_element(By.TAG_NAME, "body").text

        self.assertIn(
            "Nenhuma receita publicada no momento",
            body_text
        )

    @patch("recipes.views.PER_PAGE", new=PATCH_PER_PAGE)
    def test_input_search_not_found_recipes_with_name_abc(self):
        self.browser.get(self.live_server_url)

        self.browser \
            .find_element(By.ID, "search_recipes") \
            .send_keys("Abc", Keys.ENTER)

        body_text = self.browser.find_element(By.TAG_NAME, "body").text

        self.assertIn(
            "Nenhuma receita para a pesquisa: Abc",
            body_text
        )

    @patch("recipes.views.PER_PAGE", new=PATCH_PER_PAGE)
    def test_input_search_can_find_recipes(self):
        search_query = "bolo"

        self.make_recipes(20)
        self.make_random_recipe(
            is_published=True, title="Como preparar um bolo"
        )

        self.browser.get(self.live_server_url)
        self.browser\
            .find_element(By.ID, "search_recipes")\
            .send_keys(search_query, Keys.ENTER)

        elements = self.browser.find_elements(
            By.CLASS_NAME, "recipe-list-item")

        self.assertTrue(elements)

        for element in elements:
            self.assertIn(search_query, element.text)

    @patch("recipes.views.PER_PAGE", new=PATCH_PER_PAGE)
    def test_recipe_home_page_pagination(self):
        quantity_of_recipes = 20
        per_page = 2

        number_of_pages = self.calc_number_of_pages(
            quantity_of_recipes, per_page)

        self.make_recipes(quantity_of_recipes)

        self.browser.get(self.live_server_url)

        for page_number in range(2, number_of_pages + 1):
            pagianation_content = self.browser \
                .find_element(By.CLASS_NAME, "pagination-content")

            e = pagianation_content\
                .find_element(By.CSS_SELECTOR, f'a[href="?page={page_number}"]')

            e.click()

        pagianation_content = self.browser \
            .find_element(By.CLASS_NAME, "pagination-content")

        with self.assertRaises(NoSuchElementException):
            e = pagianation_content.find_element(
                By.CSS_SELECTOR, f'a[href="?page={number_of_pages + 1}"]')

        with self.assertRaises(NoSuchElementException):
            # Current page
            e = pagianation_content.find_element(
                By.CSS_SELECTOR, f'a[href="?page={number_of_pages}"]')

    @staticmethod
    def calc_number_of_pages(quantity_of_recipes, per_page):
        number_of_pages = 1 if (quantity_of_recipes % per_page) != 0 else 0
        number_of_pages += quantity_of_recipes // per_page

        return number_of_pages
