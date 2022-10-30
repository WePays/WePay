from email.policy import default
from attr import field
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .bill import Topic, Bills


class UploadTopicForm(ModelForm):
    title = forms.TextInput()
    price = forms.DecimalField()
    bill = forms.TextInput()
    user = forms.TextInput()

    class Meta:
        model = Topic
        fields = ('title', 'price', 'bill', 'user')

class UploadBillForm(ModelForm):
    header = forms.TextInput()
    name = forms.TextInput()
    pub_date = forms.DateTimeField(initial=timezone.localtime)

    class Meta:
        model = Bills
        fields = ('header', 'name', 'pub_date')