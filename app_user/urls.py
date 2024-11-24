from django.contrib.auth.views import LoginView
from django.urls import path

from app_main.views import checkout
from .views import UserRegistration,  user_logout, Account

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='app_user/login.html'), name='login' ),
    path('logout/', user_logout, name='logout'),
    path('account/<int:user_id>/', Account.as_view(), name='account'),
    path('checkout/', checkout, name='checkout'),

]
