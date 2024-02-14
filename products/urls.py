from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.product, name="products"),
    path("addproduct", views.addProduct, name="addproducts"),
    path('edit/<int:pk>/', views.editProduct, name='editProducts'),
    path('delete/<int:pk>/', views.deleteProduct, name='deleteProducts'),
    path('product_list', views.product_list, name='product_list'),
    # path('addcart/<int:product_id>/', views.addcart, name='addcart'),
    # path('cart', views.cart_detail, name='cart_detail'),
    # path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

