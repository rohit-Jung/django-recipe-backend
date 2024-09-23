# urls.py
from django.urls import path
from .views import shoppinglist_list_create, shoppinglist_detail, delete_ingredient_item, update_ingredient_item

urlpatterns = [
    path('', shoppinglist_list_create, name='shoppinglist-list-create'),
    path('<int:pk>/', shoppinglist_detail, name='shoppinglist-detail'),

    path('ingredient-items/delete/<int:item_id>/', delete_ingredient_item, name='delete_ingredient_item'),
    path('ingredient-items/update/<int:item_id>/', update_ingredient_item, name='delete_ingredient_item'),
]
