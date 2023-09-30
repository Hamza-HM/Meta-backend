from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter(trailing_slash=False)
# router.register('books', views.Book, basename='books')

# urlpatterns = router.urls
#function based urls
# urlpatterns = [
#     path('menu-items/', views.menu_items, name='menu-items'),
#     path('category/<int:pk>',views.category_detail, name='category-detail'),
#     path('numbers', views.display_even_numbers, name="even-numbers"),
# ]
#class based urls
urlpatterns = [
    path('menu-items/',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>/',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('books', views.Books.as_view(), name='books'),
    # path('menu-items', views.MenuItemsView.as_view(), name='menu-items'),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('categories', views.CategoryListCreate.as_view(), name='category-items'),
    path('numbers', views.display_even_numbers, name="even-numbers"),
]
