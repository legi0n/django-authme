from typing import Union

from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.forms import BaseForm, ModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase

HttpRequestType = HttpRequest
HttpResponseType = Union[HttpResponseBase, HttpResponse]
FormType = Union[BaseForm, ModelForm]
UserType = AbstractUser
AnyUserType = Union[AbstractUser, AnonymousUser]
