from django.db import models
from agents.models import AgentDB
from actions.models import ActionDB

class Document(models.Model):
    # TODO: Maybe documents should also keep the original reply from the model, before parsing to Markdown.
    name = models.CharField(max_length=256)
    text = models.TextField()
    version = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    instruction = models.ForeignKey("Instruction", on_delete=models.CASCADE, null=True, blank=True)
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
    agent = models.ForeignKey(AgentDB, on_delete=models.CASCADE, null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Instruction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.ForeignKey(ActionDB, on_delete=models.CASCADE)
    prompt = models.TextField(null=True, blank=True)
