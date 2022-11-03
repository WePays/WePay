from django.contrib import admin

from .models import *


class BillsAdmin(admin.ModelAdmin):
    list_display = ("header", "name", "pub_date")


class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "bill")


class BankPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "bill",
        "status",
        "bank_name",
        "bank_account",
        "name",
    )


class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "bill", "status")

    
class OmisePaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "bill", "status", "payment_type")



admin.site.register(Bills, BillsAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(CashPayment, CashPaymentAdmin)
admin.site.register(PromptPayPayment, OmisePaymentAdmin)
admin.site.register(SCBPayment, OmisePaymentAdmin)
admin.site.register(STBPayment, OmisePaymentAdmin)
admin.site.register(BBLPayment, OmisePaymentAdmin)
admin.site.register(BAYPayment, OmisePaymentAdmin)
