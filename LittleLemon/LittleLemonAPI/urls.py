from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.MenuItemsListView.as_view(), name='menu-items-list'),
    
]
