from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import upload_payment, success_view 
urlpatterns = [
    path("", views.cartdisplay, name="cartdisplay"),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.upload_payment, name='payment'),
    path('success/', views.success_view, name='success'),
    path('payment-detail/<int:id>/', views.payment_detail, name='payment_detail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

