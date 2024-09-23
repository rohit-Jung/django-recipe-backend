# urls.py
from django.urls import path
from .views import mealplan_list_create, mealplan_detail

urlpatterns = [
    path('mealplans/', mealplan_list_create, name='mealplan-list-create'),
    path('mealplans/<int:pk>/', mealplan_detail, name='mealplan-detail'),
]
