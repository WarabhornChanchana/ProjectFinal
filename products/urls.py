from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.product, name="products"),
    path("addproduct", views.addProduct, name="addproducts"),
    path('edit/<int:pk>/', views.editProduct, name='editProducts'),
    path('delete/<int:pk>/', views.deleteProduct, name='deleteProducts'),
    path('search/', views.product_search, name='product_search'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

