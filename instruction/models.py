from django.db import models

from projects.models import Project
from actions.models import Action

class Instruction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    previous_instruction = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Instruction {self.pk}: {self.action.name if self.action else 'No action'}"
    
    def get_possible_actions(self):
        if self.previous_instruction:
            return self.previous_instruction.action.get_next_actions()
        else:
            return Action.objects.filter(previous_action=None)
