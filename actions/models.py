from django.db import models

class Action(models.Model):
    """Abstract representation of an action.
    Actions are high-level things that agents can do. 
    They are composed of instructions.

    Attributes:
        agent (Agent): The agent that can perform the action.
        name (str): The name of the action.
        identifier (str): The identifier of the action.
        short_description (str): One sentence description.
        description (str): The description of the action.
        first_instruction_type (InstructionType): The first instruction type in the sequence.
        beta (bool): If the action is in beta.
        alpha (bool): If the action is in alpha.
    """
    agent = models.ForeignKey('agents.Agent', related_name='actions', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256, default="Not set")
    short_description = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    first_instruction_type = models.ForeignKey('instruction.InstructionType', related_name='first_instruction_type', on_delete=models.CASCADE, null=True, blank=True)
    beta = models.BooleanField(default=True)
    alpha = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    @property
    def get_action_text(self):
        return "Create " + self.name.lower()
    
    @property
    def get_action_subtext(self):
        return self.short_description