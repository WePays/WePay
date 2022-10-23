from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Bills  # ,Food


class BaseViewTest(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        self.user1 = User.objects.create_user(
            username="test_user1", email="user1@example.com", password="user1")
        self.user1.save()
        self.client.login(username="test_user1", password="user1")

    def test_logout(self):
        """After logout bring user back to login page."""
        self.client.logout()
        last = Bills.objects.last()
        all_redirected_url = ['/bill/', '/bill/create/']
        if last:
            all_redirected_url.append(f'/bill/{last.id-1}')
        for url in all_redirected_url:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302)

        # no bills exist in here
        if last:
            url = f'/bill/{last.id+1}'
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 301)


class BillViewTest(BaseViewTest):
    """Test for BillView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BaseViewTest, self).setUp()

    def test_bill_page(self):
        """After login its will goes to bill page."""
        response = self.client.get(reverse("bills:bill"))
        self.assertEqual(response.status_code, 302)
