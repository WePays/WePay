import logging
from typing import List
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Bills(models.Model):
    header = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def calculate_price(self, person: User) -> float:
        """calculate price for each person"""
        food = Topic.objects.filter(bill=self)
        return sum(
            each_food.each_price()
            for each_food in food
            if person in each_food.user.all()
        )

    @property
    def total_price(self):
        """calculate total price"""
        food = Topic.objects.filter(bill=self)
        return sum(each_food.price for each_food in food)

    @property
    def all_user(self) -> List[User]:
        """return list of all user"""
        food = Topic.objects.filter(bill=self)
        return list({each_food.user for each_food in food})

    def __repr__(self) -> str:
        return (
            f"Bills(header={self.header}, name={self.name}, pub_date={self.pub_date})"
        )

    __str__ = __repr__


class Topic(models.Model):
    """Topic model"""

    title = models.CharField(max_length=100)
    price = models.IntegerField("price")
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name="food")

    def each_price(self):
        return self.price / len(self.user.all())

    def add_user(self, user):
        if user not in self.user.all():
            self.user.add(user)
        else:
            logging.info("user already in this food")