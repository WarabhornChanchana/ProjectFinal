from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('add_slide/', views.add_slide, name='add_slide'),
    path('admin_order/', views.admin_order, name='admin_order'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)