from attr import field
from django.forms import ModelForm
from django import forms
from .bill import Topic


class UploadTopicForm(ModelForm):
    title = forms.TextInput()
    price = forms.DecimalField()
    bill = forms.TextInput()
    user = forms.TextInput()

    class Meta:
        model = Topic
        fields = ['title', 'price', 'bill', 'user']