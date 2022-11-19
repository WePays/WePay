from unittest import skip

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
        # self.client.force_login(self.header)
        self.browser = webdriver.Chrome()

    # @skip("ERR_CONNECTION_REFUSED")
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
        submit_button.send_keys(Keys.RETURN)

        # assert "header" in self.browser.page_source

    # def test_create_bill_form(self):
    #     self.browser.get('http://127.0.0.1:8000/bill/create/')

    #     title = self.browser.find_element(By.NAME,'title')
    #     name = self.browser.find_element(By.NAME, 'topic_name')
    #     price = self.browser.find_element(By.NAME, 'topic_price')

    #     submit = self.browser.find_element(By.NAME, 'create_title')

    #     title.send_keys('Test Title')
    #     name.send_keys('Test Food')
    #     price.send_keys('100')

    #     submit.send_keys(Keys.Return)

    #     assert 'Test Title' in self.browser.page_source

    def tearDown(self):
        self.browser.close()
