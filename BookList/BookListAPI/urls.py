from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
# router = DefaultRouter(trailing_slash=False)
# router.register('books', views.Book, basename='books')

# urlpatterns = router.urls
#function based urls
# urlpatterns = [
#     path('menu-items/', views.menu_items, name='menu-items'),
#     path('category/<int:pk>',views.category_detail, name='category-detail'),
#     path('numbers', views.display_even_numbers, name="even-numbers"),
#     path('secret/', views.secret, name='secret'),
#     path('manager-view/', views.manager_view),
#     path('throttle-check/', views.throttle_check_anon),
#     path('throttle-check-auth/', views.throttle_check_auth),
#     path('api-auth-token/', obtain_auth_token),

# ]
#class based urls
urlpatterns = [
    path('menu-items/',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>/',views.MenuItemsViewSet.as_view({'get':'retrieve', 'put':'update'})),
    path('books', views.Books.as_view(), name='books'),
    # path('menu-items', views.MenuItemsView.as_view(), name='menu-items'),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('categories', views.CategoryListCreate.as_view(), name='category-items'),
    path('numbers', views.display_even_numbers, name="even-numbers"),
    path('api-auth-token/', obtain_auth_token),

]

