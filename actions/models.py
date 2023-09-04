from django.db import models

class Action(models.Model):
    """Abstract representation of an action. Actions are high-level things that agents can do. They are composed of instructions.
    
    Usually, Actions are modules containing actions in Mimesis.

    Attributes:
        agent (Agent): The agent that can perform the action.
        name (str): The name of the action.
        identifier (str): The identifier of the action.
        description (str): The description of the action.
        first_instruction_type (InstructionType): The first instruction type in the sequence.
    """
    agent = models.ForeignKey('agents.Agent', related_name='actions', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256, default="Not set")
    description = models.CharField(max_length=512)
    first_instruction_type = models.ForeignKey('instruction.InstructionType', related_name='first_instruction_type', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}" 