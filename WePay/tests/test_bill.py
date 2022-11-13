from django.urls import reverse

from WePay.models.bill import Topic
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from ..models import UserProfile, Bills
from ..views import create
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

    def test_logout(self):
        """After logout bring user back to login page."""
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        response = self.client.get("/accounts/login/")
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
        self.assertEqual(Bills.objects.get(pk=1), self.bill)  # create success

    def test_create_only_initial_topic(self):
        """test create a bill with initial topic."""
        self.new_bill = Bills.objects.create(
            header=self.user_profile, name="Beverage(s)"
        )
        self.est = Topic.objects.create(title="Est", price=20, bill=self.new_bill)
        self.est.add_user(self.user1)
        self.est.add_user(self.user2)
        self.new_bill.add_topic(self.est)
        self.assertEqual(Bills.objects.get(pk=2), self.new_bill)
        self.assertEqual(Bills.objects.get(pk=2).name, self.new_bill.name)
        self.assertEqual(Topic.objects.get(pk=3).title, self.est.title)
        self.assertEqual(Topic.objects.get(pk=3).price, self.est.price)
        self.assertEqual(Bills.objects.get(pk=2).all_user, [self.user1, self.user2])
        create(self.client.post("/bill/"), 2)
        self.assertTrue(Bills.objects.get(pk=2).is_created)
        # create(self.new_bill, 2)
        # self.assertTrue(self.new_bill.is_created)
        # self.assertEqual(Topic.objects.all().count(), 1)
        # response1 = self.client.post(reverse("bills:create"),{"title":"Food Bill", "topic_name":"Est", "topic_price":20, "username":"test_user1", "create":"Create Title"})
        # self.client.post(reverse("bills:create"), {"user": self.est.user.all()})
        # self.assertEqual(Topic.objects.get(user=self.user1), self.bill)
        # print("Tomato", Topic.objects.get(user=self.user1).user)
        # self.assertQuerysetEqual(response.context[''], [])

    def test_response_with_create_bill(self):
        data = {
            "title": "Est", "topic_name": "Toast", "username": [self.user1, self.user2], "topic_price": 2000
        }
        self.client.post(reverse("bills:create"), data=data)
        self.assertFalse(Bills.objects.last().is_created)

    def test_create_bill_with_more_topic(self):
        """test create a bill with initial topic and add more topic."""
        self.new_bill = Bills.objects.create(
            header=self.user_profile, name="Beverage(s)"
        )
        self.est = Topic.objects.create(title="Est", price=20, bill=self.new_bill)
        self.est.add_user(self.user1)
        self.est.add_user(self.user2)
        self.new_bill.add_topic(self.est)
        self.fanta = Topic.objects.create(title="Fanta", price=30, bill=self.new_bill)
        self.fanta.add_user(self.user1)
        self.fanta.add_user(self.user2)
        self.fanta.add_user(self.user3)
        self.new_bill.add_topic(self.fanta)
        self.assertEqual(Bills.objects.get(pk=2), self.new_bill)
        self.assertEqual(Bills.objects.get(pk=2).name, self.new_bill.name)
        self.assertEqual(Topic.objects.get(pk=3).title, self.est.title)
        self.assertEqual(Topic.objects.get(pk=4).title, self.fanta.title)
        self.assertEqual(
            Bills.objects.get(pk=2).all_user, [self.user1, self.user2, self.user3]
        )
        self.assertEqual(self.new_bill.total_price, 50)
        create(self.client.post("/bill/"), 2)
        self.assertTrue(Bills.objects.get(pk=2).is_created)


class DetailViewTest(BaseViewTest):
    def setUp(self):
        """Setup before running a tests."""
        super(DetailViewTest, self).setUp()

    def test_navigation(self):
        """test navigation after bill object has created"""
        response = self.client.get("/bill/1/")
        self.assertEqual(response.status_code, 302)

    def test_bill_not_exist(self):
        """test navigation if go to bill that does not exist"""
        response = self.client.get("/bill/2")
        self.assertEqual(response.status_code, 301)
