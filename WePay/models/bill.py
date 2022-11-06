import logging
from typing import List, Union
from django.db import models
from django.utils import timezone
from .userprofile import UserProfile

import omise


class Bills(models.Model):
    """
    Bill for each group that had header and title
    header -> :model:`Wepay.UserProfile`
    """

    header = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    pub_date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    @property
    def header_chain(self) -> omise.Chain:
        """header Omise Chain for Omise Payment

        Raises:
            ValueError: if header doesnt have chain

        Returns:
            Union[omise.Chain, None] -- _description_
        """

        if self.header.chain is None:
            # implement later
            logging.warning(
                "YOU MUST have a chain by click this link and verify your account"
            )
            raise ValueError(
                "YOU MUST have a chain by click this link and verify your account"
            )
        return self.header.chain

    def calculate_price(self, person: UserProfile) -> float:
        """calculate price for each person

        Arguments:
            person {UserProfile} -- each person in bills

        Returns:
            float -- price for each person
        """
        # get all topic that person had
        topic = Topic.objects.filter(bill=self)

        # sum all the price that person in that topic and return it
        return sum(
            each_topic.each_price()
            for each_topic in topic
            if person in each_topic.user.all()
        )

    @property
    def total_price(self) -> float:
        """calculate total price"""
        food = Topic.objects.filter(bill=self)
        return sum(each_food.price for each_food in food)

    @property
    def all_user(self) -> List[UserProfile]:
        """get all user who sharing with this bill

        Returns:
            List[UserProfile] -- user who Coordinate paying in that bill
        """
        food = Topic.objects.filter(bill=self)
        user_queryset = [each_food.user.all() for each_food in food]
        result = set()  # initial the set

        # add all user to set
        for queryset in user_queryset:
            result = result.union([queryset[idx] for idx in range(len(queryset))])
        return list(result)

    def __repr__(self) -> str:
        """represent Bill objects in str form"""
        return (
            f"Bills(header={self.header}, name={self.name}, pub_date={self.pub_date})"
        )

    __str__ = __repr__


class Topic(models.Model):
    """Topic model"""

    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE, null=True)
    user = models.ManyToManyField(UserProfile, related_name="topic")

    def each_price(self):

        return self.price / len(self.user.all())

    def add_user(self, user):
        if user not in self.user.all():
            self.user.add(user)
        else:
            logging.info("user already in this food")
