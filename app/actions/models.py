from django.db import models

class ActionDB(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    instruction = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name