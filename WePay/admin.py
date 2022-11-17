from django.contrib import admin
from django.template.defaulttags import register

from .models import Bills, Payment, Topic, UserProfile


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class BillsAdmin(admin.ModelAdmin):
    list_display = ("header", "name", "pub_date")


class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "bill")


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "bill", "date", "status", "payment_type")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


admin.site.register(Bills, BillsAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payment, PaymentAdmin)
