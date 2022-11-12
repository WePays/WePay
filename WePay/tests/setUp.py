# from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, Payment


class BaseSetUp(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        header = User.objects.create_user(
            username="header", email="header@example.com", password="header123"
        )
        self.header = UserProfile.objects.create(user=header, chain_id="acch_test_5tl5qdsa0cbli76hwoj")
        self.header.save()

        user1 = User.objects.create_user(
            username="test_user1", email="user1@example.com", password="user1"
        )
        self.user1 = UserProfile.objects.create(user=user1)
        self.user1.save()

        user2 = User.objects.create_user(
            username="test_user2", email="user2@example.com", password="user2"
        )
        self.user2 = UserProfile.objects.create(user=user2)
        self.user2.save()

        user3 = User.objects.create_user(
            username="test_user3", email="user3@example.com", password="user3")
        self.user3 = UserProfile.objects.create(user=user3)
        self.user3.save()

        user4 = User.objects.create_user(
            username="test_user4", email="user4@example.com", password="user4")
        self.user4 = UserProfile.objects.create(user=user4)
        self.user4.save()

        user5 = User.objects.create_user(
            username="test_user5", email="user5@example.com", password="user5")
        self.user5 = UserProfile.objects.create(user=user5)
        self.user5.save()

        user6 = User.objects.create_user(
            username="test_user6", email="user6@example.com", password="user6")
        self.user6 = UserProfile.objects.create(user=user6)
        self.user6.save()

        self.client.login(user="header", password="header123")
        self.client.login(user="test_user1", password="user1")
        self.client.login(user="test_user2", password="user2")
        self.client.login(user="test_user3", password="user3")
        self.client.login(user="test_user4", password="user4")
        self.client.login(user="test_user5", password="user5")
        self.client.login(user="test_user6", password="user6")

        self.bill = Bills.objects.create(header=self.header, name="Food Bill")
        self.pepsi = Topic.objects.create(title="Pepsi", price=20, bill=self.bill)
        self.coke = Topic.objects.create(title="Coke", price=15, bill=self.bill)

        # Set up for payment

        self.cash_payment = Payment.objects.create(bill=self.bill, user=self.user1)
        self.cash_payment.payment_type = "Cash"
        self.promptpay_payment = Payment.objects.create(bill=self.bill, user=self.user2)
        self.promptpay_payment.payment_type = "PromptPay"
        self.scb_payment = Payment.objects.create(bill=self.bill, user=self.user3)
        self.scb_payment.payment_type = "SCB"
        self.ktb_payment = Payment.objects.create(bill=self.bill, user=self.user4)
        self.ktb_payment.payment_type = "KTB"
        self.bay_payment = Payment.objects.create(bill=self.bill, user=self.user5)
        self.bay_payment.payment_type = "BAY"
        self.bbl_payment = Payment.objects.create(bill=self.bill, user=self.user6)
        self.bbl_payment.payment_type = "BBL"
