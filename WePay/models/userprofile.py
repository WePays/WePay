from django.db import models
from django.contrib.auth.models import User
import omise


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chain_key = models.CharField(max_length=100, default='')

    @property
    def chain(self) -> omise.Chain:
        return omise.Chain.retrieve(self.chain_key)

    def __str__(self):
        return self.user.username
