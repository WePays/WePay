from unittest import skip
from selenium.common.exceptions import NoSuchElementException
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class E2ETestDeploy(LiveServerTestCase):
    def setUp(self):
        """Setup before test"""
        options = ChromeOptions()
        options.add_argument("start-maximized")
        self.browser = Chrome(options=options)

    # Test with deploy web
    def login_with_deploy_web(self):
        """login function"""
        username = "wepay"
        password = "wepay123"
        self.browser.get("https://wepays.herokuapp.com/accounts/login/")
        self.browser.find_element(By.ID, "id_login").send_keys(username)
        self.browser.find_element(By.ID, "id_password").send_keys(password)
        self.browser.find_element(By.ID, "id_submit").click()

    def test_login_with_deploy_web(self):
        """Test login with deploy web."""
        self.login_with_deploy_web()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/bill/")

    def test_navigation_in_bill_page_with_deploy_web(self):
        """Test navigation in bill page with deploy web"""
        self.login_with_deploy_web()
        self.browser.implicitly_wait(10)
        # click bill button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[2]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/bill/")
        #click payment button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[3]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/payment/")
        #click history button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[4]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/history/")
        #click instruction button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[5]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/instruction/")
        #click aboutus button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[6]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/about/")
        #click logout button
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[7]").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/accounts/logout/")
        #click signout button
        self.browser.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/accounts/login/")

    def test_update_display(self):
        """Test for update display"""
        self.login_with_deploy_web()
        self.browser.implicitly_wait(5)
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[1]").click() #click userprofile
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/user-profile/")
        self.browser.find_element(By.NAME, "display name").clear()
        self.browser.find_element(By.NAME, "display name").send_keys("Halo")
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/form/div/button").click() #update userprofile
        self.assertEqual(self.browser.find_element(By.NAME, "display name").is_displayed(), True)
        self.browser.find_element(By.NAME, "display name").clear()
        self.browser.find_element(By.NAME, "display name").send_keys("wepay") #change back to Wepay
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/form/div/button").click() #update userprofile
        self.assertEqual(self.browser.find_element(By.NAME, "display name").is_displayed(), True)

    def test_create_bill_and_add_topic_with_deploy_web(self):
        """Test create bill & add topic with deploy web"""
        self.login_with_deploy_web()
        self.browser.implicitly_wait(5)
        #click create bill button #TODO add name into create button html.
        # self.browser.find_element(By.XPATH, "/html/body/div[2]/form/button").click() #This is the button when no bills
        self.browser.find_element(By.XPATH, "/html/body/div[3]/form/button").click() #This button when user have bills.
        # if user have initialize bill its will goes to bill page
        if self.browser.current_url == "https://wepays.herokuapp.com/bill/":
            self.browser.find_element(By.XPATH, "/html/body/h3/a").click()
        if self.browser.current_url == "https://wepays.herokuapp.com/bill/create/":
            # This is create bill page
            self.browser.find_element(By.NAME, "title").send_keys("KU COURT!")
            self.browser.find_element(By.NAME, "topic_name").send_keys("Chicken")
            self.browser.find_element(By.NAME, "topic_price").send_keys(2000)
            self.browser.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div[1]/input").click() # open select user
            # select three user at top
            self.browser.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div[2]/div/div[1]").click()
            self.browser.find_element(By.XPATH, "/html/body/div[2]/form/div[5]/div/div/div[2]/div/div[4]").click()
            self.browser.implicitly_wait(5)
            self.browser.find_element(By.NAME, "create_title").click()
        # This should goes to add topic page
        self.assertNotEqual(self.browser.current_url, "https://wepays.herokuapp.com/bill/create/") # But I still confused how to test with pk url.
        self.browser.find_element(By.NAME, "topic_name").send_keys("Udon")
        self.browser.find_element(By.NAME, "topic_price").send_keys(2000)
        self.browser.find_element(By.ID, "username-ts-control").click() #open select user
        self.browser.implicitly_wait(5)
        # select three user at top
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/div/div[2]/div/div[1]").click()
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/div/div[2]/div/div[4]").click()
        self.browser.find_element(By.ID, "username-ts-control").click() #close select user
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/div[4]/button").click() # add topic
        self.browser.implicitly_wait(20)
        self.browser.find_element(By.NAME, "create_button").click() # create bill
        # redirect back to bills page
        self.assertEqual(self.browser.current_url, "https://wepays.herokuapp.com/bill/")

    def test_payment_and_verify(self):
        """Test payment and verify"""
        #TODO try to add user toastwepay in test_create_bill_and_add_topic_with_deploy_web
        username1 = "toastwepay"
        password1 = "wepay123"

    def test_delete_button(self):
        """Test delete button"""
        self.test_create_bill_and_add_topic_with_deploy_web()
        self.browser.implicitly_wait(5)
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/a[2]").click()
        #delete button
        self.browser.implicitly_wait(5)
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody[1]/tr/td[6]/a").click() # delete first bill
