from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.cartdisplay, name="cartdisplay"),
    path('cart/remove_single/<int:product_id>/', views.remove_single_from_cart, name='remove_single_from_cart'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)