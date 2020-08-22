from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('user_subscription/<subscription_number>',
         views.user_subscription,
         name='user_subscription'),
    path('order_history/<order_number>',
         views.order_history,
         name='order_history'),
]
