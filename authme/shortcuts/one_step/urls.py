from django.urls import path

from .views import LoginView, LogoutView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="authme_signup"),
    path("login/", LoginView.as_view(), name="authme_login"),
    path("logout/", LogoutView.as_view(), name="authme_logout"),
]

del path
