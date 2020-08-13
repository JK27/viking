from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('user_subscription/<subscription_number>',
         views.user_subscription,
         name='user_subscription'),
]
