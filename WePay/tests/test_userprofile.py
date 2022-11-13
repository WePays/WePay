from django.urls import reverse
from .setUp import BaseSetUp
from django.contrib.auth.models import User
from WePay.models.userprofile import UserProfile
from ..models import Bills, Topic, Payment
from unittest import SkipTest


class UserProfileViewTest(BaseSetUp):
    def setUp(self):
        super(UserProfileViewTest, self).setUp()

    @SkipTest
    def test_display_name(self):
        response = self.client.post("/user-profile/", {"display name": "Toast"})

    @SkipTest
    def test_fetch_key(self):
        data = {"fetch-key": "fetch"}
        response = self.client.post(reverse("user-profile:fetch-key", data))
        self.assertEqual(response.status_code, 302)
