from django.http import HttpRequest


class PayMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        print(request.META)
        print(request.body)
        print(request.headers)

                
        response = self.get_response(request)
        return response