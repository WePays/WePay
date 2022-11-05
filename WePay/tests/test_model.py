from .setUp import BaseSetUp
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic


class BillModelTest(BaseSetUp):
    """test for Bill model"""

    def SetUp(self):
        super(BaseSetUp, self).setUp()

    def test_calculate_price(self):
        """test calculate price for each user."""
        self.pepsi.add_user(self.user1)
        self.pepsi.add_user(self.user2)
        self.coke.add_user(user=self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 10.0)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 25.0)

    def test_total_price(self):
        """test total price in bill."""
        self.assertEqual(self.bill.total_price, 35)

    def test_all_user(self):
        """test all user."""
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertListEqual(self.bill.all_user, list(set(self.pepsi.user.all()).union(set(self.coke.user.all()))))

    def test_duplicate_user(self):
        """test when you add duplicate user."""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 20)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 15)


class TopicModelTest(BaseSetUp):
    """test for Food model."""

    def SetUp(self):
        super(BaseSetUp, self).setUp()

    def test_each_price(self):
        """test food price for each user."""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        self.assertEqual(self.pepsi.each_price(), 10)

    def test_add_user(self):
        """test add user to Food.user.all()"""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        self.assertIn(self.user1, self.pepsi.user.all())
        self.assertIn(self.user2, self.pepsi.user.all())

    def test_add_duplicate_user(self):
        """test add duplicate user to that food."""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        check = sum(user == self.user1 for user in self.pepsi.user.all())
        self.assertEqual(check, 1)
