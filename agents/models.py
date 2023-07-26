from django.db import models

# Create your models here.

class TraitDB(models.Model):

    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    self_definition = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class PersonalityDB(models.Model):
    
    name = models.CharField(max_length=256)
    traits = models.ManyToManyField(TraitDB, null=True, blank=True)

    def __str__(self):
        return self.name

class AgentDB(models.Model):
    
    name =  models.CharField(max_length=256)
    definition = models.CharField(max_length=512)
    object = models.JSONField()
    personality = models.ForeignKey(PersonalityDB, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name