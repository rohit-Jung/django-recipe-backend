from django.urls import path
from .views import saved_recipe_list_create, saved_recipe_detail, saved_recipe_list

urlpatterns = [
    path('', saved_recipe_list, name='saved_recipe_list'),
    path('create/', saved_recipe_list_create, name='saved_recipe_list_create'),
    path('<int:pk>/', saved_recipe_detail, name='saved_recipe_detail'),
]
