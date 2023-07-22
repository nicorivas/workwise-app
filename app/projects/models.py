from django.db import models
from agents.models import AgentDB

# Create your models here.

class Message(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    agent = models.ForeignKey(AgentDB, on_delete=models.CASCADE, null=True, blank=True)
    user = models.CharField(max_length=256, null=True, blank=True)
    type = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.message

class Record(models.Model):
    voice_record = models.FileField(upload_to="records")
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("record_detail", kwargs={"id": str(self.id)})

class Project(models.Model):

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name