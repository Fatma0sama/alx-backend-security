from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def login_view(request):
    return JsonResponse({"message": "Login view"})
