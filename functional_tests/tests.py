from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


# A person can navigate to the home page of the site
# and see a list of users
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_can_navigate_to_home_page(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('Profiles', self.browser.title)

# A person can navigate to a profile on the home page via a link,
# and view the user profile

# User can log in

# logged in user can edit their own profile