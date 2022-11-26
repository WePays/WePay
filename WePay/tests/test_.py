from unittest import skip

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from WePay.models.userprofile import UserProfile


class BillFormTest(LiveServerTestCase):
    def setUp(self):
        header = User.objects.create_user(
            username="header", email="header@example.com", password="header123"
        )
        self.header = UserProfile.objects.create(
            user=header, chain_id="acch_test_5tl5qdsa0cbli76hwoj"
        )
        self.header.save()

        user = User.objects.create_user(
            username="test_user", email="user1@example.com", password="user"
        )
        self.user = UserProfile.objects.create(user=user)
        self.user.save()
        # self.client.force_login(self.header)
        self.browser = webdriver.Chrome()

    # @skip("Temporalily skip")
    def test_login(self):
        # url to visit
        self.browser.get("http://127.0.0.1:8000/accounts/login/")

        # find the elements we need to submit form
        username_input = self.browser.find_element(By.ID, "id_login")
        password_input = self.browser.find_element(By.ID, "id_password")
        submit_button = self.browser.find_element(By.ID, "id_submit")

        # populate the form with data
        username_input.send_keys(self.header.name)
        password_input.send_keys(self.header.user.password)

        # submit form
        # submit_button.send_keys(Keys.RETURN)
        # click the button to login
        submit_button.click()

        # assert "header" in self.browser.page_source

    @skip("it still not work, i will try later after reading a selenium docs")
    def test_initialize_bill_form(self):

        self.browser.get("http://127.0.0.1:8000/accounts/login/")

        # find the elements we need to submit form
        username_input = self.browser.find_element(By.ID, "id_login")
        password_input = self.browser.find_element(By.ID, "id_password")
        submit_button = self.browser.find_element(By.ID, "id_submit")

        # populate the form with data
        username_input.send_keys(self.header.name)
        password_input.send_keys(self.header.user.password)

        # submit form
        submit_button.click()

        self.browser.implicitly_wait(20)

        self.browser.get("http://127.0.0.1:8000/bill/create/")

        title = self.browser.find_element(By.XPATH, "//input[@id='title']")
        name = self.browser.find_element(By.ID, "topic_name")
        price = self.browser.find_element(By.ID, "topic_price")
        assign_to_users = self.browser.find_elements(By.ID, "username")
        # assign_to_users = self.browser.find_elements(By.XPATH, )

        create = self.browser.find_element(By.NAME, "create_title")

        title.send_keys("Test Title")
        name.send_keys("Test Food")
        price.send_keys(100)
        assign_to_users.send_keys("test_user")

        create.send_keys(Keys.Return)

    #     assert 'Test Title' in self.browser.page_source

    def tearDown(self):
        self.browser.close()
