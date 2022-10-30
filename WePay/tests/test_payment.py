from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, CashPayment
from .setUp import BaseSetUp
from unittest import skip

# class CashPayment(BaseSetUp):
#     def setUp(self):
#         super(BaseSetUp, self).setUp()
#         self.hawaiian_pizza = Topic.objects.create(title='Hawaiian Pizza', price=40, bill=self.bill)
#         self.boston_pizza = Topic.objects.create(title='Boston Pizza', price=45, bill=self.bill)
#         self.user1_payment = CashPayment.objects.create(bill=self.bill, user=self.user1, amount=100)
    
#     def test_paid_status(self):
#         """Test that the bill is paid when all users have paid"""
#         self.assertEqual(self.user1_payment.status, 'UNPAID')
#         self.user1_payment.pay()
#         self.assertEqual(self.user1_payment.status, 'PAID')
#         self.assertEqual(self.user1_payment.amount, 100)
#         self.assertEqual(self.user1_payment.pay(), 'Already paid')
        
#     def test_unpaid_status(self):
#         """Test that the bill is unpaid when all users have not paid"""
#         self.assertEqual(self.user2_payment.status, 'UNPAID')
#         self.assertEqual(self.user2_payment.amount, 100)
