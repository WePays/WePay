from typing import Union

import omise
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """User Profile of each user
    Attr:
        user: :model:`auth.User` (ForignKey)
        chain_id: str
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chain_id = models.CharField(max_length=100, default="")

    @property
    def name(self) -> str:
        """get a name of each user(username)

        Returns:
            str -- username of each user
        """
        return self.user.username

    @property
    def chain(self) -> Union[omise.Chain, None]:
        """get a omise Chain of each user

        Returns:
            Union[omise.Chain, None] -- if user has linked chain with omise
            and fetch key already it will return a Chain object else it will
            return None otherwise
        """
        omise.api_secret = settings.OMISE_SECRET
        return omise.Chain.retrieve(self.chain_id) if self.chain_id else None

    def __repr__(self) -> str:
        """represent UserProfile object with human readable code

        Returns:
            str -- name of each user that user manually set
        """
        return self.name

    __str__ = __repr__
