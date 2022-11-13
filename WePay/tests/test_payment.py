from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, CashPayment, Payment
from .setUp import BaseSetUp
from unittest import skip

# class TestPayment(BaseSetUp):
#     def setUp(self):
#         super(TestPayment, self).setUp()
#         self.pepsi.add_user(self.user1)
#         self.pepsi.add_user(self.user2)
#         self.coke.add_user(self.user2)
#         self.cash_payment = Payment.objects.create(bill=self.bill, user=self.user1)
#         self.cash_payment.payment_type = "Cash"
#         self.promptpay_payment = Payment.objects.create(bill=self.bill, user=self.user2)
#         self.promptpay_payment.payment_type = "PromptPay"

#     def test_create_duplicate_payment(self):
#         """Test create duplicate payment object."""
#         self.test = Payment.objects.create(bill=self.bill, user=self.user1)

#     def test_payment_choice(self):
#         """test payment choice."""
#         self.assertEqual(self.cash_payment.payment_type,"Cash")
#         self.assertEqual(self.promptpay_payment.payment_type, "PromptPay")
