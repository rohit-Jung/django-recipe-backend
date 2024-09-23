# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update_user, name='user_update'),
    path('current-user/', views.get_current_user, name="current_user"),
    path('token/refresh/', views.custom_token_refresh_view, name='token_refresh'),


    #other routes
    path('users/', views.user_list_create, name='user_list_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
]
