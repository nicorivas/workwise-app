from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=256)
    default = models.BooleanField(default=False)
    subdomain = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"