from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('introduction/', views.IntroductionView.as_view(), name='introduction_page'),
    path('advantages/', views.AdvantagesView.as_view(), name='advantages_page'),
]
