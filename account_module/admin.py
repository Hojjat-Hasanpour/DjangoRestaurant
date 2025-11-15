from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin


class MyUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('فیلد های شخصی سازی شده', {
            'fields': ['email_active_code'],
        }),
    )

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d _ %H:%M:%S')


admin.site.register(models.User, MyUserAdmin)
