# from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, Payment
from .utlis import create_user, create_bill, create_topic, create_payment


class BaseSetUp(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        self.header = create_user('header', 'header123', 'header@exmple.com', "acch_test_5tl5qdsa0cbli76hwoj")
        self.user1 = create_user("test_user1", "user1", "user1@example.com")
        self.user2 = create_user("test_user2", "user2", "user2@example.com")
        self.user3 = create_user("test_user3", "user3", "user3@example.com")
        self.user4 = create_user("test_user4", "user4", "user4@example.com")
        self.user5 = create_user("test_user5", "user5", "user5@example.com")
        self.user6 = create_user("test_user6", "user6", "user6@example.com")

        self.bill = create_bill(self.header, "Food Bill")
        self.pepsi = create_topic("Pepsi", 20, self.bill)
        self.coke = create_topic("Coke", 15, self.bill)

        # Set up for payment
        self.cash_payment = create_payment(self.bill, self.user1, "Cash")
        self.promptpay_payment = create_payment(self.bill, self.user2, "PromptPay")
        self.scb_payment = create_payment(self.bill, self.user3, "SCB")
        self.ktb_payment = create_payment(self.bill, self.user4, "KTB")
        self.bay_payment = create_payment(self.bill, self.user5, "BAY")
        self.bbl_payment = create_payment(self.bill, self.user6, "BBL")

        self.lst_payment = [
            self.cash_payment,
            self.promptpay_payment,
            self.scb_payment,
            self.ktb_payment,
            self.bay_payment,
            self.bbl_payment,
        ]
        self.lst_user = [
            self.user1,
            self.user2,
            self.user3,
            self.user4,
            self.user5,
            self.user6,
        ]
