from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.city, name='city_info'),
    path('f', views.f),
]