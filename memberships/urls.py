from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_memberships, name="memberships"),
    path('select/<item_id>/', views.select_membership,
         name="select_membership"),
    path('<membership_id>', views.membership_detail, name="membership_detail"),
    path('<view_selected_membership>', views.view_selected_membership,
         name="view_selected_membership"),
]
