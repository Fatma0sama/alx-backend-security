from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.core.cache import cache

from .models import RequestLog, BlockedIP

try:
    from ipgeolocation import IpGeolocationAPI
except Exception:
    IpGeolocationAPI = None


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Forbidden")

        country = None
        city = None

        cache_key = f"geo_{ip}"
        geo = cache.get(cache_key)

        if geo:
            country, city = geo
        elif IpGeolocationAPI:
            try:
                geo_api = IpGeolocationAPI()
                data = geo_api.get(ip)
                country = data.get("country_name")
                city = data.get("city")
                cache.set(cache_key, (country, city), 86400)
            except Exception:
                pass

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=now(),
            country=country,
            city=city
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
