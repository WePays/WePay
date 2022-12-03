from ..models import UserProfile, Bills, Topic, Payment
from django.contrib.auth.models import User


def create_user(username: str, password: str, email: str, chain_id: str = "") -> UserProfile:
    """create a user"""
    user = User.objects.create_user(
        username=username, email=email, password=password)
    userprofile = UserProfile.objects.create(
        user=user, chain_id=chain_id
    )
    userprofile.save()
    return userprofile

def create_bill(header: UserProfile, name: str)-> Bills:
    """create a bill"""
    bill = Bills.objects.create(header=header, name=name)
    bill.save()
    return bill

def create_topic(title: str, price: int, bill: Bills)-> Topic:
    """create a topic"""
    topic = Topic.objects.create(title=title, price=price, bill=bill)
    topic.save()
    return topic

def add_user_topic(topic: Topic, lst_user: list[UserProfile]):
    """add user to topic"""
    for user in lst_user:
        topic.add_user(user)
    topic.save()
    return

def create_payment(bill: Bills, user: UserProfile, pay_type: str="Cash"):
    """create a payment"""
    payment = Payment.objects.create(bill=bill, user=user)
    payment.payment_type = pay_type
    payment.save()
    return payment
