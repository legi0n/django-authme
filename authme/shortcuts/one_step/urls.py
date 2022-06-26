from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='authme_signup'),
    path('login/', LoginView.as_view(), name='authme_login'),
]

del path