from django.db import models
from agents.models import AgentDB
from actions.models import ActionDB
from document.models import Document, DocumentElement
import json

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
    action = models.ForeignKey(ActionDB, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    previous_instruction = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Instruction {self.pk}: {self.action.name if self.action else 'No action'}"
    
    def get_possible_actions(self):
        if self.previous_instruction:
            return self.previous_instruction.action.get_next_actions()
        else:
            return ActionDB.objects.filter(previous_action=None)
