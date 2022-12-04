from django.urls import reverse
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from .utlis import create_user

class UserProfileViewTest(BaseSetUp):
    def setUp(self):
        """Setup before test"""
        super(UserProfileViewTest, self).setUp()
        self.test_header = create_user("test_header", "header123", "will32672@hotmail.com")
        self.test_user = create_user("test_user", "1234", "user@example.com")
        self.client.force_login(self.test_header.user)

    def test_display_name(self):
        """Test display name"""
        data = {"display name": "Toast"}
        response = self.client.post(reverse("user-profile:userprofile"), data=data)
        self.assertEqual(response["Location"], "/user-profile/")  # POST success
        response2 = self.client.get(reverse("user-profile:userprofile"))
        self.assertEqual(response2.context["user"].username, "Toast")  # GET success

    def test_fetch_key_with_example_email(self):
        """Test fetch chain id with example email."""
        self.client.logout()
        self.client.force_login(self.test_user.user)
        response = self.client.post(reverse("user-profile:fetch-key"))
        self.assertEqual(response.status_code, 302)
        response2 = self.client.get(reverse("user-profile:userprofile"))
        self.assertEqual(response2.context["chain_id"], "")
        response3 = self.client.get(reverse("user-profile:fetch-key"))
        self.assertContains(response3, "", status_code=302)

    def test_fetch_key(self):
        """Test fetch chain id with same email as omise."""
        response = self.client.post(reverse("user-profile:fetch-key"))
        self.assertEqual(response.status_code, 302)
        response2 = self.client.get(reverse("user-profile:userprofile"))
        self.assertEqual(response2.context["chain_id"], "acch_test_5tmytw2wqewbq05abwu")
