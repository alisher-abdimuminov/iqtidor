from django.http import HttpRequest


class PayMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if (request.path == "/pay/"):
            request.META.pop("HTTP_AUTHORIZATION")
        response = self.get_response(request)
        return response