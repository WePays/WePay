from django.contrib import admin

from .models import Bills, Food, BankPayment, CashPayment, PromptPayPayment

class BillsAdmin(admin.ModelAdmin):
    list_display = ('header', 'name', 'pub_date')

class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'bill')

class BankPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'bill', 'status', 'image', 'bank_name', 'bank_account', 'name')


class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'bill', 'status')

class PromptPayPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'bill', 'status', 'phone_number', 'name')


admin.site.register(Bills, BillsAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(BankPayment, BankPaymentAdmin)
admin.site.register(CashPayment, CashPaymentAdmin)
admin.site.register(PromptPayPayment, PromptPayPaymentAdmin)
