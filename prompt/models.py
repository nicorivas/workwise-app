from django.db import models
from actions.models import Action
from django.contrib.auth.models import User

class Prompt(models.Model):
    name = models.CharField(max_length=256)
    index = models.IntegerField(default=0)
    prompt = models.JSONField(default=dict)
    action = models.ManyToManyField(Action, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_updated_by')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"