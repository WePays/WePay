# from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic


class BaseSetUp(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        header = User.objects.create_user(
            username="header", email="header@example.com", password="header123"
        )
        self.header = UserProfile.objects.create(user=header)
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

        self.client.login(user="header", password="header123")
        self.client.login(user="test_user1", password="user1")
        self.client.login(user="test_user2", password="user2")

        self.bill = Bills.objects.create(header=self.header, name="Food Bill")
        self.pepsi = Topic.objects.create(title="Pepsi", price=20, bill=self.bill)
        self.coke = Topic.objects.create(title="Coke", price=15, bill=self.bill)
