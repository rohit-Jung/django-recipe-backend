from django.urls import path
from . import views

# Recipe URLs
urlpatterns = [
    path('', views.recipe_list, name='recipe-list'),
    path('create/', views.recipe_create, name='recipe-create'),  
    path('user/', views.get_user_recipes, name='user-recipes'), 
    path('<int:pk>/', views.each_recipe_detail, name='recipe-detail'), 
    path('<int:pk>/delete/', views.delete_recipe, name='recipe-delete'),  
    path('<int:pk>/update/', views.update_recipe, name='recipe-update'),  
]

# Review URLs
urlpatterns += [
    path('reviews/', views.review_list, name='review-list'),
    path('reviews/<int:recipe_id>/create/', views.create_review, name='create-review'),
    path('reviews/<int:pk>/', views.review_detail, name='review-detail'),
    path('reviews/<int:pk>/update/', views.update_review, name='update-review'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete-review'),
]