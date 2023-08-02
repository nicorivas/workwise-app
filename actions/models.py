from django.db import models


class ActionFormElementType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class ActionFormElement(models.Model):
    action = models.ForeignKey('ActionDB', on_delete=models.CASCADE)
    type = models.ForeignKey(ActionFormElementType, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    guide = models.CharField(max_length=512, null=True, blank=True)
    audio = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ActionDB(models.Model):
    name = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256, default="Not set")
    description = models.CharField(max_length=512)
    prompt_instructions = models.CharField(max_length=512, null=True, blank=True)
    action_label = models.CharField(max_length=256, null=True, blank=True)
    follow_message = models.CharField(max_length=512, null=True, blank=True)
    previous_action = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey('agents.AgentDB', related_name='actions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_next_actions(self):
        return ActionDB.objects.filter(previous_action=self)
        