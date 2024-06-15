
from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register-user"),
    path('update_user/<user_id>', views.update_user, name="update-user"),
    path('update_password/<user_id>', views.update_password, name="update-password"),
]
