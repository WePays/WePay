from django.urls import reverse

from WePay.models.bill import Topic
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from ..models import UserProfile, Bills
from django.utils import timezone
from unittest import skip


class BaseViewTest(BaseSetUp):
    def setUp(self):
        """Setup before running a tests."""
        super(BaseViewTest, self).setUp()
        self.test_header = User.objects.create(username="test_header")
        self.test_header.set_password("header123")
        self.user_profile = UserProfile.objects.create(user=self.test_header)
        self.user_profile.save()
        self.client.login(username="test_header", password="header123")

    @skip("something wrong")
    def test_logout(self):
        """After logout bring user back to login page."""
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.assertFalse(self.test_header.is_authenticated)
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        # last = Bills.objects.last()
        # print(last)
        # all_redirected_url = ["/bill/", "/bill/create/"]
        # if last:
        #     all_redirected_url.append(f"/bill/{last.id-1}")
        # for url in all_redirected_url:
        #     resp = self.client.get(url)
        #     print(url)
        #     self.assertEqual(resp.status_code, 302)

        # # no bills exist in here
        # if last:
        #     url = f"/bill/{last.id+1}"
        #     resp = self.client.get(url)
        #     self.assertEqual(resp.status_code, 301)


class BillViewTest(BaseViewTest):
    """Test for BillView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BillViewTest, self).setUp()

    def test_bill_page(self):
        """After login its will goes to bill page."""
        response = self.client.get("/bill/")
        self.assertEqual(response.status_code, 302)


class BillCreateViewTest(BaseViewTest):
    """Test for BillCreateView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BillCreateViewTest, self).setUp()

    # def test_create_page(self):
    #     """test navigate to create bill page."""
    #     response = self.client.get("/bill/create/")
    #     self.assertEqual(response.status_code, 302)
    def test_navigate_create_bill_page(self):
        """test navigate to bill page"""
        response = self.client.get("/bill/create/")
        self.assertEqual(response.status_code, 302)

    def test_create_bill(self):
        """test created bill."""
        self.assertEqual(Bills.objects.get(pk=1), self.bill) # create success

    def test_create_initial_topic(self):
        """test create a bill with initial topic."""
        self.new_bill = Bills.objects.create(header=self.user_profile, name="Food Bill")
        self.est = Topic.objects.create(title="Est", price=20, bill=self.new_bill)
        self.est.add_user(self.user1)
        self.est.add_user(self.user2)
        self.new_bill.add_topic(self.est)
        # response1 = self.client.post(reverse("bills:create"),{"title":"Food Bill", "topic_name":"Est", "topic_price":20, "username":"test_user1", "create":"Create Title"})
        # self.assertEqual(Bills.objects.get(pk=3), self.bill)
        # print("Tomato", self.client.post("/bill/create/")['lst_user'])
        # self.assertQuerysetEqual(response.context[''], [])

class DetailViewTest(BaseViewTest):
    def setUp(self):
        """Setup before running a tests."""
        super(DetailViewTest, self).setUp()

    def test_navigation(self):
        """test navigation after bill object has created"""
        response = self.client.get("/bill/1/")
        self.assertEqual(response.status_code, 302)
