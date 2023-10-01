from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.menu_items_view, name='menu-items-list'),
    path('menu-items/<int:id>', views.menu_item_detailed_view, name='menu-item-detail'),
    path('groups/manager/users', views.ListAddManagers.as_view(), name='list-managers'),
    path('groups/manager/users/<int:pk>', views.DestroyFromManager.as_view(), name='remove-managers'),
    path('groups/delivery-crew/users', views.ListCreateDeliveryCrew.as_view(), name='list-managers'),
    path('groups/delivery-crew/users/<int:pk>', views.DestroyFromDelivery.as_view(), name='remove-delivery'),
]
