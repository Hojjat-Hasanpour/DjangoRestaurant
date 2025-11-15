from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from site_module.models import SiteGallery


class GalleryListView(ListView):
    template_name = 'site_module/gallery.html'
    model = SiteGallery
    context_object_name = 'site_images'
    paginate_by = 12

    def get_queryset(self):
        query = super(GalleryListView, self).get_queryset()
        query = query.filter(is_active=True)
        return query
