from django.contrib import admin
from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from django_jalali.admin.filters import JDateFieldListFilter
# from rangefilter2.filter import DateRangeFilter
# from rangefilter.filters import (
#     DateRangeFilterBuilder,
#     DateTimeRangeFilterBuilder,
#     NumericRangeFilterBuilder,
#     DateRangeQuickSelectListFilterBuilder,
# )

from .models import Order, OrderDetail


class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'get_payment_date_jalali']
    readonly_fields = ['user', 'is_paid', 'payment_date']
    # list_filter = ['user', 'is_paid', 'payment_date']
    list_filter = ['user', 'is_paid', ('payment_date', JDateFieldListFilter)]

    @admin.display(description='تاریخ پرداخت', ordering='payment_date')
    def get_payment_date_jalali(self, obj):
        if not obj.payment_date:
            return '-'
        return date2jalali(obj.payment_date).strftime('%Y/%m/%d')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
