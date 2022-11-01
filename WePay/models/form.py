from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .userprofile import UserProfile
from .bill import Topic, Bills
from .payment import BasePayment, OmisePayment, CashPayment


class UploadTopicForm(ModelForm):

    # def __init__(self, request, *args, **kwargs):
    #     """ Grants access to the request object so that only members of the current user
    #     are given as options"""

    title = forms.TextInput()
    price = forms.DecimalField()
    bill = forms.TextInput()
    user = forms.TextInput()
    # # user = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    # user = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())

    class Meta:
        model = Topic
        fields = ('title', 'price', 'bill', 'user')


class UploadBillForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UploadBillForm, self).__init__(*args, **kwargs)
        self.fields['header'].queryset = UserProfile.objects.filter(user=self.request.user)

    header = forms.CharField()
    name = forms.TextInput()
    pub_date = forms.DateTimeField(initial=timezone.localtime())

    class Meta:
        model = Bills
        fields = ('header', 'name', 'pub_date')


class PaymentForm(ModelForm):

    class Meta:
        model = OmisePayment
        fields = ('user', 'payment_type')
