from django.urls import path
from .views import register, login_user, logout_user, RegistrationWizard
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register/', RegistrationWizard.as_view(), name='register'),
    path('authenticate/login/', LoginView.as_view(template_name='authenticate/login.html'), name='login'), # type: ignore
    path('logout/', logout_user, name='logout'),
    # ... your other URLs
]
