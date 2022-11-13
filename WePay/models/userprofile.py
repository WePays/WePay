from django.db import models
from django.contrib.auth.models import User
from typing import Union
import omise


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chain_id = models.CharField(max_length=100, default="")

    @property
    def name(self):
        return self.user.username

    @property
    def chain(self) -> Union[omise.Chain, None]:
        print(self.chain_id)
        return omise.Chain.retrieve(self.chain_id) if self.chain_id else None

    def __repr__(self) -> str:
        return self.user.username

    __str__ = __repr__
