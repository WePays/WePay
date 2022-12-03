from unittest import skip

from django.contrib.auth.models import User
from django.test import Client, LiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from WePay.models.userprofile import UserProfile


class E2ETestLocal(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
        header = User.objects.create_user(
            username="header", email="header@example.com", password="header123"
        )
        header.save()
        self.header = UserProfile.objects.create(
            user=header, chain_id="acch_test_5tl5qdsa0cbli76hwoj"
        )
        self.header.save()
        user = User.objects.create_user(
            username="test_user", email="user1@example.com", password="user"
        )
        user.save()
        self.user = UserProfile.objects.create(user=user)
        self.user.save()
        self.browser = Chrome()
        # self.browser.get(self.live_server_url + "/accounts/login/")
        # self.browser.get("http://127.0.0.1:8000/accounts/login/")
        self.browser.implicitly_wait(5)
        self.browser.set_page_load_timeout(30)
        self.browser.get(self.live_server_url)

    def login(self):
        self.client.login(username=self.header.name, password="header123")
        cookie = self.client.cookies['sessionid']
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "path": "/",
            }
        )
        self.browser.refresh()

    # @skip("Temporalily skip")
    def test_login(self):
        # url to visit
        # self.browser.get("http://127.0.0.1:8000/accounts/login/")
        self.browser.get(self.live_server_url)
        # find the elements we need to submit form
        username_input = self.browser.find_element(By.ID, "id_login")
        password_input = self.browser.find_element(By.ID, "id_password")
        submit_button = self.browser.find_element(By.ID, "id_submit")

        username_input.send_keys(self.header.name)
        password_input.send_keys(self.header.user.password)

        # submit button
        submit_button.click()

    #     assert "header" in self.browser.page_source

    # @skip("it still not work, i will try later after reading a selenium docs")
    def test_initial_bill(self):

        self.login()

        self.browser.get(self.live_server_url + reverse("bills:create"))

        title = self.browser.find_element(By.XPATH, "//input[@id='title']")
        name = self.browser.find_element(By.ID, 'topic_name')
        price = self.browser.find_element(By.ID, 'topic_price')
        assign_to_users = self.browser.find_element(By.TAG_NAME, 'select')
        # assign_to_users = self.browser.find_elements(By.XPATH, )

        create_title = self.browser.find_element(By.NAME, 'create_title')

        title.send_keys('Test Title')
        name.send_keys('Test Food')
        price.send_keys(100)
        assign_to_users.send_keys(self.user.name)
        # users = assign_to_users.text.split('\n')
        self.assertIn('test_user', assign_to_users.text.split('\n'))
        # self.assertEqual('test_user', users[len(users) - 1])

        create_title.click()

    def test_create_bill(self):

        self.login()

        self.browser.get(self.live_server_url + reverse("bills:create"))

        # title = self.browser.find_element(By.XPATH, "//input[@id='title']")
        # name = self.browser.find_element(By.ID, 'topic_name')
        # price = self.browser.find_element(By.ID, 'topic_price')
        # assign_to_users = self.browser.find_element(By.TAG_NAME, 'select')
        # create_title = self.browser.find_element(By.NAME, 'create_title')

        self.browser.find_element(By.XPATH, "//input[@id='title']").send_keys('Test Title') # Bill title
        self.browser.find_element(By.ID, 'topic_name').send_keys('Test Food') # Topic name
        self.browser.find_element(By.ID, 'topic_price').send_keys(100) # Topic price
        self.assertIn('test_user', self.browser.find_element(By.TAG_NAME, 'select').text.split('\n')) # Assign to user

        self.browser.find_element(By.NAME, 'create_title').click()

        self.browser.find_element(By.NAME, 'topic_name').send_keys('Test Food') # Topic name
        self.browser.find_element(By.NAME, 'topic_price').send_keys(100) # Topic price
        self.browser.find_element(By.TAG_NAME, 'select').send_keys(self.user.name) # Assign to user (topic)

        self.browser.find_element(By.TAG_NAME, 'button').click() # Create topic

        self.browser.find_element(By.NAME, 'create_button').click() # Create bill

    def test_delete_topic(self):

        self.test_initial_bill()

        # self.browser.find_element(By.XPATH, "//input[@id='title']").send_keys('Test Title') # Bill title
        # self.browser.find_element(By.ID, 'topic_name').send_keys('Test Food') # Topic name
        # self.browser.find_element(By.ID, 'topic_price').send_keys(100) # Topic price
        # self.assertIn('test_user', self.browser.find_element(By.TAG_NAME, 'select').text.split('\n')) # Assign to user

        # self.browser.find_element(By.NAME, 'create_title').click()

        self.browser.find_element(By.NAME, 'topic_name').send_keys('Test Food') # Topic name
        self.browser.find_element(By.NAME, 'topic_price').send_keys(100) # Topic price
        self.browser.find_element(By.TAG_NAME, 'select').send_keys(self.user.name) # Assign to user (topic)

        self.browser.find_element(By.TAG_NAME, 'button').click() # Create topic

        self.browser.find_element(By.XPATH, 'html/body/div[2]/div/table/tbody[1]/tr/td[5]/a').click() # Delete Topic

    def test_delete_bill(self):

        self.test_create_bill()

        self.browser.find_element(By.XPATH, 
            "/html/body/div[2]/div/div/table/tbody[1]/tr/td[6]/a").click() # Delete bill


    def tearDown(self):
        self.browser.close()
