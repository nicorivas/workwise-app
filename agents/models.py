from django.db import models

class AgentType(models.Model):
    
    name = models.CharField(max_length=256)
    definition = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    short_title = models.CharField(max_length=512, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="agents", null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.name} - {self.short_title}"

class Trait(models.Model):

    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    self_definition = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class Personality(models.Model):
    
    name = models.CharField(max_length=256)
    traits = models.ManyToManyField(Trait, null=True, blank=True)

    def __str__(self):
        return self.name

class Agent(models.Model):
    
    type = models.ForeignKey(AgentType, on_delete=models.CASCADE)
    company = models.ManyToManyField("company.Company")
    name =  models.CharField(max_length=256, null=True, blank=True) # Fields are optional as they could deafult to type.
    definition = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_title = models.CharField(max_length=512, null=True, blank=True)
    object = models.JSONField(null=True, blank=True)
    personality = models.ForeignKey(Personality, null=True, blank=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="agents", null=True, blank=True)
    show_in_explorer = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}. {self.name} - {self.short_title}"
    
    def greeting_message(self):
        return "Hi! How can I help you?"

    def check_project(self, project):

        if project.action.name == "Feedback Advice":

            project.add_instruction("Feedback follow up")

            return True
    
