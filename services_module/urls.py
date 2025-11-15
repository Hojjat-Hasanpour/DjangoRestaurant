from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.ServicesListView.as_view(), name='services_list_page')
    re_path(r'service/(?P<slug>[-\w]+)/', views.ServicesDetailView.as_view(), name='service_detail_page'),
]
