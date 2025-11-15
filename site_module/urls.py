from django.urls import path

from site_module import views

urlpatterns = [
    path('gallery/', views.GalleryListView.as_view(), name='gallery_page'),
]
