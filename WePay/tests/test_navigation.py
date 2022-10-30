from django.urls import reverse
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from ..models.payment import Bills  # ,Food
from WePay.models.upload import UploadBillForm, UploadTopicForm
from datetime import timezone

class BaseViewTest(BaseSetUp):
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


class BillCreateViewTest(BaseViewTest):
    """Test for BillCreateView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BaseViewTest, self).setUp()

    def test_create_page(self):
        """test navigate to create bill page."""
        response = self.client.get("/bill/create/")
        self.assertEqual(response.status_code, 302)

    def test_form_topic_data(self):
        """Test for form_topic data"""
        form_topic_data = {"title": "Chicken", "price": 2000, "bill": self.bill, "user": self.user1}
        form = UploadTopicForm(data=form_topic_data)
        self.assertTrue(form.is_valid())

    def test_form_bill_data(self):
        form_bill_data = {"header": self.header, "name": "blabla", "pub_date":timezone.localtime}
        form = UploadBillForm(data=form_bill_data)
        self.assertTrue(form.is_valid())