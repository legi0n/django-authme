from django.urls import path, include

urlpatterns = [
	path('one_step/', include('authme.shortcuts.one_step.urls')),
]
