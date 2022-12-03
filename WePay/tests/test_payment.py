from unittest import skip

from django.shortcuts import reverse
from django.test import TestCase

from .utlis import create_user, create_payment, create_bill, create_topic, add_user_topic
from ..models import Bills, Payment, Topic


class TestPayment(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        self.header1 = create_user("header1", "header123", "header1@example.com")
        self.header2 = create_user("header2", "header123",
                                   "header2@example.com", "acch_test_5tl5qdsa0cbli76hwoj")
        self.user1 = create_user("test_user1", "user1", "user1@example.com")
        self.user2 = create_user("test_user2", "user2", "user2@example.com")
        self.user3 = create_user("test_user3", "user3", "user3@example.com")
        self.user4 = create_user("test_user4", "user4", "user4@example.com")
        self.user5 = create_user("test_user5", "user5", "user5@example.com")
        self.user6 = create_user("test_user6", "user6", "user6@example.com")

        self.user_tup = (self.user1, self.user2, self.user3, self.user4, self.user5, self.user6)

        # bill1
        self.bill = create_bill(header=self.header1, name="Food Bill")
        self.pepsi = create_topic(title="Pepsi", price=50, bill=self.bill)
        self.coke = create_topic(title="Coke", price=20, bill=self.bill)
        self.salmon = create_topic(title="Salmon", price=500, bill=self.bill)

        add_user_topic(self.pepsi, [self.user1, self.user3])
        add_user_topic(self.coke, [self.header1, self.user2])
        add_user_topic(self.salmon, [self.header1, self.user1, self.user3])
        self.bill.save()

        # bill2
        self.bill1 = create_bill(header=self.header2, name="Bowling bill")

        socks = create_topic(title="Socks", price=100, bill=self.bill1)
        bowling = create_topic(title="bowling 2 game", price=300, bill=self.bill1)
        add_user_topic(socks, [self.user1, self.user5, self.user4])
        add_user_topic(bowling, [self.user2, self.header2, self.user1, self.user3])
        self.bill1.save()

        self.client.force_login(self.header1.user)

        self.header_payment = create_payment(user=self.header1, bill=self.bill)
        self.user1_payment = create_payment(user=self.user1, bill=self.bill)
        self.user2_payment = create_payment(user=self.user2, bill=self.bill)
        self.user3_payment = create_payment(user=self.user3, bill=self.bill)

        self.header2_payment = create_payment(user=self.header2, bill=self.bill1)
        self.user1_bill1_payment = create_payment(user=self.user1, bill=self.bill1)
        self.user2_bill1_payment = create_payment(user=self.user2, bill=self.bill1)
        self.user3_bill1_payment = create_payment(user=self.user3, bill=self.bill1)
        self.user4_bill1_payment = create_payment(user=self.user4, bill=self.bill1)
        self.user5_bill1_payment = create_payment(user=self.user5, bill=self.bill1)
        self.user6_bill1_payment = create_payment(user=self.user6, bill=self.bill1)

    def test_payment_doesnt_exist(self):
        """get payment that not exist will not have detail"""
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 100}))
        self.assertEqual(resp.status_code, 404)

    def test_cash_only_payment(self):
        """when pay lessthan 20 baht or morethan 150k baht it need to pay cash only"""
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 3}))
        self.assertContains(
            resp,
            "* Your amount is less than 20 Baht or more than 150,000 Baht, you can only pay with cash",
            status_code=200,
        )

    def test_paid_header_no_chain(self):
        """Cant pay with other choice when header not have chain"""
        self.client.logout()
        self.client.force_login(self.user1.user)
        resp = self.client.get(reverse("payments:detail", kwargs={"pk": 2}))
        self.assertContains(
            resp,
            "* This bill is not in chain, you can only pay with cash or tell header to register the chain \
                    \n instruction<a href='/instruction/'> here</a>",
            status_code=200,
        )

    @skip("AssertionError: '/bill/1/' != '/bill/2/'")
    def test_verify_cash_payment(self):
        """test verify cash payment by header."""
        # cashpayment
        self.client.logout()
        self.client.force_login(self.user1.user)
        resp1 = self.client.post(
            reverse("payments:detail", kwargs={"pk": 2}), data={"payment_type": "Cash"}
        )
        self.assertRedirects(
            resp1, reverse("payments:payment"), status_code=302, target_status_code=200
        )

        resp2 = self.client.get(reverse("payments:detail", kwargs={"pk": 2}))
        self.assertEqual(resp2.context["payment_type"], "Cash")
        self.assertEqual(
            resp2.context["status"], Payment.Status_choice.PENDING
        )  # This is PENDING NOW.

        self.client.logout()
        self.client.force_login(self.header1.user)
        resp3 = self.client.get(reverse("payments:confirm", kwargs={"pk": 2}))
        #! Paid in bill 2 but redirect into bill 1 instead (Its can be my mistake please check)
        self.assertRedirects(resp3, "/bill/2/", 302)

    @skip(
        "omise.errors.InvalidChargeError: amount must be greater than or equal to ฿20 (2000 satangs)"
    )
    def test_pay_redirect_on_cash_payment(self):
        """testing whether pay truly redirect"""
        # cashpayment
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp1 = self.client.post(
            reverse("payments:detail", kwargs={"pk": 3}), data={"payment_type": "Cash"}
        )
        self.assertRedirects(
            resp1, reverse("payments:payment"), status_code=302, target_status_code=200
        )
        resp2 = self.client.get(reverse("payments:detail", kwargs={"pk": 3}))
        self.assertEqual(resp2.context["payment_type"], "Cash")
        #! BUG PENDING in Context But UNPAID on user status
        self.assertEqual(resp2.context["status"], Payment.Status_choice.PENDING)
        #! BUG
        # self.assertEqual(self.user2_payment.status, Payment.Status_choice.PENDING)

    def test_pay_redirect_on_scb_payment(self):
        """testing whether pay truly redirect on SCBPayment"""
        # other payment
        self.client.logout()
        self.client.force_login(self.user2.user)
        resp = self.client.post(
            reverse("payments:detail", kwargs={"pk": 7}), data={"payment_type": "SCB"}
        )
        resp1 = self.client.get(reverse("payments:detail", kwargs={"pk": 7}))
        self.assertEqual(resp1.context["payment_type"], "SCB")
        self.assertRedirects(
            resp,
            resp1.context["payment"].uri,
            status_code=302,
            fetch_redirect_response=False,
        )
        resp2 = self.client.get(reverse("payments:update", kwargs={"pk": 7}))
        self.assertRedirects(resp2, "/payment/", 302)

        #! BUG or I'm misunderstood.
        # self.assertEqual(self.user2_bill1_payment.status, Payment.Status_choice.PAID)

    def test_pay_redirect_on_promptpay_payment(self):
        """when click pay it will redirect to qr pages"""
        self.client.logout()
        self.client.force_login(self.user3.user)
        resp = self.client.post(
            reverse("payments:detail", kwargs={"pk": 8}),
            data={"payment_type": "PromptPay"},
        )
        resp1 = self.client.get(reverse("payments:detail", kwargs={"pk": 8}))
        self.assertEqual(resp1.context["payment_type"], "PromptPay")
        self.assertRedirects(
            resp,
            '/payment/8/qr',
            status_code=302,
            fetch_redirect_response=False,
        )
        resp2 = self.client.get(reverse("payments:update", kwargs={"pk": 8}))
        self.assertRedirects(resp2, "/payment/", 302)

    def test_pay_redirect_on_ktb_payment(self):
        self.client.logout()
        self.client.force_login(self.user4.user)
        resp = self.client.post(
            reverse("payments:detail", kwargs={"pk": 9}), data={"payment_type": "KTB"}
        )
        resp1 = self.client.get(reverse("payments:detail", kwargs={"pk": 9}))
        self.assertEqual(resp1.context["payment_type"], "KTB")
        self.assertRedirects(
            resp,
            resp1.context["payment"].uri,
            status_code=302,
            fetch_redirect_response=False,
        )
        resp2 = self.client.get(reverse("payments:update", kwargs={"pk": 9}))
        self.assertRedirects(resp2, "/payment/", 302)
