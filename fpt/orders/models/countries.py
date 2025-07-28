# Django

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    phone_prefix = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ("country", "name")

    def __str__(self):
        return f"{self.name} ({self.country.code})"
