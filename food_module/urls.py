from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.FoodTemplateView.as_view(), name='food_category_page'),
    re_path(r'food/(?P<slug>[-\w]+)/', views.FoodDetailView.as_view(), name='food_detail_page'),
    # path('<slug:slug>', views.RoomDetailView, name='room_detail_page'),
]
