from django.urls import path

from . import views
from .views import CategoryList

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('category/<int:category_id>/', CategoryList.as_view(), name='category-products'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product-detail'),

    # cart urls
    # path('cart/', views.cart_view, name='cart_view'),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    # path('add/<int:product_id>/', views.cart_view, name='add_to_cart'),
    # path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('change_product_cart/<int:product_id>/<str:action>/', views.change_product_cart, name='change_product_cart'),

    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('change_product_cart/<int:product_id>/<str:action>/', views.change_product_cart, name='change_product_cart'),

]
