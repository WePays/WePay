from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User

from WePay.views import bill

from ..models import Bills, Food #, Payment, BankPayment
# Create your tests here.

class BillModelTest(TestCase):

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
        self.user3 = User.objects.create_user(username="test_user3",
            email="user3@example.com", password="user3"
        )
        self.user3.save()
        self.user4 = User.objects.create_user(username="test_user4",
            email="user4@example.com", password="user4"
        )
        self.user4.save()
        self.client.login(username="header", password="header123")
        self.client.login(username="test_user1", password="user1")
        self.client.login(username="test_user2", password="user2")
        # self.client.login(username="test_user3", password="user3")
        # self.client.login(username="test_user4", password="user4")

    """test for Bill model"""

    # @skip("unfinished test")
    def test_calculate_price(self):
        """test calculate price"""
        bill = Bills.objects.create(header=self.header, name='Food Bill')
        pepsi = Food.objects.create(title='Pepsi', price=12, bill=bill)
        pepsi.add_user(user=self.user1)
        pepsi.add_user(user=self.user2)
        coke = Food.objects.create(title='Coke', price=15, bill=bill)
        coke.add_user(user=self.user2)
        self.assertEqual(bill.calculate_price(person=self.user1), pepsi.each_price())
        self.assertEqual(bill.calculate_price(person=self.user2), coke.each_price())


    @skip("unfinished test")
    def test_total_price(self):
        """test total price"""


    @skip("unfinished test")
    def test_all_user(self):
        """test all user"""
