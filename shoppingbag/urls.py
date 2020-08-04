from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_shoppingbag, name="view_shoppingbag"),
    path('add/<item_id>/', views.add_to_shoppingbag, name="add_to_shoppingbag"),
    path('adjust/<item_id>/', views.adjust_shoppingbag, name="adjust_shoppingbag"),
    path('remove/<item_id>/', views.remove_from_shoppingbag, name="remove_from_shoppingbag"),
]
