from django.urls import reverse
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, Payment
from unittest import SkipTest


class UserProfileViewTest(BaseSetUp):
    def setUp(self):
        super(UserProfileViewTest, self).setUp()
        self.test_header = User.objects.create(
            username="test_header", email="test@example.com"
        )
        self.test_header.set_password("header123")
        self.test_header.save()
        self.user_profile = UserProfile.objects.create(user=self.test_header)
        self.user_profile.save()
        self.client.force_login(self.test_header)

    def test_display_name(self):
        data = {"display name": "Toast"}
        self.client.post(reverse("user-profile:userprofile"), data=data)
        self.assertEqual(self.user_profile.name, "Toast")

    @SkipTest
    def test_fetch_key(self):
        data = {"fetch-key": "fetch"}
        response = self.client.post(reverse("user-profile:fetch-key", data))
        self.assertEqual(response.status_code, 302)
