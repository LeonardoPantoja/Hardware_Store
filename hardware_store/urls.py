from . import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import register, login_view, remove_from_cart
from allauth.socialaccount import urls as socialaccount_urls

urlpatterns = [
    path('', views.home, name='home'),

    # Products
    path('product_list', views.product_list, name='product_list'),
    path('create_product', views.create_product , name='create-product'),
    path('edit_product/<int:pk>', views.edit_product , name='edit-product'),
    path('delete_product/<int:pk>', views.delete_product , name='delete-product'),
    path('product_list/<int:pk>/', views.category_products, name='category_products'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    # Category
    path('category_list', views.category_list , name='category-list'),
    path('create_category', views.create_category , name='create-category'),
    path('edit_category/<int:pk>', views.edit_category , name='edit-category'),
    path('delete_category/<int:pk>', views.delete_category , name='delete-category'),
    # Account
    path('accounts/', include('allauth.urls')),
    path('accounts/', include(socialaccount_urls)),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),

    # Cart
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

]