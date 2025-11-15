from django.contrib import admin

from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from contact_module.models import ContactUs


class ContactUsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    readonly_fields = ['get_create_date_jalali']
    list_display = ['user', 'title', 'get_create_date_jalali', 'is_read_by_admin', 'is_active', 'parent']
    list_editable = ['is_active']

    def get_create_date_jalali(self, obj):
        return date2jalali(obj.create_date).strftime('%Y/%m/%d')

    get_create_date_jalali.short_description = 'تاریخ ایجاد'
    get_create_date_jalali.admin_order_field = 'create_date'


admin.site.register(ContactUs, ContactUsAdmin)
