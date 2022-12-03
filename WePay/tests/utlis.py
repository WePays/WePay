from ..models import UserProfile
from django.contrib.auth.models import User


def create_user(username: str, password: str, email: str) -> UserProfile:
    """create a user"""
    user = User.objects.create_user(
        username=username, email=email, password=password)
    userprofile = UserProfile.objects.create(
        user=user, chain_id="acch_test_5tl5qdsa0cbli76hwoj"
    )
    userprofile.save()
    return userprofile
