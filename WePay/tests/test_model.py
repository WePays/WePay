from django.urls import reverse

from WePay.models.payment import AlreadyPayError
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, Payment, CashPayment, PromptPayPayment, SCBPayment, KTBPayment, BBLPayment, BAYPayment
from unittest import SkipTest


class BillModelTest(BaseSetUp):
    """test for Bill model"""

    def test_calculate_price(self):
        """test calculate price for each user."""
        self.pepsi.add_user(self.user1)
        self.pepsi.add_user(self.user2)
        self.coke.add_user(self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 10.0)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 25.0)

    def test_total_price(self):
        """test total price in bill."""
        self.assertEqual(self.bill.total_price, 35)

    def test_all_user(self):
        """test all user."""
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertListEqual(
            self.bill.all_user,
            list(set(self.pepsi.user.all()).union(set(self.coke.user.all()))),
        )

    def test_duplicate_user(self):
        """test when you add duplicate user."""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user1)
        self.coke.add_user(user=self.user2)
        self.assertEqual(self.bill.calculate_price(person=self.user1), 20)
        self.assertEqual(self.bill.calculate_price(person=self.user2), 15)


class TopicModelTest(BaseSetUp):
    """test for Food model."""

    def test_each_price(self):
        """test food price for each user."""
        self.pepsi.add_user(user=self.user1)
        self.pepsi.add_user(user=self.user2)
        self.assertEqual(self.pepsi.calculate_price(), 10)

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


class PaymentModelTest(BaseSetUp):
    """test for payment model."""

    def setUp(self):
        """SetUp before test"""
        super(PaymentModelTest, self).setUp()

    def test_create_duplicate_payment(self):
        """Test create duplicate payment object."""
        self.test = Payment.objects.create(bill=self.bill, user=self.user1)

    def test_payment_choice(self):
        """test payment type."""
        self.assertEqual(self.cash_payment.selected_payment, CashPayment)
        self.assertEqual(self.promptpay_payment.selected_payment, PromptPayPayment)
        self.assertEqual(self.scb_payment.selected_payment, SCBPayment)
        self.assertEqual(self.ktb_payment.selected_payment, KTBPayment)
        self.assertEqual(self.bay_payment.selected_payment, BAYPayment)
        self.assertEqual(self.bbl_payment.selected_payment, BBLPayment)

    # def test_payment_status(self):
    #     """test payment status for each payment"""
    #     for payment in self.lst_payment:
    #         self.assertEqual(payment.status, "UNPAID")
    #         payment.pay()
    #         if payment == self.cash_payment:
    #             self.assertEqual(payment.status, "PENDING")
    #         else:
    #             self.assertEqual(payment.status, "PAID")
    #         # After status == PAID its can still paid.
    #         self.assertRaises(AlreadyPayError, payment.pay())

    def test_payment_calculate_price(self):
        """test calculate price for each user in bill."""
        for user in self.lst_user:
            self.pepsi.add_user(user)
        self.assertEqual(self.cash_payment.price, self.pepsi.calculate_price())
        self.assertEqual(self.promptpay_payment.price, self.pepsi.calculate_price())
        self.assertEqual(self.scb_payment.price, self.pepsi.calculate_price())
        self.assertEqual(self.ktb_payment.price, self.pepsi.calculate_price())
        self.assertEqual(self.bay_payment.price, self.pepsi.calculate_price())
        self.assertEqual(self.bbl_payment.price, self.pepsi.calculate_price())


class UserProfileTest(BaseSetUp):
    def setUp(self):
        super(UserProfileTest, self).setUp()
