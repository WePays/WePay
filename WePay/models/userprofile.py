from django.db import models
from django.contrib.auth.models import User
from typing import Union
import omise


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chain_key = models.CharField(max_length=100, default='')

    @property
    def chain(self) -> Union[omise.Chain, None]:
        return omise.Chain.retrieve(self.chain_key) if self.chain_key else None

    def __str__(self) -> str:
        return self.user.username
