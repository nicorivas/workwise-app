from django.db import models

#from document.models import Document

class Company(models.Model):
    name = models.CharField(max_length=256)
    default = models.BooleanField(default=False)
    #strategy = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="company_strategy", null=True, blank=True)
    #values = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="company_values", null=True, blank=True)

    def __str__(self):
        return self.name