# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.tests.base.base_recipe import RecipeMixin

class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def sleep(self, seconds: int = 2):
        time.sleep(seconds)

    def setUp(self, *args, **kwargs):
        self.browser = make_chrome_browser()
        return super().setUp(*args, **kwargs)


    def tearDown(self, *args, **kwargs):
        self.browser.close()
        self.browser.quit()
        return super().tearDown(*args, **kwargs)
