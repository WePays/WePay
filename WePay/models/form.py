from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .userprofile import UserProfile
from .bill import Topic, Bills
from .payment import BasePayment, OmisePayment, CashPayment


class UploadTopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ("title", "price", "user")


class UploadBillForm(ModelForm):

    header = forms.TextInput()
    name = forms.TextInput()

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super(UploadBillForm, self).__init__(*args, **kwargs)
    #     self.fields['header'].queryset = UserProfile.objects.filter(user=self.request.user)

    class Meta:
        model = Bills
        fields = ("header", "name")

    def save(self, topic: Topic, commit: bool = ...):
        super().save(commit)
        topic.bill = self.instance
        topic.save()
        return super().save(commit)


# class PaymentForm(ModelForm):

#     payment_type = forms.ChoiceField(choices=OmisePayment.PaymentChoice)

#     class Meta:

#         model = OmisePayment
#         fields = ('user', 'payment_type')
