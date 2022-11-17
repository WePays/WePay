from django.contrib.auth.models import User
from django.shortcuts import reverse
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, CashPayment, Payment
from .setUp import BaseSetUp
from django.test import TestCase


class TestPayment(TestCase):

    def setUp(self):
        """Setup before running a tests."""
        header1 = User.objects.create_user(
            username="header1", email="header1@example.com", password="header123"
        )
        self.header1 = UserProfile.objects.create(
            user=header1)
        self.header1.save()

        header2 = User.objects.create_user(
            username="header2", email="header2@example.com", password="header123"
        )
        self.header2 = UserProfile.objects.create(
            user=header2, chain_id="acch_test_5tl5qdsa0cbli76hwoj"
        )
        self.header2.save()

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
            username="test_user3", email="user3@example.com", password="user3"
        )
        self.user3 = UserProfile.objects.create(user=user3)
        self.user3.save()

        self.user_tup = (self.user1, self.user2, self.user3)

        self.bill = Bills.objects.create(header=self.header1, name="Food Bill")
        self.pepsi = Topic.objects.create(title="Pepsi", price=50)
        self.coke = Topic.objects.create(title="Coke", price=20)
        self.salmon = Topic.objects.create(title='Salmon', price=500)

        self.pepsi.add_user(self.user1)
        self.pepsi.add_user(self.user3)

        self.coke.add_user(self.header1)
        self.coke.add_user(self.user2)

        self.salmon.add_user(self.header1)
        self.salmon.add_user(self.user1)
        self.salmon.add_user(self.user3)

        self.bill.add_topic(self.pepsi)
        self.bill.add_topic(self.coke)
        self.bill.add_topic(self.salmon)
        self.bill.save()

        self.bill1 = Bills.objects.create(header=self.header2, name='Bowling bill')

        socks = Topic.objects.create(title='Socks', price=100)
        bowling = Topic.objects.create(title='bowling 2 game', price='300')
        socks.add_user(self.user1)
        bowling.add_user(self.user2)
        bowling.add_user(self.header2)
        bowling.add_user(self.user1)
        self.bill1.add_topic(socks)
        self.bill1.add_topic(bowling)
        self.bill1.save()

        self.client.force_login(self.header1.user)

        self.header_payment = Payment.objects.create(user=self.header1, bill=self.bill)
        self.user1_payment = Payment.objects.create(user=self.user1, bill=self.bill)
        self.user2_payment = Payment.objects.create(user=self.user2, bill=self.bill)
        self.user3_payment = Payment.objects.create(user=self.user3, bill=self.bill)

        self.header1_payment = Payment.objects.create(user=self.header1, bill=self.bill1)
        self.user1_bill1_payment = Payment.objects.create(user=self.user1, bill=self.bill1)
        self.user2_bill1_payment = Payment.objects.create(user=self.user2, bill=self.bill1)

    def test_payment_doesnt_exist(self):
        """get payment that not exist will not have detail"""
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 100}))
        self.assertEqual(resp.status_code, 302)

    def test_cash_only_payment(self):
        """when pay lessthan 20 bath or morethan 150k baht it need to pay cash only"""
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 3}))
        self.assertContains(resp, "* Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash", status_code=200)

    def test_paid_header_no_chain(self):
        """Cant pay with other choice when header not have chain"""
        self.client.logout()
        self.client.force_login(self.user1.user)
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 2}))
        self.assertContains(resp, "* This bill is not in chain, you can only pay with cash or tell header to register the chain \
                    \n<a href='/instruction/'>instruction here</a>", status_code=200)

    def test_pay_redirect(self):
        """testing whether pay button truly redirect"""
        # cashpayment
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp = self.client.post(reverse("payments:detail", kwargs={"pk": 3}), data={"payment_type": "Cash"})
        self.assertRedirects(resp, reverse("payments:payment"), status_code=302, target_status_code=200)
        self.assertEqual(self.user2_payment.status, Payment.Status_choice.PENDING)
        # ! BUG

        # # other payment
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp = self.client.post(reverse("payments:detail", kwargs={"pk": 7}), data={"payment_type": "SCB"})
        self.assertRedirects(resp, self.user2_bill1_payment.uri, status_code=302, fetch_redirect_response=False)
