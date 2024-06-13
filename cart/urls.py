from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import upload_payment, success_view
from .views import order_details
from .views import error_view
from .views import purchase_history, update_order_status
urlpatterns = [
    path("", views.cartdisplay, name="cartdisplay"),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.upload_payment, name='payment'),
    path('success/', views.success_view, name='success'),
    path('order-details/<int:order_id>/', order_details, name='order_details'),
    path('error/', error_view, name='error_view'),
    path('sales_history/', views.sales_history, name='sales_history'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('submit_review/<int:order_id>/<int:product_id>/', views.submit_review, name='submit_review'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

