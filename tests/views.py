from django.http.response import HttpResponse
from django.views.generic.base import View

from authme._types import HttpRequestType, HttpResponseType

__all__ = [
    "TestView",
]


class TestView(View):
    def get(self, request: HttpRequestType) -> HttpResponseType:
        return HttpResponse("Hello, world!")

    def post(self, request: HttpRequestType) -> HttpResponseType:
        return self.get(request)

    def put(self, request: HttpRequestType) -> HttpResponseType:
        return self.get(request)

    def delete(self, request: HttpRequestType) -> HttpResponseType:
        return self.get(request)
