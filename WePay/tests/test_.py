from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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

    def test_login(self):
        self.browser.get('http://127.0.0.1:8000/accounts/login/')
        username_input = self.browser.find_element(By.NAME, 'login')
        password_input = self.browser.find_element(By.NAME, 'password')
        submit_button = self.browser.find_element(By.ID, 'submit')

        username_input.send_keys(self.header.name)
        username_input.send_keys(Keys.RETURN)
        password_input.send_keys(self.header.user.password)
        password_input.send_keys(Keys.RETURN)
        submit_button.click()

        assert 'header' in self.browser.page_source

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