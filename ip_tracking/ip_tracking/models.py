from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.CharField(max_length=255)
