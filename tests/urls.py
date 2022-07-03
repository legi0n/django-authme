from django.urls import include, path

urlpatterns = [
    path("one_step/", include("authme.shortcuts.one_step.urls")),
]
