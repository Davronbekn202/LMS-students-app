from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.create_user, name='registration'),
    path('log-in/', views.login_user, name='login'),
    path('log-out/', views.logout_user, name='logout'),
]
