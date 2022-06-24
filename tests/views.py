from django.views.generic.base import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse

__all__ = [
    'TestView',
]


class TestView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('Hello, world!')

    def post(self, request: HttpRequest) -> HttpResponse:
        return self.get(request)

    def put(self, request: HttpRequest) -> HttpResponse:
        return self.get(request)

    def delete(self, request: HttpRequest) -> HttpResponse:
        return self.get(request)
