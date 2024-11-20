from django.urls import path, include
from rest_framework import routers
from .views import *

routers = routers.DefaultRouter()

routers.register(r'users/', UserProfileViewSet, basename='user_list'),
routers.register(r'store_list/', StoreViewSet, basename='store_list'),
routers.register(r'product/', ProductViewSet, basename='product_list'),
routers.register(r'orders/', OrdersViewSet, basename='orders_list'),
routers.register(r'rating', RatingViewSet, basename='rating_list'),
routers.register(r'cart', CartViewSet, basename='cart_list'),
routers.register(r'cartitem', CarItemViewSet, basename='cartitem_list'),


urlpatterns = [
    path('', include(routers.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('courier', CourierViewSet.as_view({'get': 'list', 'post': 'create'}), name='courier_list')

]