from django.contrib import admin
from django.utils.html import format_html

from . import models
# Register your models here.


class SiteGalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag', 'is_active']
    list_editable = ['is_active']

    def image_tag(self, obj):
        return format_html('<img src="{}" width=100px height=100px />'.format(obj.image.url))

    image_tag.short_description = 'عکس گالری'
    image_tag.admin_order_field = 'image'


admin.site.register(models.SiteSetting)
admin.site.register(models.Slider)
admin.site.register(models.HomeImageOrder)
admin.site.register(models.SiteGallery, SiteGalleryAdmin)
