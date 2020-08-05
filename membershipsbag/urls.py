from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_membershipsbag, name="view_membershipsbag"),
    path('add/<item_id>/', views.add_to_membershipsbag,
         name="add_to_membershipsbag"),
]
