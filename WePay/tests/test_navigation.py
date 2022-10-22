from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User


class BillViewTest(TestCase):
    """Test for BillView"""
    def setUp(self):
        """Setup before running a tests."""
        self.user1 = User.objects.create_user(username="test_user1",
                                              email="user1@example.com", password="user1")
        self.user1.save()
        self.client.login(username="test_user1", password="user1")

    def test_bill_page(self):
        """After login its will goes to bill page."""
        response = self.client.get(reverse("bills:bill"))
        self.assertEqual(response.status_code, 200)

    
    def test_logout(self):
        """After logout bring user back to login page."""
        self.client.logout()
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)