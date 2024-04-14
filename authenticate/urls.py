from django.urls import path
from .views import register, login_user, logout_user, RegistrationWizard

urlpatterns = [
    path('register/', RegistrationWizard.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # ... your other URLs
]
