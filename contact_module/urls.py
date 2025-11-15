from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactUsCreateView.as_view(), name='contact_us_page')
]
