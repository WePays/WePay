from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Bills, Food  # , Payment, BankPayment
# Create your tests here.


class BillModelTest(TestCase):
    """test for Bill model"""

    def setUp(self):
        """Setup before running a tests."""
        self.header = User.objects.create_user(username="header",
                                               email="header@example.com", password="header123"
                                               )
        self.header.save()
        self.user1 = User.objects.create_user(username="test_user1",
                                              email="user1@example.com", password="user1"
                                              )
        self.user1.save()
        self.user2 = User.objects.create_user(username="test_user2",
                                              email="user2@example.com", password="user2"
                                              )
        self.user2.save()
        self.client.login(username="header", password="header123")
        self.client.login(username="test_user1", password="user1")
        self.client.login(username="test_user2", password="user2")

        self.bill = Bills.objects.create(header=self.header, name='Food Bill')
        self.pepsi = Food.objects.create(title='Pepsi', price=20, bill=self.bill)
        self.coke = Food.objects.create(title='Coke', price=15, bill=self.bill)

    def test_calculate_price(self):
        """test calculate price"""
        self.pepsi.add_user(self.user1)
        self.pepsi.add_user(self.user2)
        self.coke.add_user(user=self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 10.0)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 25.0)

    def test_total_price(self):
        """test total price"""
        self.assertEqual(self.bill.total_price, 35)

    def test_all_user(self):
        """test all user"""
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertListEqual(self.bill.all_user, [self.pepsi.user, self.coke.user])

    def test_duplicate_user(self):
        """test duplicate user"""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 20)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 15)


class FoodModelTest(TestCase):
    """test for Food model"""

    def setUp(self):
        """Setup before running a tests."""
        self.header = User.objects.create_user(username="header",
                                               email="header@example.com", password="header123"
                                               )
        self.header.save()
        self.user1 = User.objects.create_user(username="test_user1",
                                              email="user1@example.com", password="user1"
                                              )
        self.user1.save()
        self.user2 = User.objects.create_user(username="test_user2",
                                              email="user2@example.com", password="user2"
                                              )
        self.user2.save()
        self.client.login(username="header", password="header123")
        self.client.login(username="test_user1", password="user1")
        self.client.login(username="test_user2", password="user2")

        self.bill = Bills.objects.create(header=self.header, name='Food Bill')
        self.pepsi = Food.objects.create(title='Pepsi', price=20, bill=self.bill)
        self.coke = Food.objects.create(title='Coke', price=15, bill=self.bill)

    def test_each_price(self):
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        self.assertEqual(self.pepsi.each_price(), 10)

    def test_add_user(self):
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        self.assertIn(self.user1, self.pepsi.user.all())
        self.assertIn(self.user2, self.pepsi.user.all())

    def test_add_duplicate_user(self):
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        check = sum(user == self.user1 for user in self.pepsi.user.all())
        self.assertEqual(check, 1)
