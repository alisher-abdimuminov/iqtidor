from django.http import HttpRequest


class PayMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if (request.path == "/pay/"):
            try:
                request.META.pop("HTTP_AUTHORIZATION")
            finally:
                pass
        response = self.get_response(request)
        return response