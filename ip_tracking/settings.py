INSTALLED_APPS += [
    "ip_tracking",
    "ratelimit",
]

MIDDLEWARE += [
    "ip_tracking.middleware.IPTrackingMiddleware",
]

RATELIMIT_ENABLE = True
