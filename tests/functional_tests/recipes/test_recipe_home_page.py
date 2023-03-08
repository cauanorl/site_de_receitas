import pytest

from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_home_page_no_recipes_found_message(self):
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(
            "Nenhuma receita publicada no momento",
            body_text
        )
        

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
