from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_memberships, name="memberships"),
    path('<membership_id>', views.membership_detail, name="membership_detail"),
]
