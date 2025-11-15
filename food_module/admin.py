from django.contrib import admin
from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Food, FoodCategory, FoodCapacity


class FoodAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

    list_display = ['name', 'category', 'is_active', 'slug']
    list_editable = ['is_active']
    list_filter = ['category']


class FoodCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

    list_display = ['name', 'slug', 'is_active', 'is_delete']
    list_editable = ['is_active', 'is_delete']


class FoodCapacityAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['food', 'get_date_jalali', 'is_active', 'capacity']
    # list_editable = ['is_active', 'capacity']
    list_filter = ['food']

    def get_date_jalali(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')

    get_date_jalali.short_description = 'تاریخ'
    get_date_jalali.admin_order_field = 'date'


admin.site.register(Food, FoodAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(FoodCapacity, FoodCapacityAdmin)
